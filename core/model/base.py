from abc import ABC, abstractmethod

import numpy as np
from PIL import Image


class BaseModel(ABC):
    """Abstract base class for a generic model."""

    @abstractmethod
    def get_text_embs(self, text: str) -> np.ndarray:
        """
        Get the text embeddings for a given text.

        Args:
            text (str): The text to get the embeddings for.

        Returns:
            np.ndarray: The text embeddings.
        """
        pass

    @abstractmethod
    def get_img_embs(self, img: Image.Image) -> np.ndarray:
        """
        Get the image embeddings for a given image.

        Args:
            img (Image.Image): The image to get the embeddings for.

        Returns:
            np.ndarray: The image embeddings.
        """
        pass
