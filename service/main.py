import time
import numpy as np

import logging
import log_config

from .db import Database
from .screenshot import capture
from .utils import compare_with_prev_img, get_active_application_name, modulate_interval

logger = logging.getLogger(__name__)

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
        if isinstance(curr_emb[0], np.ndarray):
            Ddb.insert_entry(current_screenshot_path, active_application_name, curr_emb[0])
            interval = modulate_interval(interval, curr_emb[1])
        else:
            Ddb.insert_entry(current_screenshot_path, active_application_name)
            logger.info("Database was found to be empty. No comparison initiated.")

        logger.info(f"CURRENT INTERVAL is {interval}")

if __name__ == "__main__":
    smarn()