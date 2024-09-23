import os
import subprocess
from PIL import Image
from datetime import datetime
import time

rate = 120

def identify_session() -> str:
    if "WAYLAND_DISPLAY" in os.environ:
        return "W"
    elif "DISPLAY" in os.environ:
        return "X"
    else:
        return "U"
        raise ValueError("Unknown session type")

def is_gnome_desktop() -> str:
    return os.environ.get('XDG_CURRENT_DESKTOP', '').lower() == "gnome"

def capture(session_type: str, is_gnome: bool) -> Image:
    smarn_dir = os.path.dirname(os.path.abspath(__file__))
    screenshots_dir = os.path.join(smarn_dir, "screenshots")

    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
        print(f"Created directory: {screenshots_dir}")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"smarn_{timestamp}.png"
    filepath = os.path.join(screenshots_dir, filename)

    if session_type == "W":
        if not is_gnome:
            try:
                subprocess.run(["grim", filepath], check=True)
                print("Screenshot saved as ", filepath)
            except subprocess.CalledProcessError as e:
                print(f"Error executing grim: {e}")
            except FileNotFoundError:
                print("grim is not found. Install grim to take screenshots")
        else:
            try:
                subprocess.run(['gnome-screenshot', '-f', filepath], check=True)
                print(f"Screenshot saved as {filepath}")
            except subprocess.CalledProcessError as e:
                print(f"Error executing gnome-screenshot: {e}")
            except FileNotFoundError:
                print("gnome-screenshot is not installed. Please install it to take screenshots.")

    elif session_type == "X":
        try:
            subprocess.run(["scrot", filepath], check=True)
            print("Screenshot saved as ", filepath)
        except subprocess.CalledProcessError as e:
            print(f"Error executing scrot: {e}")
        except FileNotFoundError:
            print("scrot is not found. Install scrot to take screenshots")

if __name__ == "__main__":
    capture(identify_session(), is_gnome_desktop())