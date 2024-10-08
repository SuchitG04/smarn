import numpy as np
import struct

from vectors import get_img_emb
from db import Database

db = Database("test.sqlite")
CMP_THRESHOLD = 0.9

# TODO: Evaluate if this file is necessary and if the functions can be moved elsewhere.

def deserialize(serialized_data: bytes) -> np.ndarray:
    """Deserializes raw bytes back into a numpy array."""
    num_floats = len(serialized_data) // struct.calcsize('f')  # number of floats
    return np.array(list(struct.unpack(f'{num_floats}f', serialized_data)))

def compare_with_prev_img(curr_img: str) -> bool:
    """
    Compares a given image to the last entry in the DB.
    Returns (True, img_emb) if the images are same, (False, None) otherwise.
    """
    last_entry = db.get_last_entry()
    if last_entry is None:
        return False, None
    curr_img_emb = get_img_emb(curr_img)
    last_entry_emb = deserialize(last_entry[0])
    similarity = np.dot(curr_img_emb, last_entry_emb)
    if similarity > CMP_THRESHOLD:
        return True
    else:
        return False
