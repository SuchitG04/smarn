import logging
import os

import numpy as np
from models import device, model, processor
from PIL import Image

logger = logging.getLogger(__name__)


def get_img_emb(path: str) -> np.ndarray:
    """Get embeddings for an image given an image path. Raises ValueError if image path is invalid."""
    if not os.path.exists(path):
        raise ValueError("Image path does not exist!")

    if device == "gpu" and (model is None or processor is None or device is None):
        raise ValueError("Model or processor was not loaded properly.")
    if device == "cpu" and (model is None or device is None):
        raise ValueError("Model was not loaded properly.")

    if device == "gpu":
        processed_image = processor.process_images([Image.open(path)]).to(model.device)
        image_embedding = model(**processed_image)
        return image_embedding.cpu().detach().numpy()

    # CPU
    logger.info("Image embedding retrieved.")
    return model.encode_image(path)


def get_text_emb(text: str) -> np.ndarray:
    """Get embeddings for text."""
    if model is None or processor is None or device is None:
        raise ValueError("Model or processor was not loaded properly.")

    if device == "gpu":
        processed_text = processor.process_queries([text]).to(model.device)
        text_embedding = model(**processed_text)
        return text_embedding.cpu().detach().numpy()

    # CPU
    logger.info("Text embedding retrieved.")
    return model.encode_text(text)
