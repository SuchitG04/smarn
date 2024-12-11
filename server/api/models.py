from typing import List, Optional

from pydantic import BaseModel

class ImageMetadata(BaseModel):
    image_path: str
    application_name: Optional[str] = ""
    timestamp: str
    distance: float


class QueryResponse(BaseModel):
    text_query: str
    image_list_with_metadata: List[ImageMetadata]
