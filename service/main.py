import time
import numpy as np

from .db import Database
from .screenshot import capture
from .utils import compare_with_prev_img, get_active_application_name

rate: float = 1
interval: float = 0.5


def smarn():
    global rate, interval
    Ddb = Database()
    Ddb.create_tables()
    while True:
        current_screenshot_path: str = capture()
        time.sleep(rate * 60)

        curr_emb = compare_with_prev_img(current_screenshot_path)
        active_application_name = get_active_application_name()

        # if the current embedding is an array, insert it into the database
        if isinstance(curr_emb[1], np.ndarray):
            Ddb.insert_entry(
                current_screenshot_path, active_application_name, curr_emb[1]
            )
            # check if the rate has to be altered
            # TODO: fix issue of rate stuck at 0.5
            if rate in range(1, 5):
                if curr_emb[0]:
                    rate += interval
                    # rate = min(5, rate + interval)
                else:
                    rate -= interval
                    # rate = max(1, rate - interval)
        # do nothing if the database is empty
        else:
            Ddb.insert_entry(current_screenshot_path, active_application_name)
            print("Database is empty.")

        print("RATE: ", rate)


if __name__ == "__main__":
    smarn()
