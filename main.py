import os
import subprocess
import time
from datetime import datetime

rate = 120

def identify_session() -> str:
    if "WAYLAND_DISPLAY" in os.environ:
        return "W"
    elif "DISPLAY" in os.environ:
        return "X"
    else:
        raise ValueError("Unknown session type")


def is_gnome_desktop() -> bool:
    return os.environ.get("XDG_CURRENT_DESKTOP", "").lower() == "gnome"


def capture(session_type: str, is_gnome: bool):
    smarn_dir = os.path.dirname(os.path.abspath(__file__))
    screenshots_dir = os.path.join(smarn_dir, "screenshots")

    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"smarn_{timestamp}.png"
    filepath = os.path.join(screenshots_dir, filename)

    if session_type == "W":
        if not is_gnome:
            try:
                subprocess.run(["grim", filepath], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error executing grim: {e}")
            except FileNotFoundError:
                print("grim is not found. Install grim to take screenshots.")
        else:
            try:
                subprocess.run(["gnome-screenshot", "-f", filepath], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error executing gnome-screenshot: {e}")
            except FileNotFoundError:
                print(
                    "gnome-screenshot is not installed. Install gnome-screenshots to take screenshots."
                )

    elif session_type == "X":
        try:
            subprocess.run(["scrot", filepath], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing scrot: {e}")
        except FileNotFoundError:
            print("scrot is not found. Install scrot to take screenshots.")

    else:
        print("Unknown session type. Screenshot not possible.")


if __name__ == "__main__":
    while True:
        capture(identify_session(), is_gnome_desktop())
        time.sleep(rate)
