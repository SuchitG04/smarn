import config.log_config  # setup logging

# import uvicorn
from models import load_model
from screenshot import service

if __name__ == "__main__":
    state = load_model()

    # TODO: Run both of these as two different processes using multiprocessor
    # uvicorn.run("api.main:app", host="localhost", port=8000, reload=True)
    service(state)
