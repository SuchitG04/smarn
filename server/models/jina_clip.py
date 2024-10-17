from transformers import AutoModel, PreTrainedModel
import logging

logger = logging.getLogger(__name__)

def load_cpu_model() -> PreTrainedModel:
    """
    Load the CLIP model for CPU.

    model name: "jinaai/jina-clip-v1"

    Returns:
        PreTrainedModel: The CLIP model.
    """
    logger.info("Loading Pretrained JinaAI from Huggingface Transformers.")
    return AutoModel.from_pretrained("jinaai/jina-clip-v1", trust_remote_code=True)