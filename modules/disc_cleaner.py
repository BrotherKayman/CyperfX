import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttkB
import pyclamd
import shutil
import platform
import subprocess
import ctypes
import main
class DiscManager:
    """Class to manage disc operations such as clearing temporary files, cache, and deleting files."""

    def clear_temp_files(self):
        """Clear temporary files, cache directories, and empty the trash/recycle bin."""
        # Determine the operating system
        current_os = platform.system()

        # Get the system's temporary directory
        temp_dir = os.path.join(os.environ.get('TEMP', os.environ.get('TMPDIR', '/tmp')))

        # Define cache directories based on the operating system (basic)
        cache_dirs = []
        if current_os == "Windows":
            cache_dirs.extend([
                os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
                os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
                os.path.join(os.environ['LOCALAPPDATA'], 'Mozilla', 'Firefox', 'Profiles'),
            ])
        elif current_os == "Darwin":  # macOS
            cache_dirs.append(os.path.join(os.environ['HOME'], 'Library', 'Caches'))
        elif current_os == "Linux":
            cache_dirs.append(os.path.join(os.environ['HOME'], '.cache'))

        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to clear temporary files, cache, and empty the trash/recycle bin?")
        if not confirm:
            return

        # Calculate initial disk space
        initial_disk_space = shutil.disk_usage('/').free

        # Clear temporary files
        if temp_dir:
            try:
                shutil.rmtree(temp_dir)
                os.makedirs(temp_dir) 
                messagebox.showinfo("Success", "Temporary files cleared.")
            except Exception as e:
                messagebox.showerror("Error", f"Error clearing temporary files: {e}")

        # Clear cache directories
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                try:
                    shutil.rmtree(cache_dir)
                    os.makedirs(cache_dir)  
                    messagebox.showinfo("Success", f"Cache cleared at: {cache_dir}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error clearing cache at {cache_dir}: {e}")

        # Empty trash/recycle bin based on the operating system
        try:
            if current_os == "Windows":
                ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 1)
                messagebox.showinfo("Success", "Recycle bin emptied.")
            elif current_os == "Darwin":  # macOS
                # Run a shell command to empty trash on macOS
                subprocess.run(["osascript", "-e", 'tell application "Finder" to empty trash'], check=True)
                messagebox.showinfo("Success", "Trash emptied.")
            elif current_os == "Linux":
                # Run a shell command to empty the trash on Linux
                trash_path = os.path.join(os.environ['HOME'], ".local/share/Trash/files")
                shutil.rmtree(trash_path)
                messagebox.showinfo("Success", "Trash emptied.")
        except Exception as e:
            messagebox.showerror("Error", f"Error emptying trash/recycle bin: {e}")

        # Calculate final disk space
        final_disk_space = shutil.disk_usage('/').free

        # Calculate space freed
        space_freed = initial_disk_space - final_disk_space
        space_freed_mb = space_freed / (1024 * 1024)

        messagebox.showinfo("Space Freed", f"Space freed: {space_freed_mb:.2f} MB")

    def delete_files(self):
        """Open a file dialog for the user to choose files to delete."""
        file_paths = filedialog.askopenfilenames(title="Select files to delete")
        total_deleted_size = 0  # Track total size of deleted files

        if file_paths:
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected files?")
            if confirm:
                try:
                    for file_path in file_paths:
                        file_size = os.path.getsize(file_path)
                        total_deleted_size += file_size
                        os.remove(file_path)
                    messagebox.showinfo("Success", f"Selected files deleted. Total size freed: {total_deleted_size / (1024 * 1024):.2f} MB")
                except Exception as e:
                    messagebox.showerror("Error", f"Error deleting files: {e}")
            else:
                messagebox.showinfo("Deletion Cancelled", "File deletion was cancelled by the user.")
        else:
            messagebox.showinfo("No Files Selected", "No files selected for deletion.")

def main():
    # Main App window
    app = ttkB.Window(themename='superhero')
    app.title("Clean Disc")
    app.geometry('320x150')
    app.maxsize(height=200, width=600)
    app.minsize(height=200, width=600)

    # Create an instance of the DiscManager class
    disc_manager = DiscManager()

    # Create "Quick clean" button
    disc_frame = ttkB.Frame(app, height=400, width=600, style='')
    disc_frame.place(x=0, y=0)

    quick_clean_button = ttkB.Button(disc_frame, text="Quick clean", command=disc_manager.clear_temp_files, style='outline')
    quick_clean_button.place(x=50, y=50, height=100, width=150)

    # Create "Delete Files" button
    delete_files_button = ttkB.Button(disc_frame, text="Delete Files", command=disc_manager.delete_files, style='outline')
    delete_files_button.place(x=225, y=50, height=100, width=150)

    # Create "Exit" button
    exit_button = ttkB.Button(disc_frame, text="Exit", command=app.quit, style='outline.danger')
    exit_button.place(x=400, y=50, height=100, width=150)

    app.mainloop()

if __name__ == "__main__":
    main()