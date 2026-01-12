#STEP 1: imports
import sqlite3
from datetime import datetime
from config import DATABASE_PATH

#STEP 2: Creating a connection
def get_connection():
    """Creates and returns a db connection"""

    conn = sqlite3.connect(DATABASE_PATH)  
    #This makes queries return dict instead of tuples
    conn.row_factory = sqlite3.Row
    return conn

#STEP 3: Creating tables - patients and readings
def initialize_database():
    """Create tables if they dont exist"""
    conn = get_connection()
    cursor = conn.cursor()  #cursor? - pointer to execute cmds


    #patients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            condition TEXT,
            threshold_high REAL DEFAULT 180,
            threshold_low REAL DEFAULT 70
        )
    """)
    
    #readings table
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS readings(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   patient_id TEXT,
                   glucose_level NOT NULL,
                   timestamp TEXT NOT NULL,
                   FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
    """)

    conn.commit()  #This saves chngs
    conn.close()

    print("My first database initialization complete! (11-01-2026)")


#STEP 4: insert data
def add_patient(patient_id, name, age, condition, threshold_high=180, threshold_low=70):
    """
    Add new patient to db

      Args:
        patient_id: Unique identifier (e.g., "P001")
        name: Patient's name
        age: Patient's age
        condition: Medical condition (e.g., "Type 2 Diabetes")
        threshold_high: Upper glucose limit
        threshold_low: Lower glucose limit
    """

    conn = get_connection()
    cursor = conn.cursor()

    try: #try: attempt the operation
        #IMPORTANT: Using ? to prevent SQL injection attacks
        cursor.execute("""
            INSERT INTO patients (patient_id, name, age, condition, threshold_high, threshold_low)
            VALUES(?,?,?,?,?,?)
                       """, (patient_id, name, age, condition, threshold_high, threshold_low))
        
        conn.commit()
        print(f"Added patient: {name}")

    except sqlite3.IntegrityError: #except: handle a certain error
        #this might happen if patient exists
        print(f"Patient {patient_id} exists")

    finally: #finally: always run
        #IMPORTANT: Always close connection even if error occurs
        conn.close()

#STEP 5: Add readings
def add_reading(patient_id, glucose_level):
    """
    Records glucose reading for a patient

    Args:
        patient_id: Unique identifier for the patient
        glucose_level: Glucose reading value in mg/dL
    """
    conn = get_connection()
    cursor = conn.cursor()

    #this auto generates timestamp
    #datetime.now(): Gets current time
    #.isoformat(): Converts to string like "2026-01-11T14:30:00"
    timestamp = datetime.now().isoformat() 

    cursor.execute("""
        INSERT INTO readings (patient_id, glucose_level, timestamp)
        VALUES (?,?,?)
    """, (patient_id, glucose_level, timestamp))
    
    conn.commit()
    conn.close()

#STEP 6: Retriving data
def get_recent_reading(patient_id, limit=10):
    """
    Get most recent readings of a patient
    Args:
        patient_id: Unique identifier for the patient
        limit: Number of recent readings to retrieve

    Return:
        List of recent readings as dictionaries
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
            SELECT glucose_level, timestamp
            FROM readings
            WHERE patient_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
    """, (patient_id, limit))   

    #Fetch all results
    rows = cursor.fetchall()

    #convert list of dictionaries
    readings = []
    for row in rows:
        readings.append({
            'glucose_level': row['glucose_level'],
            'timestamp': row['timestamp']
        })    

    conn.close()
    return readings




