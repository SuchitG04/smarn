from pydantic import BaseModel

class ImageMetadata(BaseModel):
    image_path: str 
    application_name: str
    timestamp: str
    distance: float

class QueryResponse(BaseModel):
    text_query: str
    image_list_with_metadata: list[ImageMetadata]