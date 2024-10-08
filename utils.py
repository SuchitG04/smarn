import numpy as np
import struct

from vectors import get_img_emb
from db import Database

db = Database("test.sqlite")
CMP_THRESHOLD = 0.9

# TODO: Evaluate if this file is necessary and if the functions can be moved elsewhere.

def deserialize(serialized_data: bytes) -> np.ndarray:
    """
    Deserializes raw bytes back into a numpy array.

    Args:
        serialized_data (bytes): Raw bytes from database.
    Returns:
        np.ndarray: Deserialized numpy array.
    """
    num_floats = len(serialized_data) // struct.calcsize('f')  # number of floats
    return np.array(list(struct.unpack(f'{num_floats}f', serialized_data)))

def compare_with_prev_img(curr_img: str) -> np.ndarray | None:
    """
    Compares a given image to the last entry in the DB.

    Args:
        curr_img (str): The image to compare with the last entry.
    Returns:
        None: If the images are same.
        np.ndarray: The image embeddings otherwise.
    """
    last_entry = db.get_last_entry()
    if last_entry is None:
        return False, None
    curr_img_emb = get_img_emb(curr_img)
    last_entry_emb = deserialize(last_entry[0])
    similarity = np.dot(curr_img_emb, last_entry_emb)
    if similarity > CMP_THRESHOLD:
        return None
    else:
        return curr_img_emb
