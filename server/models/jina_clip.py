from transformers import AutoModel, PreTrainedModel


def load_cpu_model() -> PreTrainedModel:
    """
    Load the CLIP model for CPU.

    model name: "jinaai/jina-clip-v1"

    Returns:
        PreTrainedModel: The CLIP model.
    """
    return AutoModel.from_pretrained("jinaai/jina-clip-v1", trust_remote_code=True)
