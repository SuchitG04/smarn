import time
import numpy as np

from .db import Database
from .screenshot import capture
from .utils import compare_with_prev_img, get_active_application_name, modulate_interval

interval: float = 1

def smarn():
    global interval
    Ddb = Database()
    Ddb.create_tables()
    while True:
        current_screenshot_path: str = capture()
        time.sleep(interval * 60)

        curr_emb = compare_with_prev_img(current_screenshot_path)
        active_application_name = get_active_application_name()

        # if the current embedding is an array, insert it into the database
        if isinstance(curr_emb[1], np.ndarray):
            Ddb.insert_entry(
                current_screenshot_path, active_application_name, curr_emb[1]
            )
            # check if the interval has to be altered
            interval = modulate_interval(interval, curr_emb[2])
        # do nothing if the database is empty
        else:
            Ddb.insert_entry(current_screenshot_path, active_application_name)
            print("Database is empty.")

        print("INTERVAL: ", interval)

if __name__ == "__main__":
    smarn()