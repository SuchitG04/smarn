import os
import struct
import subprocess
import numpy as np

from .db import Database
from .vectors import get_img_emb

CMP_THRESHOLD = 0.85

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


def compare_with_prev_img(curr_img: str) -> tuple[bool, np.ndarray | None]:
    """
    Compares a given image to the last entry in the DB.

    Args:
        curr_img (str): The image to compare with the last entry.
    Returns:
        np.ndarray : The image embeddings if the similarity is not above the threshold.

    Note: Returns True if the images are same, None if there's no prev image, and the embedding if they are not similar.
    """
    last_entry = Database().get_last_entry()
    if last_entry is None:
        return False, None
    curr_img_emb = get_img_emb(curr_img)
    last_entry_emb = deserialize(last_entry[0])
    similarity = cosine_similarity(curr_img_emb, last_entry_emb)

    if similarity > CMP_THRESHOLD:
        return True, curr_img_emb, similarity
    else:
        return False, curr_img_emb, similarity


def identify_session() -> str:
    """
    Identify the current display server session.

    Returns:
        str: "X" if the session is X11, "W" if the session is Wayland.
    """
    if "WAYLAND_DISPLAY" in os.environ:
        return "W"
    elif "DISPLAY" in os.environ:
        return "X"
    else:
        raise ValueError("Unknown session type")


def get_active_application_name_x11() -> str:
    """
    Get the name of the active application from X11 using `xprop`.

    Returns:
        str: The name of the active application (window class) in an X11 session.
    """
    try:
        window_id_output = subprocess.run(
            ["xprop", "-root", "_NET_ACTIVE_WINDOW"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

        # Extract the window ID
        window_id = window_id_output.split()[-1]

        wm_class_output = subprocess.run(
            ["xprop", "-id", window_id, "WM_CLASS"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

        # Extract the window class name
        wm_class = wm_class_output.split("=")[1].strip().replace('"', "").split(", ")[0]

        return wm_class

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to retrieve window information from X11: {e}")
    except IndexError as e:
        raise RuntimeError(f"Unexpected output format from xprop command: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")


# TODO: Implement this function to handle wayland applications
def get_active_application_name_wayland() -> str:
    """
     Get the name of the active application on Wayland.

    Returns:
        str: The name of the active application in a Wayland session.
    """
    return ""


def get_active_application_name() -> str:
    """
    Get the name of the active application, depending on the display server.

    Returns:
        str: The name of the active application for X11 or Wayland.
    """
    session = identify_session()
    if session == "W":
        try:
            # Try to get the application name using X11 function to check if it's running on XWayland
            return get_active_application_name_x11()
        except RuntimeError:
            print("Functionality not implemented yet.")
            return get_active_application_name_wayland()
    elif session == "X":
        return get_active_application_name_x11()
    else:
        raise ValueError("Unknown session type")

def modulate_interval(interval: float, cosine_similarity: float) -> float:
    """
    Modulates the interval dynamically based on the cosine similarity value.

    Args:
        interval: The interval to be modulated
        cosine_similarity: The cosine similarity value between image embeddings.
    Returns:
        interval: Modulated interval (necessarily not the different in value as the interval argument)
    """
    delta = 0.15  # The change in interval
    # Ensure interval remains between 0.25 and 5
    if 0.25 <= interval <= 5:
        if cosine_similarity > 0.9:  
            interval = min(5, interval + delta) # High similarity, increase interval
        elif cosine_similarity < 0.6:  
            interval = max(0.25, interval - delta) # Low similarity, decrease interval
    return interval