from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from mysql.connector import Error
from datetime import date

app = Flask(__name__)
app.secret_key = 'health_records_secret_key_2026'

# ──────────────────────────────────────────────
# Database Configuration
# ──────────────────────────────────────────────
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '@Axtp8589',        # Update with your MySQL password
    'database': 'health_records_db'
}


def get_db_connection():
    """Create and return a MySQL database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn, None
    except Error as e:
        print(f"Database connection error: {e}")
        return None, str(e)


def init_database():
    """Initialize the database and create tables if they don't exist."""
    try:
        # First connect without specifying a database to create it
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.close()
        conn.close()

        # Now connect to the created database and set up tables
        conn, _ = get_db_connection()
        if conn is None:
            return False

        cursor = conn.cursor()

        # Create Persons table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Persons (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                age INT NOT NULL,
                gender VARCHAR(20) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                email VARCHAR(100) NOT NULL
            )
        """)

        # Create HealthRecords table with foreign key
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS HealthRecords (
                id INT PRIMARY KEY AUTO_INCREMENT,
                person_id INT NOT NULL,
                blood_group VARCHAR(5) NOT NULL,
                conditions TEXT,
                medications TEXT,
                status ENUM('Active', 'Recovered', 'Critical') NOT NULL,
                record_date DATE NOT NULL,
                FOREIGN KEY (person_id) REFERENCES Persons(id)
                    ON DELETE CASCADE
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully.")
        return True

    except Error as e:
        print(f"Database initialization error: {e}")
        return False


# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────

@app.route('/')
def index():
    """Redirect to Add Person page."""
    return redirect(url_for('add_person'))


@app.route('/add-person', methods=['GET', 'POST'])
def add_person():
    """Page 1: Add a new person to the database."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        gender = request.form.get('gender', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()

        # Validation
        if not all([name, age, gender, phone, email]):
            flash('All fields are required.', 'error')
            return redirect(url_for('add_person'))

        try:
            age = int(age)
        except ValueError:
            flash('Age must be a valid number.', 'error')
            return redirect(url_for('add_person'))

        conn, error_msg = get_db_connection()
        if conn is None:
            flash(f'Database connection failed: {error_msg}', 'error')
            return redirect(url_for('add_person'))

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Persons (name, age, gender, phone, email) VALUES (%s, %s, %s, %s, %s)",
                (name, age, gender, phone, email)
            )
            person_id = cursor.lastrowid
            conn.commit()
            flash(f'Basic details for "{name}" saved. Now add health record.', 'success')
            return redirect(url_for('health_status', person_id=person_id))
        except Error as e:
            flash(f'Error: {e}', 'error')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('add_person'))

    return render_template('add_person.html')


@app.route('/health-status', methods=['GET', 'POST'])
def health_status():
    """Page 2: Add or update a health record for a registered person."""
    # Check for pre-selected person from Step 1
    selected_person_id = request.args.get('person_id')
    
    conn, _ = get_db_connection()
    persons = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, name, age FROM Persons ORDER BY id DESC")
            persons = cursor.fetchall()
            cursor.close()
        except Error as e:
            flash(f'Error fetching persons: {e}', 'error')
        finally:
            conn.close()

    if request.method == 'POST':
        person_id = request.form.get('person_id', '').strip()
        blood_group = request.form.get('blood_group', '').strip()
        conditions = request.form.get('conditions', '').strip()
        medications = request.form.get('medications', '').strip()
        status = request.form.get('status', '').strip()
        record_date = request.form.get('record_date', '').strip()

        if not all([person_id, blood_group, status, record_date]):
            flash('Person, blood group, status, and date are required.', 'error')
            return redirect(url_for('health_status'))

        conn, error_msg = get_db_connection()
        if conn is None:
            flash(f'Database connection failed: {error_msg}', 'error')
            return redirect(url_for('health_status'))

        try:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO HealthRecords
                   (person_id, blood_group, conditions, medications, status, record_date)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (int(person_id), blood_group, conditions, medications, status, record_date)
            )
            conn.commit()
            flash('Health record saved successfully!', 'success')
        except Error as e:
            flash(f'Error: {e}', 'error')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('health_status'))

    return render_template('health_status.html', persons=persons, selected_id=selected_person_id)


@app.route('/summary')
def summary():
    """Page 3: Restricted Admin View with filtering."""
    # Simple access check (e.g., prompt for key or check session)
    access_key = request.args.get('key')
    if access_key != 'admin2026':
        return render_template('restricted.html'), 403
    # Get filter parameters
    age_min = request.args.get('age_min', '').strip()
    age_max = request.args.get('age_max', '').strip()
    condition = request.args.get('condition', '').strip()
    status = request.args.get('status', '').strip()

    conn, _ = get_db_connection()
    records = []

    if conn:
        try:
            cursor = conn.cursor(dictionary=True)

            # Build JOIN query with dynamic filters
            query = """
                SELECT
                    p.id AS person_id,
                    p.name,
                    p.age,
                    p.gender,
                    p.phone,
                    p.email,
                    h.id AS record_id,
                    h.blood_group,
                    h.conditions,
                    h.medications,
                    h.status,
                    h.record_date
                FROM HealthRecords h
                JOIN Persons p ON h.person_id = p.id
                WHERE 1=1
            """
            params = []

            if age_min:
                query += " AND p.age >= %s"
                params.append(int(age_min))

            if age_max:
                query += " AND p.age <= %s"
                params.append(int(age_max))

            if condition:
                query += " AND h.conditions LIKE %s"
                params.append(f'%{condition}%')

            if status:
                query += " AND h.status = %s"
                params.append(status)

            query += " ORDER BY h.record_date DESC, p.name ASC"

            cursor.execute(query, params)
            records = cursor.fetchall()
            cursor.close()

        except Error as e:
            flash(f'Error fetching records: {e}', 'error')
        finally:
            conn.close()

    return render_template('summary.html', records=records,
                           filters={'age_min': age_min, 'age_max': age_max,
                                    'condition': condition, 'status': status,
                                    'key': access_key})


@app.route('/api/persons', methods=['GET'])
def api_persons():
    """API endpoint to get all persons (used by Health Status page)."""
    conn, _ = get_db_connection()
    if conn is None:
        return jsonify([])
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, age, gender FROM Persons ORDER BY name")
        persons = cursor.fetchall()
        cursor.close()
        return jsonify(persons)
    except Error:
        return jsonify([])
    finally:
        conn.close()


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────


# Initialize database on module load to ensure it's ready even if using 'flask run'
init_database()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
