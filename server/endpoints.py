from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from db import Database
from pydantic_models import ImageMetadata, QueryResponse

app = FastAPI()
db = Database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:1420"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def greet():
    return {"message": "Hello from smarn"}


@app.get("/search", response_model=QueryResponse)
async def search(text_query: str):
    if not text_query or text_query.strip() == "":
        raise HTTPException(status_code=400, detail="Text query is empty")

    try:
        results: list | None = db.get_top_k_entries(text_query, 20)
        if not results:
            raise HTTPException(status_code=404, detail="No results found")

        image_list_with_metadata: list = []

        for entry in results:
            metadata = ImageMetadata(
                image_path=entry[0],
                application_name=entry[1],
                timestamp=entry[2],
                distance=entry[3],
            )
            image_list_with_metadata.append(metadata)

        response = QueryResponse(
            text_query=text_query, image_list_with_metadata=image_list_with_metadata
        )

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal sever error: " + str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="endpoints:app", host="localhost", port=8000, reload=True)
