import os
import subprocess
import time
from datetime import datetime
from screenshot import capture, identify_session
from utils import compare_with_prev_img

rate = 0.5

def smarn():
    while True:
        capture(identify_session())
        time.sleep(rate * 60)

if __name__ == "__main__":
    smarn()