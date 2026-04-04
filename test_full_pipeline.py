import time
from src.database import initialize_database, add_patient
from src.data_generator import simulate_all_patients
from src.alert_system import start_monitoring_in_background

initialize_database()

add_patient("P001", "Shruti", 33, "Type 1 Diabetes")
add_patient("P002", "Rahul", 27, "Prediabetes")
add_patient("P003", "Anita", 45, "Healthy")

patient_ids = ["P001", "P002", "P003"]

# Start the monitor in background FIRST
start_monitoring_in_background(patient_ids)

# Then start generating data (runs for 2 minutes)
simulate_all_patients(patient_ids, duration_minutes=2)