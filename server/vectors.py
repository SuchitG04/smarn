import os

import numpy as np
import torch
from colpali_engine.models import ColPali, ColPaliProcessor
from PIL import Image
from transformers import AutoModel, BitsAndBytesConfig

model = None
processor = None
device = None


def load_model():
    """Loads the appropriate model and processor based on the system's hardware.

    - If a GPU is available:
        - Loads the colpali model with 8-bit quantization.
        - Retrieves the ColPali processor and assigns it
          to the `processor` variable, and the model is assigned to `model`.
        - The `device` variable is updated to "gpu".

    - If no GPU is available:
        - Loads the AutoModel from "jinaai/jina-clip-v1" and assigns it to `model`.
        - The `device` variable is updated to "cpu".
    """
    global model, processor, device
    if model is None:
        if torch.cuda.is_available():

            quantization_config = BitsAndBytesConfig(load_in_8bit=True)
            model_name = "vidore/colpali-v1.2"

            model = ColPali.from_pretrained(
                model_name,
                torch_dtype=torch.float16,
                device_map="cuda:0",
                quantization_config=quantization_config,
            ).eval()

            # ColPaliProcessor.from_pretrained will return (tuple[ColPaliProcessor, dict[str, Unknown]] | ColPaliProcessor)
            processor_or_tuple = ColPaliProcessor.from_pretrained(
                model_name, quantization_config=quantization_config
            )

            if isinstance(processor_or_tuple, tuple):
                processor = processor_or_tuple[0]
            else:
                processor = processor_or_tuple

            device = "gpu"
        else:
            model = AutoModel.from_pretrained(
                "jinaai/jina-clip-v1", trust_remote_code=True
            )
            device = "cpu"


def get_img_emb(path: str) -> np.ndarray:
    """Get embeddings for an image given an image path. Raises ValueError if image path is invalid."""
    if not os.path.exists(path):
        raise ValueError("Image path does not exist!")

    global model, processor, device
    load_model()
    if model is None or processor is None or device is None:
        raise ValueError("Model or processor was not loaded properly.")

    if device == "gpu":
        processed_image = processor.process_images([Image.open(path)]).to(model.device)
        image_embedding = model(**processed_image)
        return image_embedding.cpu().detach().numpy()

    # CPU
    return model.encode_image(path)


def get_text_emb(text: str) -> np.ndarray:
    """Get embeddings for text."""
    global model, processor, device
    load_model()
    if model is None or processor is None or device is None:
        raise ValueError("Model or processor was not loaded properly.")

    if device == "gpu":
        processed_text = processor.process_queries([text]).to(model.device)
        text_embedding = model(**processed_text)
        return text_embedding.cpu().detach().numpy()

    # CPU
    return model.encode_text(text)
