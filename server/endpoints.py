from fastapi import FastAPI
from db import Database
from models import ImageMetadata, QueryResponse

app = FastAPI()
db = Database()

@app.get("/")
async def greet():
    return {
        "message": "Hello from smarn"
    }

@app.get("/search", response_class=QueryResponse)
async def search(text_query: str):
    results: list = db.get_top_k_entries(text_query, 20)

    image_list_with_metadata: list = []

    for entry in results:
        metadata = ImageMetadata(
            image_path=entry[0],
            application_name=entry[1],
            timestamp=entry[2],
            distance=entry[3]
        )
        image_list_with_metadata.append(metadata)

    response = QueryResponse(
        text_query=text_query,
        image_list_with_metadata=image_list_with_metadata
    )

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="localhost", port=8000, reload=True)