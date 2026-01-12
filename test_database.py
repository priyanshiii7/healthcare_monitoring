from src.database import initialize_database, add_patient, add_reading, get_recent_reading

#1. initialize
initialize_database()

#add test patient
add_patient("P1", "Voldemort", 78, "Type 2 Diabetes")

#add readings
add_reading("P1", 120)
add_reading("P1", 190)
add_reading("P1", 220)

#fetch recent readings
readings = get_recent_reading("P1")
print("Recent readings: ")
for r in readings:
    print(f" {r['timestamp']}: {r['glucose_level']} mg/dL")
