import sqlite3
from config import (
    DATABASE_PATH,
    GLUCOSE_THRESHOLD_HIGH,
    GLUCOSE_THRESHOLD_LOW,
    CONSECUTIVE_HIGH_READINGS
)

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_latest_readings(patient_id, count):
    """
    Fetches the last `count` readings for a patient.
    Returns a list of glucose levels (just the numbers), newest first.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT glucose_level
        FROM readings
        WHERE patient_id = ?
        ORDER BY timestamp DESC
        LIMIT ?          
    """, (patient_id, count))

    rows = cursor.fetchall()
    conn.close()

    # Extract just the glucose numbers into a plain list
    # row['glucose_level'] works because of row_factory = sqlite3.Row
    return [row['glucose_level']for row in rows]

def is_critically_high(glucose_level):
    """Single reading is dangerously high."""
    return glucose_level > GLUCOSE_THRESHOLD_HIGH

def is_critically_low(glucose_level):
    """Single reading is dangerously low. Low is actually more dangerous than high."""
    return glucose_level < GLUCOSE_THRESHOLD_LOW

def has_consecutive_high_readings(patient_id):
    """
    Returns True if the last CONSECUTIVE_HIGH_READINGS readings are ALL high.
    This filters out random spikes.
    """
    readings = get_latest_readings(patient_id, CONSECUTIVE_HIGH_READINGS)

    # Edge case: if patient has fewer readings than required, cant judge yet
    if len(readings) < CONSECUTIVE_HIGH_READINGS:
        return False
    
    # Check if EVERY reading in the list is above threshold
    # all() returns True only if every item passes the condition
    return all(level > GLUCOSE_THRESHOLD_HIGH for level in readings)

def analyze_patient(patient_id):
    """
    Main function. Analyzes a patient and returns a dict describing their status.

    Returns:
        dict with keys:
            - status: 'critical_high', 'critical_low', 'warning_high', 'normal'
            - latest_reading: most recent glucose level
            - message: human readable description
            - should_alert: True/False
    """

    readings = get_latest_readings(patient_id, CONSECUTIVE_HIGH_READINGS)
    #Edge case: no readings
    if not readings:
        return {
            'status' : 'no_data',
            'latest_reading' : None,
            'message' : 'No readings yet',
            'should alert': False
        }
    
    latest = readings[0]

    # Check low first — hypoglycemia is more immediately dangerous
    if is_critically_low(latest):
        return{
            'status' : 'critical_low',
            'latest_reading': latest,
            'message': f'CRITICAL: Glucose is dangerously low at {latest} mg/dl.',
            'should_alert' : True
        }

    if has_consecutive_high_readings(patient_id):
        return{
            'status' : 'critical_high',
            'latest_reading' : latest,
            'message' : f'ALERT: Glucose has been high for {CONSECUTIVE_HIGH_READINGS} consecutive readings.Latest: {latest} mg/dl',
            'should_alert': True
        }                          
    if is_critically_high(latest):
        return {
            'status' : 'warning_high',
            'latest_reading' : latest,
            'message' : f'WARNING: Glucose is elevated at {latest} mg/dl.Monitoring...',
            'should_alert' : False
        }
    
    return {
        'status' : 'normal',
        'latest_reading' : latest,
        'message' : f'Glucose level is normal at {latest} mg/dl.',
        'should_alert' : False
    }