## Healthcare Patient Monitoring System

Real-time IoT glucose monitoring simulation with anomaly detection and predictive analytics.

=> Table of Contents

Overview
Features
Tech Stack
Project Structure
Installation
Usage
How It Works
Current Progress
Roadmap
Learning Journey


=> Overview
A healthcare monitoring system that simulates real-time glucose data from IoT devices, analyzes patient health patterns, and generates automated alerts for anomalies. Built as a learning project to understand:

Real-time data processing
Database design and optimization
Multi-threaded programming
Time-series analysis
Healthcare data patterns

Inspiration: Based on Google Cloud's patient monitoring blueprint, adapted for local development and learning.

=> Features

Implemented
Real-time Data Generation: Simulates glucose readings from IoT devices every 5 seconds
Multi-Patient Support: Concurrent data streams for multiple patients using threading
Persistent Storage: Normalized SQLite database with relational schema
Realistic Patterns: Glucose variations mimicking real-world diabetic/non-diabetic patterns
Data Integrity: SQL injection prevention, foreign key constraints, error handling

In Progress
Anomaly Detection Engine: Pattern recognition for consecutive high readings
Alert System: Automated notifications for critical glucose levels
Time-Series Analysis: Pandas-based trend analysis and 7-day moving averages
Data Visualization: Graphs showing glucose trends and peak risk windows

Planned
RESTful API: FastAPI endpoints for data access
Web Dashboard: Real-time monitoring interface
Predictive Analytics: ML model for glucose forecasting
Cloud Integration: Google Cloud Pub/Sub and BigQuery implementation


=> Tech Stack
Python 3.8+
SQLite
Pandas, NumPy
Threading
FastAPI, RESTful
Matplotlib/Plotly

=> Project Structure
healthcare_monitoring/
│
├── data/
│   └── health_data.db          # SQLite database (auto-generated)
│
├── src/
│   ├── __init__.py
│   ├── database.py             # Database operations (CRUD)
│   ├── data_generator.py       # IoT simulation engine
│   ├── analyzer.py             # Anomaly detection logic
│   └── alert_system.py         # Alert generation
│
├── tests/
│   ├── test_database.py        # Database unit tests
│   └── test_generator.py       # Generator tests
│
├── config.py                   # Configuration settings
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
└── README.md                   # This file


=> Installation
Prerequisites

Python 3.8 or higher
pip (Python package manager)

Setup

Clone the repository

bashgit clone https://github.com/yourusername/healthcare-monitoring.git
cd healthcare-monitoring

Create a virtual environment

bashpython -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate

Install dependencies

bashpip install -r requirements.txt

Initialize database

bashpython -c "from src.database import initialize_database; initialize_database()"

=> Usage
Quick Start
1. Add sample patients:
pythonfrom src.database import add_patient

add_patient("P001", "Alice Johnson", 45, "Type 2 Diabetes")
add_patient("P002", "Bob Smith", 52, "Type 1 Diabetes")
add_patient("P003", "Carol Williams", 38, "Prediabetes")

2. Run simulation:
pythonfrom src.data_generator import simulate_all_patients

# Simulate 3 patients for 2 minutes
patient_ids = ["P001", "P002", "P003"]
simulate_all_patients(patient_ids, duration_minutes=2)
3. Retrieve readings:
pythonfrom src.database import get_recent_reading

readings = get_recent_reading("P001", limit=10)
for r in readings:
    print(f"{r['timestamp']}: {r['glucose_level']} mg/dL")
Configuration
Edit config.py to customize:
python# Database
DATABASE_PATH = 'data/health_data.db'

# Glucose thresholds (mg/dL)
GLUCOSE_THRESHOLD_HIGH = 180
GLUCOSE_THRESHOLD_LOW = 70

# Simulation settings
SIMULATION_INTERVAL = 5  # seconds between readings
NUM_PATIENTS = 3

=> How It Works
Data Flow Architecture
┌─────────────────┐
│  Data Generator │ ──▶ Simulates IoT glucose sensors
└────────┬────────┘
         │ (Every 5 seconds)
         ▼
┌─────────────────┐
│   SQLite DB     │ ──▶ Stores patient data & readings
└────────┬────────┘
         │ (Queries)
         ▼
┌─────────────────┐
│    Analyzer     │ ──▶ Detects anomalies (In Progress)
└────────┬────────┘
         │ (Alerts)
         ▼
┌─────────────────┐
│  Alert System   │ ──▶ Notifications (Planned)
└─────────────────┘

=> Database Schema
Patients Table:
sqlCREATE TABLE patients (
    patient_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    condition TEXT,
    threshold_high REAL DEFAULT 180,
    threshold_low REAL DEFAULT 70
);
Readings Table:
sqlCREATE TABLE readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT NOT NULL,
    glucose_level REAL NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);
Glucose Simulation Logic
For diabetic patients:

Base range: 90-160 mg/dL
Variation: ±20 mg/dL
Spike probability: 10% chance of +30-60 mg/dL spike

For non-diabetic patients:

Base range: 80-120 mg/dL
Variation: ±20 mg/dL
More stable readings


=> Current Progress
Phase 1: Foundation (Complete)

 Project structure setup
 Database schema design
 CRUD operations
 Connection management
 Error handling (IntegrityError, connection failures)

Phase 2: Data Generation (80% Complete)

 Single patient simulation
 Realistic glucose patterns
 Timestamp generation
 Multi-threaded architecture setup
 Complete threading implementation
 Thread safety testing

Phase 3: Analytics (Planned)

 Anomaly detection algorithm
 Pandas time-series analysis
 7-day moving averages
 Peak risk window identification
 Trend forecasting

Phase 4: Alerts (Planned)

 Rule-based alert triggers
 Consecutive high reading detection (3+ occurrences)
 Alert message generation
 Notification system


=> Roadmap
Short-term (Next 2-4 weeks)

 Complete multi-threaded data generation
 Build anomaly detection engine
 Implement basic alert system
 Add unit tests (pytest)

Medium-term (1-2 months)

 FastAPI REST endpoints
 Data visualization dashboard
 Historical trend analysis
 Export data to CSV/JSON

Long-term (3+ months)

 Machine learning model for predictions
 Integration with Google Cloud services
 Real-time WebSocket updates
 Mobile app integration


=> Learning Journey
This project is a hands-on learning experience covering:
Concepts Learned
Database Design:
Normalization (3NF)
Foreign key relationships
SQL vs NoSQL trade-offs
Query optimization

Python Best Practices:
Modular code structure
Configuration management
Error handling patterns
Docstring documentation

Concurrency:
Threading fundamentals
Race condition prevention
Thread-safe database access

Currently Learning:
Pandas DataFrames
Time-series analysis
Statistical anomaly detection
Performance optimization

Key Insights

"Premature optimization is the root of all evil" - Donald Knuth

Make it work → Make it right → Make it fast
Database connections are expensive - use connection pooling
Threading ≠ Parallel processing - Python GIL limitations
Separation of concerns - each module does ONE thing well


Contributing
This is a learning project, but we welcome suggestions.

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit changes (git commit -m 'Add amazing feature')
Push to branch (git push origin feature/amazing-feature)
Open a Pull Request


Acknowledgments:
Inspiration: Google Cloud Healthcare Monitoring Blueprint
Database Tutorial: SQLite official documentation
Community: Python threading discussions on Stack Overflow

January 11, 2026 - Added multi-threaded data generation architecture

Built with ❤️ as a learning journey into healthcare tech and real-time data processing
