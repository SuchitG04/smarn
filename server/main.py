import asyncio

import config.log_config  # setup logging

# import uvicorn
from screenshot import service

if __name__ == "__main__":
    # TODO: make a start-up script to run these services
    # uvicorn.run("api.main:app", host="localhost", port=8000, reload=True)
    # uvicorn.run("api.main:app", host="localhost", port=8000, reload=True)

    asyncio.run(service())
