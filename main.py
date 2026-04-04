from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth import decode_token, hash_password, verify_password, create_access_token
from src.database import (
    initialize_database,
    add_patient,
    get_all_patients,
    get_patient,
    get_recent_readings,
    get_unresolved_alerts,
    create_doctor,
    get_doctor_by_username,
    get_patients_by_doctor,
    assign_patient_to_doctor,
)

from src.analyzer import analyze_patient
from pydantic import BaseModel
from pydantic import BaseModel
from typing import Optional

initialize_database()

app = FastAPI(title="Hospital Glucose Monitor")
security = HTTPBearer()  # Reads the token from request headers

# --- Request Models ---
# Pydantic models define what data we EXPECT to receive
# If the request doesn't match, FastAPI auto-rejects it with a clear error

class PatientCreate(BaseModel):
    patient_id: str
    name: str
    age: int
    condition: str
    threshold_high: float = 180
    threshold_low: float = 70

class DoctorRegister(BaseModel):
    username: str
    full_name: str
    password: str
    specialty: Optional[str] = "General"


class DoctorLogin(BaseModel):
    username: str
    password: str


class AssignPatient(BaseModel):
    patient_id: str


def get_current_doctor(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    This is a dependency — FastAPI runs this automatically on protected endpoints.
    
    It reads the token from the Authorization header,
    decodes it, and returns the doctor's info.
    If the token is missing or invalid, it rejects the request with 401.
    """
    token = credentials.credentials
    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid/expired token")
    
    doctor = get_doctor_by_username(payload.get("username"))
    if not doctor:
        raise HTTPException(status_code=401, detail="Doctor not found")
    return doctor

# --- API Endpoints ---
@app.get("/")
async def root():
    return {"message": "Hospital Glucose Monitor is running"}

@app.post("/auth/register")
async def register(doctor: DoctorRegister):
    """Register a new doctor account."""
    hashed = hash_password(doctor.password)
    success = create_doctor(
        username=doctor.username,
        full_name=doctor.full_name,
        password_hash=hashed,
        specialty=doctor.specialty
    )
    if not success:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": f"Account created for Dr. {doctor.full_name}"}


@app.post("/auth/login")
async def login(credentials: DoctorLogin):
    """Login and receive a JWT token."""
    doctor = get_doctor_by_username(credentials.username)

    if not doctor:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(credentials.password, doctor['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Create token containing the username
    token = create_access_token({"username": doctor['username']})

    return {
        "access_token": token,
        "token_type": "bearer",
        "doctor": doctor['full_name']
    }


# --- Protected Endpoints (login required) ---

@app.get("/me")
async def get_my_profile(current_doctor: dict = Depends(get_current_doctor)):
    """Returns the logged-in doctor's profile."""
    return {"doctor": current_doctor}


@app.get("/my-patients")
async def get_my_patients(current_doctor: dict = Depends(get_current_doctor)):
    """Returns ONLY the patients assigned to the logged-in doctor."""
    patients = get_patients_by_doctor(current_doctor['id'])
    return {"patients": patients, "count": len(patients)}


@app.post("/my-patients/assign")
async def assign_patient(
    body: AssignPatient,
    current_doctor: dict = Depends(get_current_doctor)
):
    """Assign an existing patient to the logged-in doctor."""
    patient = get_patient(body.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    assign_patient_to_doctor(body.patient_id, current_doctor['id'])
    return {"message": f"Patient {body.patient_id} assigned to Dr. {current_doctor['full_name']}"}


@app.get("/my-patients/{patient_id}")
async def get_my_patient_detail(
    patient_id: str,
    current_doctor: dict = Depends(get_current_doctor)
):
    """Get full details for one of the doctor's assigned patients."""
    # First verify this patient belongs to this doctor
    my_patients = get_patients_by_doctor(current_doctor['id'])
    patient_ids = [p['patient_id'] for p in my_patients]

    if patient_id not in patient_ids:
        raise HTTPException(status_code=403, detail="This patient is not assigned to you")

    readings = get_recent_readings(patient_id, limit=10)
    analysis = analyze_patient(patient_id)

    return {
        "patient": get_patient(patient_id),
        "latest_readings": readings,
        "current_status": analysis
    }


@app.get("/alerts")
async def get_alerts(current_doctor: dict = Depends(get_current_doctor)):
    """Get all unresolved alerts — protected, doctors only."""
    alerts = get_unresolved_alerts()
    return {"alerts": alerts, "count": len(alerts)}

@app.post("/patients")
async def create_patient(patient: PatientCreate):
    """Add a new patient."""
    add_patient(
        patient_id=patient.patient_id,
        name=patient.name,
        age=patient.age,
        condition=patient.condition,
        threshold_high=patient.threshold_high,
        threshold_low=patient.threshold_low,
    )
    return {"message": f"Patient {patient.name} added successfully"}

@app.get("/patients/{patient_id}")
async def get_patient_detail(patient_id: str):
    """Get one patient's info + their latest readings + current status."""
    patient = get_patient(patient_id)

    if not patient:
        raise HTTPException(status_code=404, details=f"Patient{patient_id} not found")
    
    readings = get_recent_readings(patient_id, limit=10)
    analysis = analyze_patient(patient_id)

    return {
        "patient": patient,
        "latest_readings": readings,
        "current_status": analysis
    }

@app.get("/patients/{patient_id}/readings")
async def get_readings(patient_id: str, limit: int = 20):
    """Get recent readings for a patient."""
    patient = get_patient(patient_id)

    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")
    readings = get_recent_readings(patient_id, limit=limit)
    return {"patient_id" : patient_id, "readings": readings}

@app.get("/alerts")
async def get_alerts():
    """Get all unresolved alerts — this is what the doctor checks."""
    alerts = get_unresolved_alerts()
    return {"alerts": alerts, "count": len(alerts)}


@app.get("/patients")
async def list_patients():
    """Get all patients."""
    patients = get_all_patients()
    return {"patients": patients}