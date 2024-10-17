"""
Loads the appropriate model and processor based on the system's hardware.

 - If a GPU is available:
     - Loads the colpali model with 8-bit quantization.
     - Retrieves the ColPali processor and assigns it
         to the `processor` variable, and the model is assigned to `model`.
     - The `device` variable is updated to "gpu".

 - If no GPU is available:
     - Loads the AutoModel from "jinaai/jina-clip-v1" and assigns it to `model`.
     - The `device` variable is updated to "cpu".
     - The `processor` variable is not assigned as it is not required for the CPU model.
"""

import torch

import logging

from .colpali import load_gpu_model
from .jina_clip import load_cpu_model

logger = logging.getLogger(__name__)

model = None
processor = None
device = None
REQUIRED_MEMORY = 7.0

def get_gpu_vram():
    """
    Returns the total VRAM available on the GPU in GB.
    """
    logger.info("VRAM GPU retrieval initiated.")
    return torch.cuda.get_device_properties(torch.device("cuda:0")).total_memory / (
        1024**3
    )

if model is None:
    try:
        if torch.cuda.is_available() and get_gpu_vram() > REQUIRED_MEMORY:
            model, processor = load_gpu_model()            
            device = "gpu"
            logger.info("A GPU was detected on this device.")
        else:
            model = load_cpu_model()
            device = "cpu"
            logger.info("A CPU was detected on this device.")
    except (RuntimeError, OSError) as e:
        logger.debug("There was an error in loading the model - {e}")