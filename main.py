import os
import subprocess
import time
from datetime import datetime
from screenshot import capture, identify_session

rate = 120

if __name__ == "__main__":
    while True:
        capture(identify_session(), is_gnome_desktop())
        time.sleep(rate)