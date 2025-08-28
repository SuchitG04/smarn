import os
import customtkinter as ctk
from PIL import Image, ImageTk
import requests
import threading
from datetime import datetime
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:8000"
SCREENSHOTS_DIR = Path.home() / ".smarn" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


class SmarnApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("smarn - Linux Screen Recall")
        self.geometry("1200x800")

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Create search frame
        self.search_frame = ctk.CTkFrame(self, corner_radius=0)
        self.search_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Search entry
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search your screen history...",
            width=600,
            height=40,
            font=("Arial", 14),
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.search())

        # Search button
        self.search_button = ctk.CTkButton(
            self.search_frame, text="Search", command=self.search, height=40, width=100
        )
        self.search_button.pack(side="right")

        # Results frame
        self.results_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
        self.results_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.results_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Status bar
        self.status_var = ctk.StringVar(value="Ready")
        self.status_bar = ctk.CTkLabel(
            self,
            textvariable=self.status_var,
            anchor="w",
            font=("Arial", 10),
            text_color=("gray50", "gray70"),
        )
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 5))

        # Initial state
        self.search_in_progress = False
        self.images = []

    def search(self):
        if self.search_in_progress:
            return

        query = self.search_entry.get().strip()
        if not query:
            self.status_var.set("Please enter a search query")
            return

        self.search_in_progress = True
        self.status_var.set(f"Searching for: {query}...")
        self.search_button.configure(state="disabled")

        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        self.images.clear()

        # Start search in a separate thread
        threading.Thread(
            target=self._perform_search, args=(query,), daemon=True
        ).start()

    def _perform_search(self, query):
        try:
            response = requests.get(
                f"{API_BASE_URL}/search", params={"text_query": query}
            )
            response.raise_for_status()
            results = response.json()

            # Schedule UI update on the main thread
            self.after(0, self._display_results, results)

        except requests.RequestException as e:
            self.after(0, self._handle_error, f"Error searching: {str(e)}")
        finally:
            self.after(0, self._search_complete)

    def _display_results(self, results):
        if not results.get("image_list_with_metadata"):
            self.status_var.set("No results found")
            return

        self.status_var.set(f"Found {len(results['image_list_with_metadata'])} results")

        for idx, item in enumerate(results["image_list_with_metadata"]):
            row = idx // 3
            col = idx % 3

            # Create a frame for each result
            result_frame = ctk.CTkFrame(self.results_frame, corner_radius=5)
            result_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

            # Load and display image
            image_path = item["image_path"]
            image_name = os.path.basename(image_path)
            local_path = SCREENSHOTS_DIR / image_name

            # Download image if not exists
            if not local_path.exists():
                try:
                    img_response = requests.get(f"{API_BASE_URL}/images/{image_name}")
                    img_response.raise_for_status()
                    with open(local_path, "wb") as f:
                        f.write(img_response.content)
                except Exception as e:
                    print(f"Error downloading image: {e}")
                    continue

            try:
                # Load and resize image
                img = Image.open(local_path)
                img.thumbnail((300, 200))
                photo = ImageTk.PhotoImage(img)

                # Store reference to prevent garbage collection
                self.images.append(photo)

                # Create image label
                img_label = ctk.CTkLabel(result_frame, image=photo, text="")
                img_label.pack(padx=5, pady=5)

                # Add metadata
                timestamp = datetime.fromisoformat(
                    item["timestamp"].replace("Z", "+00:00")
                )
                metadata_text = (
                    f"App: {item['application_name']}\n"
                    f"Time: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"Score: {1 - item['distance']:.2f}"
                )

                metadata_label = ctk.CTkLabel(
                    result_frame,
                    text=metadata_text,
                    font=("Arial", 10),
                    justify="left",
                    anchor="w",
                )
                metadata_label.pack(padx=5, pady=(0, 5), fill="x")

            except Exception as e:
                print(f"Error displaying image: {e}")

    def _handle_error(self, message):
        self.status_var.set(message)

    def _search_complete(self):
        self.search_in_progress = False
        self.search_button.configure(state="normal")


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = SmarnApp()
    app.mainloop()


if __name__ == "__main__":
    main()
