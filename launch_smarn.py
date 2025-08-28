#!/usr/bin/env python3
import os
import sys
import subprocess
import time


def check_backend_running():
    """Check if backend server is already running"""
    try:
        import requests

        response = requests.get("http://localhost:8000/", timeout=2)
        return response.status_code == 200
    except Exception:
        return False


def start_backend():
    """Start the backend server"""
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    return subprocess.Popen(
        [sys.executable, "server/main.py"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def start_frontend():
    """Start the frontend application"""
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
    return subprocess.Popen(
        [sys.executable, "smarn_gui.py"],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def main():
    # Check if backend is already running
    if not check_backend_running():
        print("Starting smarn backend...")
        backend_process = start_backend()

        # Give the backend some time to start
        time.sleep(3)

        if not check_backend_running():
            print("Error: Failed to start smarn backend")
            backend_process.terminate()
            return 1
    else:
        print("Using existing smarn backend")
        backend_process = None

    try:
        print("Starting smarn frontend...")
        frontend_process = start_frontend()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if backend_process:
            print("Stopping backend...")
            backend_process.terminate()

    return 0


if __name__ == "__main__":
    sys.exit(main())
