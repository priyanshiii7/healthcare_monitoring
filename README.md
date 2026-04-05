# 🏥 Healthcare Patient Monitoring System

> Real-time IoT glucose monitoring simulation with a multi-threaded data pipeline, anomaly detection, and predictive analytics.

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-planned-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active%20Development-orange?style=flat-square)]()

---

## What It Does

This system simulates a real-time patient health monitoring pipeline — the kind that powers IoT devices in clinical settings. It ingests glucose readings every 5 seconds from multiple concurrent patient streams, persists them in a normalised relational database, and runs anomaly detection to flag dangerous readings automatically.

Built with a production-aware architecture from day one: proper DB normalisation, thread-safe concurrent access, SQL injection prevention, and a layered design that separates data generation, storage, and analytics cleanly.

---

## Architecture

```
┌──────────────────────┐
│   IoT Data Generator  │  ← Simulates glucose sensors (every 5s per patient)
│  (Multi-threaded)     │    Realistic diabetic / non-diabetic patterns
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   SQLite Database     │  ← Normalised schema (3NF), FK constraints,
│   (Thread-safe)       │    connection pooling, SQL injection prevention
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Anomaly Analyzer    │  ← Detects consecutive high readings,
│   (In Progress)       │    7-day moving averages, peak risk windows
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Alert System        │  ← Rule-based critical alerts (Planned)
│   + FastAPI Layer     │    REST endpoints, WebSocket real-time updates
└──────────────────────┘
```

---

## Features

### ✅ Implemented
- **Real-time data generation** — glucose readings every 5 seconds per patient
- **Multi-patient concurrency** — independent threads per patient stream, thread-safe DB writes
- **Realistic glucose simulation** — diabetic patterns (90–160 mg/dL + spike probability), non-diabetic patterns (80–120 mg/dL, more stable)
- **Persistent storage** — normalised SQLite schema with relational integrity, FK constraints, and error handling
- **Data integrity** — SQL injection prevention, IntegrityError handling, connection failure recovery

### 🔨 In Progress
- **Anomaly detection engine** — consecutive high reading detection (3+ occurrences trigger alert)
- **Pandas time-series analysis** — 7-day moving averages and trend identification
- **Alert message generation** — structured alert payloads with severity levels

### 📋 Planned
- **FastAPI REST layer** — full CRUD + real-time metrics endpoints with OpenAPI docs
- **Web dashboard** — live monitoring UI with Plotly charts
- **Predictive analytics** — ML model for glucose trend forecasting
- **Cloud integration** — Google Cloud Pub/Sub + BigQuery pipeline

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.8+ |
| Database | SQLite (→ PostgreSQL for production) |
| Data Processing | Pandas, NumPy |
| Concurrency | Python `threading` |
| API (Planned) | FastAPI |
| Visualisation (Planned) | Matplotlib, Plotly |

---

## Database Schema

```sql
CREATE TABLE patients (
    patient_id     TEXT PRIMARY KEY,
    name           TEXT NOT NULL,
    age            INTEGER,
    condition      TEXT,                    -- e.g. "Type 2 Diabetes"
    threshold_high REAL DEFAULT 180,        -- mg/dL alert ceiling
    threshold_low  REAL DEFAULT 70          -- mg/dL alert floor
);

CREATE TABLE readings (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id    TEXT    NOT NULL,
    glucose_level REAL    NOT NULL,
    timestamp     TEXT    NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);
```

**Design decisions:**
- Separate `threshold_high` / `threshold_low` per patient — different conditions require different alert ranges
- `TEXT` timestamps for portability; will migrate to `DATETIME` with indexing for production scale
- Schema in 3NF — no redundant data, clean FK relationships

---

## Glucose Simulation Logic

| Patient Type | Base Range | Variation | Spike Probability |
|---|---|---|---|
| Diabetic (Type 1 / Type 2) | 90–160 mg/dL | ±20 mg/dL | 10% chance of +30–60 mg/dL spike |
| Non-diabetic / Prediabetic | 80–120 mg/dL | ±20 mg/dL | Rare, lower magnitude |

Clinical reference ranges used:
- **Normal:** 70–99 mg/dL (fasting)
- **Prediabetic:** 100–125 mg/dL
- **Diabetic alert (high):** > 180 mg/dL
- **Hypoglycaemia alert (low):** < 70 mg/dL

---

## Installation

**Prerequisites:** Python 3.8+, pip

```bash
# 1. Clone
git clone https://github.com/priyanshiii7/healthcare_monitoring.git
cd healthcare_monitoring

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialise database
python -c "from src.database import initialize_database; initialize_database()"
```

---

## Usage

### Quick Start

```python
from src.database import add_patient
from src.data_generator import simulate_all_patients

# Register patients
add_patient("P001", "Alice Johnson", 45, "Type 2 Diabetes")
add_patient("P002", "Bob Smith",     52, "Type 1 Diabetes")
add_patient("P003", "Carol Williams", 38, "Prediabetes")

# Start simulation (3 patients, 2 minutes)
simulate_all_patients(["P001", "P002", "P003"], duration_minutes=2)
```

### Retrieve Readings

```python
from src.database import get_recent_reading

readings = get_recent_reading("P001", limit=10)
for r in readings:
    print(f"{r['timestamp']}: {r['glucose_level']} mg/dL")
```

### Configuration (`config.py`)

```python
DATABASE_PATH        = 'data/health_data.db'
GLUCOSE_THRESHOLD_HIGH = 180   # mg/dL
GLUCOSE_THRESHOLD_LOW  = 70    # mg/dL
SIMULATION_INTERVAL    = 5     # seconds between readings
NUM_PATIENTS           = 3
```

---

## Project Structure

```
healthcare_monitoring/
├── src/
│   ├── database.py        # DB init, CRUD, connection management
│   ├── data_generator.py  # IoT simulation, threading
│   └── analyzer.py        # Anomaly detection (in progress)
├── data/
│   └── health_data.db     # SQLite database (auto-created)
├── tests/
│   ├── test_generator.py
│   ├── test_database.py
│   ├── test_analyzer.py
│   └── test_full_pipeline.py
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

---

## Development Progress

| Phase | Status | Details |
|-------|--------|---------|
| Phase 1: Foundation | ✅ Complete | DB schema, CRUD, error handling, connection management |
| Phase 2: Data Generation | 🔨 80% | Single + multi-patient simulation, threading architecture |
| Phase 3: Analytics | 📋 Planned | Anomaly detection, Pandas time-series, moving averages |
| Phase 4: API + Dashboard | 📋 Planned | FastAPI endpoints, Plotly visualisation |
| Phase 5: ML Forecasting | 📋 Planned | Glucose trend prediction model |

---

## Roadmap

**Next 2–4 weeks**
- [ ] Complete thread-safe multi-patient simulation
- [ ] Anomaly detection: flag 3+ consecutive high readings
- [ ] Unit tests via `pytest` for all modules

**1–2 months**
- [ ] FastAPI REST layer with Swagger docs
- [ ] Plotly dashboard (glucose trend charts, alert log)
- [ ] CSV/JSON data export

**3+ months**
- [ ] ML forecasting model (Linear Regression → LSTM)
- [ ] Google Cloud Pub/Sub + BigQuery integration
- [ ] WebSocket real-time updates
- [ ] Docker containerisation

---

## Contributing

Contributions and suggestions welcome — this is an active learning project.

```bash
git checkout -b feature/your-feature
git commit -m 'feat: describe your change.'
git push origin feature/your-feature
# Open a Pull Request
```

---

## Inspiration & References

- [Google Cloud Healthcare Monitoring Blueprint](https://cloud.google.com/solutions/healthcare-life-sciences)
- [SQLite Documentation](https://sqlite.org/docs.html)
- Clinical glucose reference ranges: American Diabetes Association guidelines

---

**Built by [Priyanshi Rathore](https://linkedin.com/in/priyanshi-rathore-11b072217) · Final-year CS student · Bikaner, India**
