import os
from typing import Optional

import numpy as np
from transformers import AutoModel

model = AutoModel.from_pretrained("jinaai/jina-clip-v1", trust_remote_code=True)


def get_img_emb(path: str) -> Optional[np.ndarray]:
    if not os.path.exists(path):
        print("Image path does not exist!")
        return None

    return model.encode_image(path)


def get_text_emb(text: str) -> np.ndarray:
    return model.encode_text(text)


def get_dot_product(img_emb: np.ndarray, text_emb: np.ndarray) -> float:
    return float(text_emb @ img_emb.T)


if __name__ == "__main__":
    img_emb = get_img_emb("smarn_screenshots/keeb.jpg")
    text_emb = get_text_emb("keyboard")

    if img_emb:
        print(get_dot_product(img_emb, text_emb))

