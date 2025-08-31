import logging
import os
import struct
import subprocess

import numpy as np

from .db import Database

logger = logging.getLogger(__name__)


# TODO: Evaluate if this file is necessary and if the functions can be moved elsewhere.
def deserialize(serialized_data: bytes) -> np.ndarray:
    """
    Deserializes raw bytes back into a numpy array.

    Args:
        serialized_data (bytes): Raw bytes from database.
    Returns:
        np.ndarray: Deserialized numpy array.
    """
    num_floats = len(serialized_data) // struct.calcsize("f")  # number of floats
    return np.array(list(struct.unpack(f"{num_floats}f", serialized_data)))


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Computes the cosine similarity of two vectors.

    Args:
        vec1 (np.ndarray): The first vector.
        vec2 (np.ndarray): The second vector.
    Returns:
        float: The cosine similarity of two vectors.
    """
    vec1_norm = np.linalg.norm(vec1)
    vec2_norm = np.linalg.norm(vec2)

    if vec1_norm == 0 or vec2_norm == 0:
        return 0.0

    return np.dot(vec1, vec2) / (vec1_norm * vec2_norm)


def compare_with_prev_img(
    curr_img_emb: np.ndarray,
) -> float | None:
    """
    Compares a given image to the last entry in the DB.

    Args:
        curr_img_emb (np.ndarray): The image emb to compare with the last entry.
    Returns:
        float | None: The cosine similarity between the current image and the last entry.
    """
    last_entry = Database().get_last_entry()

    if last_entry is None:
        logger.debug("No last entry detected.")
        return None

    last_entry_emb = deserialize(last_entry[0])

    similarity = cosine_similarity(curr_img_emb, last_entry_emb)

    return similarity


def identify_session() -> str:
    """
    Identify the current display server session.

    Returns:
        str: "X" if the session is X11, "W" if the session is Wayland.
    """
    if "WAYLAND_DISPLAY" in os.environ:
        logger.info("Wayland display server detected.")
        return "W"
    elif "DISPLAY" in os.environ:
        logger.info("X11 display server detected.")
        return "X"
    else:
        raise ValueError("Unknown session type")


def get_active_application_name() -> str:
    """
    Get the name of the active application.

    Returns:
        str: The name of the active application for X11 or XWayland.
    """
    try:
        application_name = subprocess.run(
            ["xdotool", "getactivewindow", "getwindowclassname"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

        logger.info(f"{application_name} detected")
        return application_name
    except subprocess.CalledProcessError:
        logger.error("Failed to get the active application name.")
        return ""


def modulate_interval(interval: float, cosine_similarity: float) -> float:
    """
    Modulates the interval dynamically based on the cosine similarity value.

    Args:
        interval: The interval to be modulated
        cosine_similarity: The cosine similarity value between image embeddings.
    Returns:
        interval: Modulated interval (necessarily not the different in value as the interval argument)
    """
    delta = 0.25  # The change in interval
    # Ensure interval remains between 0.25 and 5
    if 0.25 <= interval <= 5:
        if cosine_similarity > 0.95:
            interval = min(5, interval + delta)  # High similarity, increase interval
            logger.info(f"High similarity; Increasing interval by {delta} minutes")
        elif cosine_similarity < 0.8:
            interval = max(0.25, interval - delta)  # Low similarity, decrease interval
            logger.info(f"Low similarity; Decreasing interval by {delta} minutes")

    return interval


if __name__ == "__main__":
    print(get_active_application_name())
