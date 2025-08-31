#!/usr/bin/env python3
import sys
import threading

from config.log_config import setup_logging
from core.screenshot import service as screenshot_service
from frontend.smarn_gui import main as gui_main


def main():
    """Main function to launch the smarn application."""
    # Set up logging
    setup_logging()

    # Start the screenshot service in a background thread
    screenshot_thread = threading.Thread(target=screenshot_service, daemon=True)
    screenshot_thread.start()

    # Start the GUI
    gui_main()

    return 0


if __name__ == "__main__":
    sys.exit(main())
