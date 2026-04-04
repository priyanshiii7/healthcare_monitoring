from src.database import initialize_database, add_patient, add_reading
from src.analyzer import analyze_patient

initialize_database()

# Add a test patient
add_patient("TEST01", "Test Patient", 40, "Type 2 Diabetes")

# Simulate 3 consecutive high readings
print("--- Adding 3 high readings ---")
add_reading("TEST01", 210)
add_reading("TEST01", 195)
add_reading("TEST01", 220)

result = analyze_patient("TEST01")
print(f"Status: {result['status']}")
print(f"Message: {result['message']}")
print(f"Should Alert: {result['should_alert']}")

print("\n--- Adding a normal reading ---")
add_reading("TEST01", 110)

result = analyze_patient("TEST01")
print(f"Status: {result['status']}")
print(f"Message: {result['message']}")
