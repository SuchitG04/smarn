import numpy as np
import os

from transformers import AutoModel

model = AutoModel.from_pretrained("jinaai/jina-clip-v1", trust_remote_code=True)


def get_img_emb(path: str) -> np.ndarray:
    if not os.path.exists(path):
        raise ValueError("Image path does not exist!")
    return model.encode_image(path)

def get_text_emb(text: str) -> np.ndarray:
    return model.encode_text(text)
