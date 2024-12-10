import logging
import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from transformers import PreTrainedModel

from model.jina_clip import load_cpu_model

logger = logging.getLogger(__name__)
model: PreTrainedModel | None = None


@asynccontextmanager
async def lifespan(_):
    logger.info("Starting FastAPI model service.")
    global model
    model = load_cpu_model()
    yield
    logger.info("Ending FastAPI model service.")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:1420"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/imgemb", response_model=list[float])
async def get_img_emb(image_path: str):
    global model
    if not os.path.exists(image_path):
        raise ValueError("Image path does not exist!")

    logger.info("Image embedding retrieved.")
    if not model:
        logger.error("Model not loaded")
        raise ValueError("Model not loaded")
    return model.encode_image(image_path)


@app.get("/textemb", response_model=list[float])
async def get_text_emb(query: str):
    global model

    logger.info("Text embedding retrieved.")
    if not model:
        logger.error("Model not loaded")
        raise ValueError("Model not loaded")
    return model.encode_text(query)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=6942, reload=True)
