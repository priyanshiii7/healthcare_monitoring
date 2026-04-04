import time
import threading
from datetime import datetime

from src.database import save_alert, get_unresolved_alerts
from src.analyzer import analyze_patient
from config import ALERT_CHECK_INTERVAL
from typing import List

def send_alert(patient_id: str, analysis_result: dict) -> None:
    """
    Right now this just prints and saves to database.
    Later this becomes: send push notification to doctor's phone.

    Args:
        patient_id: Which patient triggered the alert
        analysis_result: The dict returned by analyze_patient()
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n [{timestamp}] ALERT for {patient_id}")
    print(f"   Status: {analysis_result['status']}")
    print(f"   {analysis_result['message']}")
    print(f"   Saved to database for doctor review.\n")

    save_alert(
        patient_id=patient_id,
        status=analysis_result['status'],
        message=analysis_result['message'],
        glucose_level=analysis_result['latest_reading']
    )

def check_patient(patient_id: str) -> None:
    """
    Runs the analyzer for one patient and sends alert if needed.
    """
    result = analyze_patient(patient_id)
    if result['should_alert']:
        send_alert(patient_id, result)
    else:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {patient_id}: {result['status']} - {result['latest_reading']}")

def monitor_patients(patient_ids: List[str]) -> None:
    """
    Runs continuously, checking all patients every ALERT_CHECK_INTERVAL seconds.
    This is the background worker that runs alongside data generation.

    Think of this as the 'brain' that never sleeps — 
    while doctors are off duty, this keeps watching.
    """
    print(f"Monitoring started for: {patient_ids}")
    print(f"   Checking every {ALERT_CHECK_INTERVAL} seconds...\n")

    while True:
        for patient_id in patient_ids:
            check_patient(patient_id)
        time.sleep(ALERT_CHECK_INTERVAL)

def start_monitoring_in_background(patient_ids: List[str]) -> threading.Thread:
    """
    Starts the monitor in a background thread so it doesn't block
    the data generator from running at the same time.
    """
    thread = threading.Thread(
        target=monitor_patients,
        args=(patient_ids,),
        daemon=True  # daemon=True means: stop this thread when main program exits
    )
    thread.start()
    return thread

