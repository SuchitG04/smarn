import os
import subprocess
import time
from datetime import datetime
from screenshot import capture

rate = 120

def identify_session() -> str:
    if "WAYLAND_DISPLAY" in os.environ:
        return "W"
    elif "DISPLAY" in os.environ:
        return "X"
    else:
        raise ValueError("Unknown session type")

if __name__ == "__main__":
    while True:
        capture(identify_session(), is_gnome_desktop())
        time.sleep(rate)