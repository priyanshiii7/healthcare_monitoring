from src.database import initialize_database, add_patient
from src.data_generator import simulate_all_patients

initialize_database()
add_patient("P001", "Shruti", 33, "type 1 Diabetes")
add_patient("P002", "Rahul", 27, "Prediabetes")
add_patient("P003", "Anita", 45, "Healthy")

# Simulate for 1 minute (will generate 12 readings per patient)
# With 5-second intervals: 60 seconds / 5 = 12 readings each
patient_ids = ["P001", "P002", "P003"]
simulate_all_patients(patient_ids, duration_minutes=1)
print("/n Simulation Completed")