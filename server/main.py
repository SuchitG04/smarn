import config.log_config  # setup logging
import uvicorn
from api.main import app
from screenshot import service
from models import load_model


if __name__ == "__main__":
    load_model()

    # TODO: Run both of these as two different processes using multiprocessor
    # WARN: The model gets loaded twice if the reload option is set to True.
    # uvicorn.run(app, host="localhost", port=8000)
    service()
