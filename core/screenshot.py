import logging
import os
import subprocess
import time
from datetime import datetime
from PIL import Image

from .db import Database
from .model import JinaClipModel
from .utils import (
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

        compress_image(filepath)

        logger.info(f"SCREENSHOT FILEPATH: {filepath}")
        return filepath
    # Gnome support to be added
    else:
        logger.error("Unknown session detected. Screenshot not possible.")
        exit(1)


def compress_image(filepath: str, quality: int = 65) -> None:
    """
    Compress the image file while retaining the PNG format.
    """
    compressed_filepath = filepath
    with Image.open(filepath) as img:
        img = img.convert("RGB")
        img.save(compressed_filepath, "PNG", optimize=True, quality=quality)
        logger.info(f"Compressed PNG image saved at {compressed_filepath}")


def service() -> None:
    db = Database()
    model = JinaClipModel()
    db.create_tables()
    interval: float = 1
    while True:
        logger.info("Capturing screenshot...")
        current_screenshot_path: str = capture()
        time.sleep(interval * 60)

        try:
            curr_img_emb = model.get_img_embs(Image.open(current_screenshot_path))
        except ValueError:
            logger.error("Error getting image embeddings.")
            exit(1)

        similarity = compare_with_prev_img(curr_img_emb)
        active_application_name = get_active_application_name()

        if similarity is not None:
            interval = modulate_interval(interval, similarity)
        else:
            logger.info("Similarity value was not returned. The database may be empty.")

        # Insert the entry into the database
        db.insert_entry(current_screenshot_path, curr_img_emb, active_application_name)

        logger.info(f"CURRENT INTERVAL is {interval}")


if __name__ == "__main__":
    service()
