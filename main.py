import time

from utils import compare_with_prev_img
from screenshot import capture

rate: float = 2.0
db = Database("vectors.sqlite")


def smarn():
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

