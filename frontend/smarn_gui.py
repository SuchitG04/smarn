import os
import sys
import customtkinter as ctk
from PIL import Image, ImageTk
import threading
from datetime import datetime
from pathlib import Path
import logging

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.main import search_images
from config.log_config import setup_logging

# Config
SCREENSHOTS_DIR = Path.home() / ".smarn" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


class SmarnApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

        # --- Load bundled fonts ---
        FONTS_DIR = Path(__file__).parent.parent / "fonts"
        regular_path = FONTS_DIR / "Roboto-Regular.ttf"
        bold_path = FONTS_DIR / "Roboto-Bold.ttf"

        try:
            ctk.FontManager.load_font(str(regular_path))
            ctk.FontManager.load_font(str(bold_path))
            self.logger.info("Roboto fonts loaded successfully.")
        except Exception as e:
            self.logger.error(f"Could not load fonts: {e}", exc_info=True)

        # --- WINDOW CONFIG ---
        self.app_name = "Smarn"
        self.title(f"{self.app_name} - Your screen, recalled.")
        self.geometry("1280x850")
        self.minsize(1000, 700)

        # Layout grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)  # results frame takes most space

        # --- FONTS ---
        self.title_font = ctk.CTkFont(family="Roboto", size=55, weight="bold")
        self.search_font = ctk.CTkFont(family="Roboto", size=18)
        self.metadata_font = ctk.CTkFont(family="Roboto", size=13)
        self.status_font = ctk.CTkFont(family="Roboto", size=16)

        # --- TITLE ---
        self.title_label = ctk.CTkLabel(
            self,
            text=self.app_name,
            font=self.title_font,
            text_color="#1E90FF",
        )
        self.title_label.grid(row=0, column=0, pady=(30, 10), sticky="n")

        # --- SEARCH BAR ---
        search_frame = ctk.CTkFrame(self, fg_color="#222222")
        search_frame.grid(row=1, column=0, padx=40, pady=10, sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search your screen history...",
            font=self.search_font,
            height=55,
        )
        self.search_entry.grid(row=0, column=0, padx=20, pady=15, sticky="ew")
        self.search_entry.bind("<Return>", lambda e: self.search())

        # --- RESULTS ---
        self.results_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.results_frame.grid(row=2, column=0, padx=30, pady=20, sticky="nsew")
        self.results_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="cols")

        # Status label (dynamic)
        self.status_label = None

        # Internal state
        self.search_in_progress = False
        self.images = []

    def search(self):
        if self.search_in_progress:
            return

        query = self.search_entry.get().strip()
        if not query:
            return

        self.search_in_progress = True
        self.search_entry.configure(state="disabled")

        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        self.images.clear()

        # Show searching status
        self.status_label = ctk.CTkLabel(
            self.results_frame,
            text=f"Searching for: {query}...",
            font=self.status_font,
            text_color="gray70",
        )
        self.status_label.pack(pady=80)

        threading.Thread(
            target=self._perform_search, args=(query,), daemon=True
        ).start()

    def _perform_search(self, query):
        try:
            results = search_images(query)
            self.after(0, self._display_results, results)
        except Exception as e:
            self.after(0, self._handle_error, f"Error: {e}")
        finally:
            self.after(0, self._search_complete)

    def _display_results(self, results):
        if self.status_label:
            self.status_label.destroy()

        if not results:
            self.status_label = ctk.CTkLabel(
                self.results_frame,
                text="No results found",
                font=self.status_font,
                text_color="gray70",
            )
            self.status_label.pack(pady=80)
            return

        for idx, item in enumerate(results):
            row, col = divmod(idx, 3)

            try:
                image_path = item["image_path"]
                if not os.path.exists(image_path):
                    continue

                # Result card
                result_frame = ctk.CTkFrame(self.results_frame)
                result_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

                # Thumbnail
                img = Image.open(image_path)
                img.thumbnail((380, 260))
                photo = ImageTk.PhotoImage(img)
                self.images.append(photo)

                img_label = ctk.CTkLabel(result_frame, image=photo, text="")
                img_label.pack(padx=10, pady=10)

                # Metadata
                timestamp = datetime.fromisoformat(item["timestamp"])
                metadata_text = (
                    f"{item['application_name']} · {timestamp.strftime('%b %d, %H:%M')}"
                )
                metadata_label = ctk.CTkLabel(
                    result_frame,
                    text=metadata_text,
                    font=self.metadata_font,
                    text_color="gray80",
                )
                metadata_label.pack(pady=(0, 10))

            except Exception as e:
                self.logger.error(
                    f"Error displaying image {item.get('image_path')}: {e}"
                )

    def _handle_error(self, message):
        if self.status_label:
            self.status_label.configure(text=message)

    def _search_complete(self):
        self.search_in_progress = False
        self.search_entry.configure(state="normal")


def main():
    setup_logging()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = SmarnApp()
    app.mainloop()


if __name__ == "__main__":
    main()
