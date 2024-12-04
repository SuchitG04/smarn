import requests

BASE_URL = "http://localhost:6942"


# TODO: convert the response to numpy array


async def get_image_embs(image_path: str) -> list[float]:
    try:
        res = requests.get(f"{BASE_URL}/imgemb/?image_path={image_path}")
    except:
        raise Exception("Unable to response from /imgemb endpoint")

    return res.json()


async def get_text_embs(query: str) -> list[float]:
    try:
        res = requests.get(f"{BASE_URL}/textemb/?query={query}")
    except:
        raise Exception("Unable to response from /textemb endpoint")

    return res.json()
