import os
import subprocess
from datetime import datetime

save_dir = os.path.expanduser("~/smarn/smarn_screenshots")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)


def get_display_server():
    wayland = os.getenv("WAYLAND_DISPLAY")
    xorg = os.getenv("DISPLAY")

    if wayland:
        return "w"
    elif xorg:
        return "x"
    else:
        return None


def take_screenshot():
    display_server = get_display_server()
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_file = os.path.join(save_dir, f"screenshot_smarn_{current_time}.png")

    if display_server == "w":
        try:
            subprocess.run(["grim", screenshot_file], check=True)
            print(f"Screenshot saved to {screenshot_file}")
        except FileNotFoundError:
            print("grim is not installed")

    elif display_server == "x":
        try:
            subprocess.run(["scrot", screenshot_file], check=True)
            print(f"Screenshot saved to {screenshot_file}")
        except FileNotFoundError:
            print("scrot is not installed")

    else:
        print("Could not detect display server")


if __name__ == "__main__":
    take_screenshot()
