DATABASE_PATH = 'data/health_data.db'

#set patient data thresholds instead of hard coding use high and low level values
GLUCOSE_THRESHOLD_HIGH = 180
GLUCOSE_THRESHOLD_LOW = 70

#when the next data must be generated 
SIMULATION_INTERVAL = 5 #5 sec bw each reading
NUM_PATIENTS = 3

#Alert Settings
ALERT_CHECK_INTERVAL = 10 #sec
CONSECUTIVE_HIGH_READINGS = 3 #3 high reading before alert

