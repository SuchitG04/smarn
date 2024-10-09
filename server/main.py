import time

from db import Database
from screenshot import capture
from utils import compare_with_prev_img, get_active_application_name

rate: float = 2.0


def smarn():
    global rate
    Ddb = Database()
    while True:
        current_screenshot_path: str = capture()
        time.sleep(rate * 60)

        if curr_emb := compare_with_prev_img(current_screenshot_path):
            if rate >= 5:
                rate += 0.5
        else:
            if rate <= 2:
                rate -= 0.5
        
        # inserting images into database
        active_application_name = get_active_application_name()
        Database.insert_entry(current_screenshot_path, active_application_name)

if __name__ == "__main__":
    smarn()
