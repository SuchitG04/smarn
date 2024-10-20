import logging
import os

import numpy as np
from colpali_engine import ColPaliProcessor
from models import State
from PIL import Image
from transformers import PreTrainedModel

logger = logging.getLogger(__name__)


def get_img_emb(state: State, path: str) -> np.ndarray:
    """Get embeddings for an image given an image path. Raises ValueError if image path is invalid."""
    model: PreTrainedModel = state["model"]  # type: ignore
    processor: ColPaliProcessor = state["processor"]  # type: ignore
    device: str = state["device"]  # type: ignore

    if not os.path.exists(path):
        raise ValueError("Image path does not exist!")

    if device == "gpu":
        processed_image = processor.process_images([Image.open(path)]).to(model.device)
        image_embedding = model(**processed_image)
        return image_embedding.cpu().detach().numpy()

    # CPU
    logger.info("Image embedding retrieved.")
    return model.encode_image(path)


def get_text_emb(state: State, text: str) -> np.ndarray:
    """Get embeddings for text."""
    model: PreTrainedModel = state["model"]  # type: ignore
    processor: ColPaliProcessor = state["processor"]  # type: ignore
    device: str = state["device"]  # type: ignore

    if device == "gpu":
        processed_text = processor.process_queries([text]).to(model.device)
        text_embedding = model(**processed_text)
        return text_embedding.cpu().detach().numpy()

    # CPU
    logger.info("Text embedding retrieved.")
    return model.encode_text(text)
