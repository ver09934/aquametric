import os

class Config:
    
    TESTING = True
    DEBUG = True

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    SENSOR_CONFIG = os.path.join(BASE_DIR, "sensors.json")
    LIVE_CONFIG = os.path.join(BASE_DIR, "liveconf.json")
