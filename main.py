import os
import subprocess
import time
from datetime import datetime
from screenshot import capture, identify_session
from utils import compare_with_prev_img
from db import Database

rate: float = 2.0

def smarn():
    db = Database("vectors.sqlite")
    while True:
        current_screenshot_path = capture(identify_session())
        time.sleep(rate * 60)

        if curr_emb := compare_with_prev_img(current_screenshot_path):
            if rate >= 5:
                rate += 0.5
        else:
            if rate <= 2:
                rate -= 0.5

if __name__ == "__main__":
    smarn()