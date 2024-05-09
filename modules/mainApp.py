import psutil
from PIL import Image
from tkinter import PhotoImage
from datetime import datetime
import subprocess
from ttkbootstrap import ttk as ttkB
from disc_management import DiscManager

Image.CUBIC = Image.BICUBIC

class SystemMonitorApp:
    """Class to manage CyperfX
    This module monitors system performance/ utilization.
    """

    def __init__(self):
        """Initialize the application window and components."""
        # Create the application window
        self.app = ttkB.Window(themename='solar')
        self.app.title('Cyperfx')
        img = PhotoImage(file='icon.png')
        self.app.iconphoto(False, img)
        self.app.geometry('770x550')
        self.app.minsize(height=550, width=770)
        self.app.maxsize(height=550, width=770)

        # Initialize the notebook
        self.notebook = ttkB.Notebook(self.app)
        self.notebook.place(x=50, y=40, width=650, height=450)

        # Create frames for each tab and add them to the notebook
        self.cpu_frame = ttkB.Frame(self.notebook)
        self.ram_frame = ttkB.Frame(self.notebook)
        self.disc_frame = ttkB.Frame(self.notebook)

        self.notebook.add(self.cpu_frame, text='CPU')
        self.notebook.add(self.ram_frame, text='RAM')
        self.notebook.add(self.disc_frame, text='Disc')

        # Create GUI components for each frame
        self.create_cpu_frame()
        self.create_ram_frame()
        self.create_disc_frame()

        # Create buttons at the bottom
        self.create_footer()

        # Start monitoring functions
        self.update_cpu_meter()
        self.update_ram_meter()
        self.update_disc_data()

        # Start the main event loop
        self.app.mainloop()

    def create_cpu_frame(self):
        """Create the CPU usage frame."""
        # Create CPU meter
        self.cpu_meter = ttkB.Meter(
            self.cpu_frame,
            metersize=120,
            bootstyle='success',
            stripethickness=10,
            amounttotal=100,
            subtext='CPU usage',
            textright='%',
            subtextfont='Helvetica 8',
            interactive=False,
            metertype='full'
        )
        self.cpu_meter.place(x=35, y=10)

    def create_ram_frame(self):
        """Create the RAM usage frame."""
        # Create RAM meter
        self.ram_meter = ttkB.Meter(
            self.ram_frame,
            metersize=120,
            bootstyle='success',
            stripethickness=20,
            amounttotal=100,
            subtext='RAM usage',
            textright='%',
            subtextfont='Helvetica 8',
            interactive=False,
            metertype='full'
        )
        self.ram_meter.place(x=35, y=10)

    def create_disc_frame(self):
        """Create the disc usage frame."""
        # Create disc usage components
        self.disc_free = ttkB.Meter(
            self.disc_frame,
            metersize=160,
            amountused=0,
            subtext='Disc available',
            interactive=False,
            metertype='full',
            amounttotal=500,
            bootstyle='success',
            textright='GB'
        )
        self.disc_free.place(x=30, y=35)
        
        # Calculate and set initial free disk space
        disk_info = psutil.disk_usage('/')
        free_gb = disk_info.free / (1024 ** 3)
        self.disc_free['amountused'] = f'{free_gb:.2f}'
        
        # Create disc usage progress bar and label
        self.disc_usage_label = ttkB.Label(
            self.disc_frame,
            text='Disc Usage'
        )
        self.disc_usage_label.place(x=270, y=135)
        
        # Create disc usage progress bar
        self.disc_usage = ttkB.Progressbar(
            self.disc_frame,
            style='info.Horizontal.TProgressBar',
            length=200,
            value=psutil.disk_usage('/').percent
        )
        self.disc_usage.place(x=350, y=130, height=30)

        # Create disc usage value label
        self.disc_usage_value = ttkB.Label(
            self.disc_frame,
            text=f'{self.disc_usage["value"]:.2f}%'
        )
        self.disc_usage_value.place(x=560, y=135)

        # Create disc used label and progress bar
        self.disc_used_label = ttkB.Label(
            self.disc_frame,
            text='Disc Used'
        )
        self.disc_used_label.place(x=270, y=85)

        self.disc_used = ttkB.Progressbar(
            self.disc_frame,
            style='info.Horizontal.TProgressBar',
            length=200,
            value=0
        )
        self.disc_used.place(x=350, y=85, height=30)

        self.disc_used_value = ttkB.Label(
            self.disc_frame,
            text='0.00 GB'
        )
        self.disc_used_value.place(x=560, y=85)

    def create_footer(self):
        """Create the watermark and buttons at the bottom."""
        # Watermark labels
        self.waterMark = ttkB.Label(text='Kagiso Motlhaoleng', font='Helvetica 20 bold')
        self.waterMark.place(x=400, y=110)
        self.waterMark = ttkB.Label(text='ALX Africa C18', font='Helvetica 10')
        self.waterMark.place(x=400, y=150)

        # Buttons frame
        self.buttons = ttkB.Frame(self.app)
        self.buttons.place(x=50, y=500, width=670, height=50)

        # Create and place buttons
        self.exit_button = ttkB.Button(
            self.buttons,
            text='Exit',
            command=self.quit_app,
            underline=0,
            style='info.Outline.TButton'
        )
        self.exit_button.place(x=0, y=0)

        self.malware_scan_button = ttkB.Button(
            self.buttons,
            text='Scan Malware',
            command=self.run_malware_scan,
            underline=0,
            style='warning.TButton'
        )
        self.malware_scan_button.place(x=535, y=0)

        self.disc_manager_button = ttkB.Button(
            self.buttons,
            text='Clean Disc',
            command=self.start_disc_manager,
            underline=0,
            style='primary.Outline.TButton'
        )
        self.disc_manager_button.place(x=415, y=0)

    def run_malware_scan(self):
        """Run the malware scan script as a subprocess."""
        subprocess.run(["python3", "malware_scan.py"])

    def start_disc_manager(self):
        """Run the disc management script."""
        subprocess.run(["python3", "disc_management.py"])

    def update_cpu_meter(self):
        """Update the CPU meter."""
        cpu_percent = psutil.cpu_percent()
        self.cpu_meter['amountused'] = cpu_percent
        if cpu_percent >= 50.00:
            self.cpu_meter.configure(bootstyle='warning')
        else:
            self.cpu_meter.configure(bootstyle='success')

        self.app.after(1000, self.update_cpu_meter)

    def update_ram_meter(self):
        """Update the RAM meter."""
        ram_percent = psutil.virtual_memory().percent
        self.ram_meter['amountused'] = ram_percent
        if ram_percent >= 50:
            self.ram_meter.configure(bootstyle='warning')
        else:
            self.ram_meter.configure(bootstyle='success')

        self.app.after(1000, self.update_ram_meter)

    def update_disc_data(self):
        """Update the disc data by updating meters."""
        disk_info = psutil.disk_usage('/')

        self.disc_usage['value'] = disk_info.percent
        self.disc_usage_value.config(text=f"{disk_info.percent:.2f}%")

        used_gb = disk_info.used / (1024 ** 3)
        self.disc_used['value'] = used_gb
        self.disc_used_value.config(text=f"{used_gb:.2f} GB")

        self.app.after(1000, self.update_disc_data)

    def quit_app(self):
        """Exit the application."""
        self.app.quit()
