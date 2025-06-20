import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import shutil
from pathlib import Path
import threading
import logging

# Version information
VERSION = "0.1.0"

class PhotoOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Organizer & Tidier")
        self.root.geometry("600x400")
        self.root.resizable(True, True)

        # Setup a logger that does nothing until configured
        self.logger = logging.getLogger('PhotoOrganizer')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.NullHandler())

        # Variables
        self.selected_directory = tk.StringVar()
        self.run_mode = tk.StringVar(value="organize")

        self.setup_ui()

        # This log message will be ignored until a file handler is configured
        self.logger.info("Photo Organizer application started")

    def setup_logging(self, log_directory):
        """Setup logging configuration to a file."""
        # Remove existing handlers (like NullHandler) to avoid duplicates
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                     datefmt='%Y-%m-%d %H:%M:%S')

        # Create file handler
        log_file_path = Path(log_directory) / 'log.txt'

        file_handler = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        # Add handler to logger
        self.logger.addHandler(file_handler)

        # Write version information at the top of the log file
        self.logger.info(f"Photo Organizer & Tidier v{VERSION}")
        self.logger.info(f"File logging enabled. Log file: {log_file_path}")

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="Photo Organizer & Tidier",
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Directory selection
        ttk.Label(main_frame, text="Select Photo Directory:").grid(row=1, column=0, sticky=tk.W, pady=5)

        dir_frame = ttk.Frame(main_frame)
        dir_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        dir_frame.columnconfigure(0, weight=1)

        self.dir_entry = ttk.Entry(dir_frame, textvariable=self.selected_directory, state="readonly")
        self.dir_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))

        browse_btn = ttk.Button(dir_frame, text="Browse", command=self.browse_directory)
        browse_btn.grid(row=0, column=1)

        # Run mode selection
        ttk.Label(main_frame, text="Select Run Mode:").grid(row=3, column=0, sticky=tk.W, pady=(20, 5))

        mode_frame = ttk.Frame(main_frame)
        mode_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        organize_radio = ttk.Radiobutton(mode_frame, text="Organize Photos",
                                       variable=self.run_mode, value="organize")
        organize_radio.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))

        tidy_radio = ttk.Radiobutton(mode_frame, text="Tidy Photos",
                                   variable=self.run_mode, value="tidy")
        tidy_radio.grid(row=0, column=1, sticky=tk.W)

        # Mode descriptions
        desc_frame = ttk.Frame(main_frame)
        desc_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        desc_frame.columnconfigure(0, weight=1)

        self.desc_label = ttk.Label(desc_frame, text="", wraplength=500, justify=tk.LEFT)
        self.desc_label.grid(row=0, column=0, sticky=tk.W)

        # Update description based on mode
        self.update_description()

        # Bind radio buttons to update description
        organize_radio.config(command=self.update_description)
        tidy_radio.config(command=self.update_description)

        # Run button
        self.run_btn = ttk.Button(main_frame, text="Run", command=self.run_operation,
                                 style="Accent.TButton")
        self.run_btn.grid(row=6, column=0, columnspan=3, pady=20)

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready", font=("Arial", 10))
        self.status_label.grid(row=8, column=0, columnspan=3, pady=5)

    def update_description(self):
        if self.run_mode.get() == "organize":
            desc = ("Organize Photos: Creates RAW and JPG folders, moves .cr2 files to RAW, "
                   ".jpg files to JPG, and creates a copy called 'JPG - Edit 1' for editing.")
        else:
            desc = ("Tidy Photos: Keeps only .cr2 files in RAW folder that have corresponding "
                   ".jpg files in the 'JPG - Edit 1' folder (same filename, different extension).")

        self.desc_label.config(text=desc)

    def browse_directory(self):
        directory = filedialog.askdirectory(title="Select Photo Directory")
        if directory:
            self.selected_directory.set(directory)
            # Logging will be configured when an operation is run
            self.logger.info(f"Directory selected: {directory}")
        else:
            self.logger.info("Directory selection cancelled by user")

    def run_operation(self):
        if not self.selected_directory.get():
            messagebox.showerror("Error", "Please select a directory first!")
            return

        # Configure file logging now that an operation is starting
        self.setup_logging(self.selected_directory.get())

        selected_mode = self.run_mode.get()
        self.logger.info(f"Starting operation: {selected_mode} mode")
        self.logger.info(f"Target directory: {self.selected_directory.get()}")

        # Disable UI during operation
        self.run_btn.config(state="disabled")
        self.progress.start()
        self.status_label.config(text="Processing...")

        # Run operation in separate thread to keep UI responsive
        thread = threading.Thread(target=self._run_operation_thread)
        thread.daemon = True
        thread.start()

    def _run_operation_thread(self):
        try:
            if self.run_mode.get() == "organize":
                self.logger.info("Executing organize_photos operation")
                self.organize_photos()
            else:
                self.logger.info("Executing tidy_photos operation")
                self.tidy_photos()
            self.logger.info("Operation completed successfully")
        except Exception as error:
            error_msg = str(error)
            self.logger.error(f"Operation failed with error: {error_msg}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {error_msg}"))
        finally:
            self.root.after(0, self._operation_complete)

    def _operation_complete(self):
        self.progress.stop()
        self.run_btn.config(state="normal")
        self.status_label.config(text="Ready")
        self.logger.info("UI reset to ready state\n")

    def organize_photos(self):
        source_dir = Path(self.selected_directory.get())
        self.logger.info(f"Starting photo organization in: {source_dir}")

        # Create folders
        raw_folder = source_dir / "RAW"
        jpg_folder = source_dir / "JPG"
        jpg_edit_folder = source_dir / "JPG - Edit 1"

        self.logger.info("Creating folder structure")
        raw_folder.mkdir(exist_ok=True)
        jpg_folder.mkdir(exist_ok=True)
        self.logger.info(f"Created RAW folder: {raw_folder}")
        self.logger.info(f"Created JPG folder: {jpg_folder}")

        # Move files
        moved_cr2 = 0
        moved_jpg = 0
        total_files = 0

        self.logger.info("Scanning directory for photo files")
        for file_path in source_dir.iterdir():
            if file_path.is_file():
                total_files += 1
                if file_path.suffix.lower() == '.cr2':
                    destination = raw_folder / file_path.name
                    shutil.move(str(file_path), str(destination))
                    moved_cr2 += 1
                    self.logger.info(f"Moved CR2 file: {file_path.name} -> {destination}")
                elif file_path.suffix.lower() == '.jpg':
                    destination = jpg_folder / file_path.name
                    shutil.move(str(file_path), str(destination))
                    moved_jpg += 1
                    self.logger.info(f"Moved JPG file: {file_path.name} -> {destination}")

        self.logger.info(f"File processing complete. Total files scanned: {total_files}")
        self.logger.info(f"CR2 files moved: {moved_cr2}")
        self.logger.info(f"JPG files moved: {moved_jpg}")

        # Copy JPG folder to JPG - Edit 1
        self.logger.info("Creating JPG - Edit 1 folder")
        if jpg_folder.exists() and any(jpg_folder.iterdir()):
            if jpg_edit_folder.exists():
                self.logger.info("Removing existing JPG - Edit 1 folder")
                shutil.rmtree(jpg_edit_folder)
            shutil.copytree(jpg_folder, jpg_edit_folder)
            self.logger.info(f"Created JPG - Edit 1 folder: {jpg_edit_folder}")
        else:
            self.logger.warning("No JPG files found to copy to JPG - Edit 1 folder")

        message = (f"Organization complete!\n\n"
                  f"Moved {moved_cr2} .cr2 files to RAW folder\n"
                  f"Moved {moved_jpg} .jpg files to JPG folder\n"
                  f"Created JPG - Edit 1 folder\n\n"
                  f"Please edit the photos in the 'JPG - Edit 1' folder, "
                  f"then return to this tool and select 'Tidy Photos' mode.")

        self.logger.info("Photo organization completed successfully")
        self.root.after(0, lambda: messagebox.showinfo("Success", message))

    def tidy_photos(self):
        source_dir = Path(self.selected_directory.get())
        raw_folder = source_dir / "RAW"
        jpg_edit_folder = source_dir / "JPG - Edit 1"

        self.logger.info(f"Starting photo tidying in: {source_dir}")

        if not raw_folder.exists():
            error_msg = "RAW folder not found! Please run 'Organize Photos' first."
            self.logger.error(error_msg)
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            return

        if not jpg_edit_folder.exists():
            error_msg = "JPG - Edit 1 folder not found! Please run 'Organize Photos' first."
            self.logger.error(error_msg)
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            return

        self.logger.info(f"RAW folder found: {raw_folder}")
        self.logger.info(f"JPG - Edit 1 folder found: {jpg_edit_folder}")

        # Get list of edited JPG files (without extension)
        self.logger.info("Scanning JPG - Edit 1 folder for edited photos")
        edited_jpgs = {f.stem for f in jpg_edit_folder.iterdir()
                      if f.is_file() and f.suffix.lower() == '.jpg'}
        self.logger.info(f"Found {len(edited_jpgs)} edited JPG files: {list(edited_jpgs)}")

        # Keep only CR2 files that have corresponding JPG files
        kept_cr2 = 0
        removed_cr2 = 0
        total_cr2 = 0

        self.logger.info("Processing CR2 files in RAW folder")
        for cr2_file in raw_folder.iterdir():
            if cr2_file.is_file() and cr2_file.suffix.lower() == '.cr2':
                total_cr2 += 1
                if cr2_file.stem in edited_jpgs:
                    kept_cr2 += 1
                    self.logger.info(f"Keeping CR2 file: {cr2_file.name} (has edited JPG)")
                else:
                    self.logger.info(f"Removing CR2 file: {cr2_file.name} (no edited JPG)")
                    cr2_file.unlink()  # Delete the file
                    removed_cr2 += 1

        self.logger.info(f"CR2 file processing complete. Total CR2 files: {total_cr2}")
        self.logger.info(f"CR2 files kept: {kept_cr2}")
        self.logger.info(f"CR2 files removed: {removed_cr2}")

        # Rename RAW folder to RAW - Edit 1
        raw_edit_folder = source_dir / "RAW - Edit 1"
        self.logger.info("Renaming RAW folder to RAW - Edit 1")
        if raw_folder.exists():
            raw_folder.rename(raw_edit_folder)
            self.logger.info(f"Successfully renamed folder: {raw_folder} -> {raw_edit_folder}")
        else:
            self.logger.warning("RAW folder not found for renaming")

        message = (f"Tidying complete!\n\n"
                  f"Kept {kept_cr2} .cr2 files (have corresponding edited .jpg)\n"
                  f"Removed {removed_cr2} .cr2 files (no corresponding edited .jpg)\n"
                  f"Renamed RAW folder to 'RAW - Edit 1'")

        self.logger.info("Photo tidying completed successfully")
        self.root.after(0, lambda: messagebox.showinfo("Success", message))

def main():
    root = tk.Tk()
    app = PhotoOrganizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()