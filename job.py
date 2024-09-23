import os
import subprocess
from datetime import datetime

project_dir = os.path.dirname(os.path.abspath(__file__))

save_dir = os.path.join(project_dir, "smarn_screenshots")

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

def get_display_server():
    if os.getenv("WAYLAND_DISPLAY"):
        return "w"
    elif os.getenv("DISPLAY"):
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
        except subprocess.CalledProcessError:
            print("Grim failed, trying gnome-screenshot")
            try:
                subprocess.run(["gnome-screenshot", "-f", screenshot_file], check=True)
                print(f"Screenshot saved to {screenshot_file}")
            except FileNotFoundError:
                print("gnome-screenshot is not installed")

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