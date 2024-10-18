import os
import subprocess
from datetime import datetime

import logging

from .utils import identify_session

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
            logger.error("grim was not found on this system. Error capturing screenshot.")
            exit(1)
        return filepath
    elif session_type == "X":  # X11 session requires maim
        try:
            subprocess.run(["maim", filepath], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error executing maim: {e}")
            exit(1)
        except FileNotFoundError:
            logger.error("maim was not found on this system. Error capturing screenshot.")
            exit(1)
        logger.info(f"SCREENSHOT FILEPATH: {filepath}")
        return filepath
    # Gnome support to be added
    else:
        logger.error("Unknown session detected. Screenshot not possible.")
        exit(1)
