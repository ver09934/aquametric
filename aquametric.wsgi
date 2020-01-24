import sys
import os

path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path)

from aquametric import create_app
application = create_app()
