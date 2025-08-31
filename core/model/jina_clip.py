import logging

import numpy as np
from PIL import Image
from transformers import AutoModel, PreTrainedModel

from .base import BaseModel

logger = logging.getLogger(__name__)


class JinaClipModel(BaseModel):
    """Jina-CLIP model implementation."""

    def __init__(self):
        self.model: PreTrainedModel | None = None
        self._load_model()

    def _load_model(self) -> None:
        """Load the model if it hasn't been loaded yet."""
        if self.model is None:
            logger.info("Loading Pretrained JinaAI from Huggingface Transformers.")
            try:
                self.model = AutoModel.from_pretrained(
                    "jinaai/jina-clip-v1", trust_remote_code=True
                )
            except (RuntimeError, OSError) as e:
                logger.debug(f"There was an error in loading the model - {e}")

            if self.model is None:
                logger.error("Model was not loaded properly.")
                exit(1)

    def get_text_embs(self, text: str) -> np.ndarray:
        """
        Get the text embeddings for a given text.

        Args:
            text (str): The text to get the embeddings for.

        Returns:
            np.ndarray: The text embeddings.
        """
        text_embs = self.model.encode_text([text])
        return text_embs

    def get_img_embs(self, img: Image.Image) -> np.ndarray:
        """
        Get the image embeddings for a given image.

        Args:
            img (Image.Image): The image to get the embeddings for.

        Returns:
            np.ndarray: The image embeddings.
        """
        img_embs = self.model.encode_image([img])
        return img_embs
