import sys
import os

def get_path():
    try:
        d=sys._MEIPASS
        return d
    except:
        return os.path.dirname(os.path.abspath(__file__))
    
#print(get_path())