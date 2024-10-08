import os
import subprocess
from datetime import datetime

def identify_session() -> str:
    if "WAYLAND_DISPLAY" in os.environ:
        return "W"
    elif "DISPLAY" in os.environ:
        return "X"
    else:
        raise ValueError("Unknown session type")

def capture(session_type: str):
    smarn_dir = os.path.dirname(os.path.abspath(__file__))
    screenshots_dir = os.path.join(smarn_dir, "screenshots")

    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"smarn_{timestamp}.png"
    filepath = os.path.join(screenshots_dir, filename)

    if session_type == "W": # Wayland session requires scrot
        try:
            subprocess.run(["grim", filepath], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing grim: {e}")
        except FileNotFoundError:
            print("grim is not found. Install grim to take screenshots.")
    elif session_type == "X": # X11 session requires scrot
        try:
            subprocess.run(["scrot", filepath], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing scrot: {e}")
        except FileNotFoundError:
            print("scrot is not found. Install scrot to take screenshots.")
    # Gnome support to be added
    else:
        print("Unknown session type. Screenshot not possible.")