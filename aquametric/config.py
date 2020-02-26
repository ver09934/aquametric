import os

# TODO: Use environment variables for data dir name, etc.

class Config:
    
    TESTING = True
    DEBUG = True

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
