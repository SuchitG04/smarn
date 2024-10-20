import logging
from typing import Optional, TypedDict

import torch

from .colpali import ColPaliProcessor, load_gpu_model
from .jina_clip import PreTrainedModel, load_cpu_model

logger = logging.getLogger(__name__)

REQUIRED_MEMORY = 7.0


def get_gpu_vram() -> float:
    """
    Returns the total VRAM available on the GPU in GB.
    """
    logger.info("VRAM GPU retrieval initiated.")
    return torch.cuda.get_device_properties(torch.device("cuda:0")).total_memory / (
        1024**3
    )


class State(TypedDict):
    model: Optional[PreTrainedModel]
    processor: Optional[ColPaliProcessor]
    device: Optional[str]


def load_model() -> State:
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
    state: State = {
        "model": None,
        "processor": None,
        "device": None,
    }

    try:
        if torch.cuda.is_available() and get_gpu_vram() > REQUIRED_MEMORY:
            state["model"], state["processor"] = load_gpu_model()
            state["device"] = "gpu"
            logger.info("A GPU was detected on this device.")
        else:
            state["model"] = load_cpu_model()
            state["device"] = "cpu"
            logger.info("A CPU was detected on this device.")
    except (RuntimeError, OSError) as e:
        logger.debug(f"There was an error in loading the model - {e}")

    if (
        state["device"] is None
        or state["device"] == "cpu"
        and state["model"] is None
        or state["device"] == "gpu"
        and (state["model"] is None or state["processor"] is None)
    ):
        logger.error("Model or processor was not loaded properly.")
        exit(1)

    return state
