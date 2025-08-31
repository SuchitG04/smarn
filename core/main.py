from typing import List, Dict, Any
from .db import Database
from .model import JinaClipModel

db = Database()
model = JinaClipModel()


def search_images(text_query: str) -> List[Dict[str, Any]]:
    """
    Search for images based on a text query.
    """
    if not text_query or not text_query.strip():
        return []

    text_emb = model.get_text_embs(text_query)
    results = db.get_top_k_entries(text_emb, 9)

    if not results:
        return []

    image_list_with_metadata = []
    for entry in results:
        metadata = {
            "image_path": entry[0],
            "application_name": entry[1],
            "timestamp": entry[2],
            "distance": entry[3],
        }
        image_list_with_metadata.append(metadata)

    return image_list_with_metadata
