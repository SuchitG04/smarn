import logging

from transformers import AutoModel, PreTrainedModel

logger = logging.getLogger(__name__)


def load_cpu_model() -> PreTrainedModel:
    """
    Load the CLIP model for CPU.

    model name: "jinaai/jina-clip-v1"

    Returns:
        PreTrainedModel: The CLIP model.
    """
    model: PreTrainedModel | None = None
    logger.info("Loading Pretrained JinaAI from Huggingface Transformers.")
    try:
        model = AutoModel.from_pretrained("jinaai/jina-clip-v1", trust_remote_code=True)
    except (RuntimeError, OSError) as e:
        logger.debug(f"There was an error in loading the model - {e}")

    if model is None:
        logger.error("Model was not loaded properly.")
        exit(1)

    return model

