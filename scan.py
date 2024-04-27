import tkinter as tk
from tkinter import ttk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Main Window")
        self.geometry("300x200")
        
        # Create a button to open the scan window
        self.button = ttk.Button(self, text="Open Scan Window", command=self.open_scan_window)
        self.button.pack(pady=20)
    
    def open_scan_window(self):
        # Hide the current window
        self.withdraw()
        
        # Open the scan window
        scan_window = ScanWindow(self)
        scan_window.mainloop()

class ScanWindow(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.title("Scan Window")
        self.geometry("300x200")
        
        # Add widgets and functionality as needed
        label = ttk.Label(self, text="Scanning in progress...")
        label.pack(pady=20)
        
        # Optionally, you can add a button to close the scan window and show the main window again
        close_button = ttk.Button(self, text="Close Scan Window", command=self.close_scan_window)
        close_button.pack(pady=20)
        
        # Save a reference to the parent window
        self.parent = parent
    
    def close_scan_window(self):
        # Close the scan window
        self.destroy()
        # Show the main window again
        self.parent.deiconify()

if __name__ == "__main__":
    # Create and show the main window
    main_window = MainWindow()
    main_window.mainloop()
