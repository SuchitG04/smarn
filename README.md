# smarn

smarn is a local, open-source AI-powered feature for Linux that captures and stores screenshots of your activities every few seconds, allowing you to search for records of past activity using natural language.

## Intentions

smarn is designed as a Linux-exclusive counterpart to Windows Recall (although this is not the sole identity of this piece of software).
We want to give Linux users a flavour of convenience without having to supply telemetry and surveillance data.

## What does it use?

- `tauri` for a supple, sleek and minimalist user interface. ([tauri](https://github.com/tauri-apps/tauri))
- The `transformers` library; more specifically the jinaai/jina-clip-v1 model - for text and image-embedding. ([transformers](https://github.com/huggingface/transformers))
- Two FastAPI services that provide functions corresponding to text and image embeddings, searching using the said embeddings, and exposing screenshots to the interface. ([FastAPI](https://github.com/fastapi/fastapi))
- An `sqlite-vec` database to store embeddings and image-paths as well as to search for them. ([sqlite-vec](https://github.com/asg017/sqlite-vec))
- Asynchronus running of services to ensure maximum concurrency and non-blocking operations.
- An intelligent, self-rate-controlling mechanism that reduces/increases the rate of screenshot captures based on similarity of the previous and current screenshots (hence reducing compute and wastage of storage space).
