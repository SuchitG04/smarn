import os
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from server.model import get_text_embs

from .pydantic_models import ImageMetadata, QueryResponse

# INFO:  Use this if you are trying to run this file directly.
# from pydantic_models import (
#     ImageMetadata,
#     QueryResponse,
# )


# Adding the parent directory to sys.path to import db
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import Database

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
        text_emb = await get_text_embs(text_query)
        results: list | None = db.get_top_k_entries(text_emb, 20)
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

    import config.log_config  # setup logging

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)

