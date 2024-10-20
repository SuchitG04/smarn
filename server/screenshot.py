import logging
import os
import subprocess
import time
from datetime import datetime

import numpy as np
from db import Database
from utils import (
    compare_with_prev_img,
    get_active_application_name,
    identify_session,
    modulate_interval,
)

logger = logging.getLogger(__name__)


def capture() -> str:
    """
    A function that captures a screenshot (maim for X11 and grim for Wayland) and returns the path of the screenshot.
    """
    session_type = identify_session()

    smarn_dir = os.path.dirname(os.path.abspath(__file__))
    screenshots_dir = os.path.join(smarn_dir, "screenshots")

    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"smarn_{timestamp}.png"
    filepath = os.path.join(screenshots_dir, filename)

    if session_type == "W":  # Wayland session requires grim
        try:
            subprocess.run(["grim", filepath], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error executing grim: {e}")
            exit(1)
        except FileNotFoundError:
            logger.error(
                "grim was not found on this system. Error capturing screenshot."
            )
            exit(1)
        return filepath
    elif session_type == "X":  # X11 session requires maim
        try:
            subprocess.run(["maim", filepath], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error executing maim: {e}")
            exit(1)
        except FileNotFoundError:
            logger.error(
                "maim was not found on this system. Error capturing screenshot."
            )
            exit(1)
        logger.info(f"SCREENSHOT FILEPATH: {filepath}")
        return filepath
    # Gnome support to be added
    else:
        logger.error("Unknown session detected. Screenshot not possible.")
        exit(1)


def service():
    Ddb = Database()
    Ddb.create_tables()
    interval: float = 1
    while True:
        current_screenshot_path: str = capture()
        time.sleep(interval * 60)

        curr_emb = compare_with_prev_img(current_screenshot_path)
        active_application_name = get_active_application_name()

        # if the current embedding is an array, insert it into the database
        if isinstance(curr_emb[0], np.ndarray):
            Ddb.insert_entry(
                current_screenshot_path, active_application_name, curr_emb[0]
            )
            if curr_emb[1] is not None:
                interval = modulate_interval(interval, curr_emb[1])
            else:
                logger.error("Similarity value was not returned.")
        else:
            Ddb.insert_entry(current_screenshot_path, active_application_name)
            logger.info("Database was found to be empty. No comparison initiated.")

        logger.info(f"CURRENT INTERVAL is {interval}")
