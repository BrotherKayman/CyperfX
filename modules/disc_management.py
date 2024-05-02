import tkinter as tk
import ttkbootstrap as ttkB
from ttkbootstrap.widgets import Button
import shutil
import os
from tkinter import filedialog, messagebox
import platform
import subprocess
import ctypes

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

    def delete_files(self):
        """Open a file dialog for the user to choose files to delete."""
        file_paths = filedialog.askopenfilenames(title="Select files to delete")

        if file_paths:
            
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected files?")
            
            if confirm:
                try:
                    
                    for file_path in file_paths:
                        os.remove(file_path)
                    messagebox.showinfo("Success", "Selected files deleted.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error deleting files: {e}")
            else:
                messagebox.showinfo("Deletion Cancelled", "File deletion was cancelled by the user.")
        else:
            messagebox.showinfo("No Files Selected", "No files selected for deletion.")

def main():
    # Main App window
    app = ttkB.Window(themename='solar')
    app.title("Clean Disc")
    app.geometry('320x150')
    app.maxsize(height=150, width=320)
    app.minsize(height=150, width=320)

    # Create an instance of the DiscManager class
    disc_manager = DiscManager()

    # Create "Quick clean" button
    quick_clean_button = Button(app, text="Quick clean", command=disc_manager.clear_temp_files, style='info.Outline.TButton')
    quick_clean_button.place(x=55, y=30)

    # Create "Delete Files" button
    delete_files_button = Button(app, text="Delete Files", command=disc_manager.delete_files, style='danger.Outline.TButton')
    delete_files_button.place(x=170, y=30)

    # Create "Exit" button
    exit_button = Button(app, text="Exit", command=app.quit, style='warning.Outline.TButton')
    exit_button.place(x=220, y=80)

    app.mainloop()

if __name__ == "__main__":
    main()
