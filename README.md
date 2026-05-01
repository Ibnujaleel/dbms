# Health AirSense 📡🍃
**Advanced Air Quality Monitoring & Health Intelligence Platform**

Health AirSense is a premium SaaS-based health monitoring system designed to correlate personal health records with localized air quality metrics. Built with a focus on modern UI/UX principles and secure data management, it provides a scientific framework for personnel health tracking.

---

## 👥 Project Team & Responsibility Breakdown

This project is divided into four critical domains, each managed by a dedicated team member:

### 1. Backend Architecture & System Core (Lead: Member 1)
**Focus:** The "Brain" of the application.
- **Flask Framework Implementation:** Orchestrating the server-side logic, route management, and application lifecycle.
- **RESTful API Development:** Building endpoint services for dynamic data fetching (e.g., the personnel lookup API).
- **Security & Authorization:** Implementing the restricted access system and sync-key validation for the administrative dashboard.
- **Environment Management:** Handling dependency configurations via `requirements.txt` and Flask session management.

### 2. Database Design & Relational Mapping (Lead: Member 2)
**Focus:** Data Integrity & Relational Intelligence.
- **MySQL Schema Architecture:** Designing the `Persons` and `HealthRecords` tables with strong relational constraints.
- **Automated Initialization:** Developed the `init_database()` logic to ensure zero-config setup on new deployments.
- **Relational Integrity:** Implementing `ON DELETE CASCADE` and foreign key mapping to ensure data consistency across patient profiles and medical logs.
- **Query Optimization:** Crafting complex SQL JOINs for the Dashboard to provide real-time telemetry filtering based on age, status, and pathology.

### 3. Frontend Engineering & UI/UX Design (Lead: Member 3)
**Focus:** Premium Visual Identity & Glassmorphism.
- **Design System Implementation:** Developed the custom CSS design system using an 8px grid, Inter/Poppins typography, and the Deep Teal (#0F766E) palette.
- **Glassmorphism Engine:** Engineered the "frosted glass" UI layers using advanced `backdrop-filter` and transparency techniques.
- **Responsive Layouts:** Ensuring the dashboard is fully functional across mobile, tablet, and desktop resolutions.
- **Micro-animations:** Implementing CSS transitions and keyframe animations for page loads, form interactions, and navigation glows.

### 4. Integration, UX & Deployment Roadmap (Lead: Member 4)
**Focus:** User Journey & System Scalability.
- **User Flow Engineering:** designing the 3-step "Initialize → Analysis → Sync" registration stepper to minimize user cognitive load.
- **Template Orchestration:** Managing Jinja2 template inheritance (`layout.html`) to ensure branding consistency across all nodes.
- **Real-time Feedback:** Implementing the flash message system for immediate user confirmation on data syncs.
- **Future Roadmap:** Planning for IoT integration (Air Quality Sensors) and AI-driven predictive health analytics.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- MySQL Server

### Installation
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Database Configuration:**
   Update `DB_CONFIG` in `app.py` with your MySQL credentials.
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'your_user',
       'password': 'your_password',
       'database': 'health_records_db'
   }
   ```
4. **Run the application:**
   ```bash
   python app.py
   ```
5. **Access the Dashboard:**
   - Public: `http://localhost:5000/`
   - Admin Sync Key: `admin2026`

---

## 🛠️ Tech Stack
- **Backend:** Python / Flask
- **Database:** MySQL
- **Frontend:** HTML5 / CSS3 (Glassmorphism)
- **Typography:** Inter & Poppins
- **Design Principles:** SaaS Dashboard, Layered UI, 8px Grid System
