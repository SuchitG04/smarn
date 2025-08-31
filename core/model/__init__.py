from .jina_clip import JinaClipModel

# Create a single, shared instance of the model
model = JinaClipModel()

__all__ = ["model"]
