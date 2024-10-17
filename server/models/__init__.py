import torch.cuda as cuda
from colpali import load_gpu_model
from jina_clip import load_cpu_model

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
        - The `processor` variable is not assigned as it is not required for the CPU model.
    """
    global model, processor, device
    if model is None:
        try:
            if cuda.is_available():
                model, processor = load_gpu_model()
                device = "gpu"
            else:
                model = load_cpu_model()
                device = "cpu"
        except (RuntimeError, OSError) as e:
            print(f"Error loading model: {e}")


load_model()
