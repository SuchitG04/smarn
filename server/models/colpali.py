import torch
from colpali_engine.models import ColPali, ColPaliProcessor
from transformers import BitsAndBytesConfig, PreTrainedModel


def load_gpu_model() -> tuple[PreTrainedModel, ColPaliProcessor]:
    """
    Load the ColPali model and processor with 8-bit quantization for GPU.

    model name: "vidore/colpali-v1.2"

    Returns:
        tuple[PreTrainedModel, ColPaliProcessor]: The model and processor.
    """
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

    return model, processor
