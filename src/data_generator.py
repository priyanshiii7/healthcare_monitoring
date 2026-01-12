import random #to add randomness as glucose level fluctuate throughout the day
import time #to add delay bw readings
from datetime import datetime
from database import add_reading
import threading

#import settings
from config import(
    GLUCOSE_THRESHOLD_HIGH,
    GLUCOSE_THRESHOLD_LOW,
    SIMULATION_INTERVAL,
)
#1 generate a reading
def generate_glucose_reading(patient_id, is_diabetic=True):
    """
    Generate a glucose reading for a patient
    Args:
        patient_id: Which patient this reading is for
        is_diabetic: If True, wider variation and occasional spikes
    
    Returns:
        float: Glucose level in mg/dL

    """

    #base glucose level
    if is_diabetic:
        base_level = random.uniform(90, 160) #diabetics have less stable glucose
    else:
        base_level = random.uniform(80, 120) #non stay in tighter range

    variation = random.uniform(-20, 20)
    glucose_level = base_level + variation

    if random.random() < 0.1:
        # Returns: 0.0 to 1.0
        # If result is 0.05 → 0.05 < 0.1 → True (spike!)
        # If result is 0.87 → 0.87 < 0.1 → False (no spike)
        glucose_level += random.uniform(30, 60)

    glucose_level = round(glucose_level, 1) #round to 1 decimal 
    return glucose_level


#2 Simulate continuous data generation
def simulate_patient_readings(patient_id, duration_minutes= 60):
    """
    Continuously generates readings for a patient.
    
    Args:
        patient_id: Which patient to simulate
        duration_minutes: How long to run (in minutes)
    """
    print(f"Starting simulation for {patient_id}")
    # Calculate how many readings to generate
    # If interval is 5 seconds and duration is 60 minutes:
    # 60 minutes = 3600 seconds
    # 3600 / 5 = 720 readings

    total_readings = (duration_minutes * 60) // SIMULATION_INTERVAL
    for i in range(total_readings):
        #generate reading
        glucose = generate_glucose_reading(patient_id, is_diabetic=True)
        #save to db
        add_reading(patient_id, glucose)
        timestamp = datetime.now().strftime("%H:%M:%S") #string format time
        print(f"[{timestamp}] {patient_id}: {glucose} mg/dL")

        #wait before next reading
        time.sleep(SIMULATION_INTERVAL) #pauses execution
        #creates an issue - this code is sequential cant take readings for 2 or more patients together
        #sol? threading - run multiple simultaneously

def simulate_all_patients(patient_ids, duration_minutes= 60):
    """
    Simulates multiple patients simultaneously.
    
    Args:
        patient_ids: List of patient IDs to simulate
        duration_minutes: How long to run
    """
    
    threads = []

    #create a thread for each patient
    
