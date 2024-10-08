import time

from db import Database
from screenshot import capture
from utils import compare_with_prev_img

rate: float = 2.0


def smarn():
    db = Database("vectors.sqlite")
    while True:
        current_screenshot_path = capture()
        time.sleep(rate * 60)

        if curr_emb := compare_with_prev_img(current_screenshot_path):
            if rate >= 5:
                rate += 0.5
        else:
            if rate <= 2:
                rate -= 0.5


if __name__ == "__main__":
    smarn()

