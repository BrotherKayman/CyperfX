#!/usr/bin/python

import psutil
import ttkbootstrap as ttkB
from PIL import Image
import subprocess
from tkinter import PhotoImage
from datetime import datetime
from disc_management import DiscManager
Image.CUBIC = Image.BICUBIC
class SystemMonitorApp:
    """Class to manage CyperfX
    This module monitors system performance/ utilization
    """
    
    def __init__(self):
        """Initialize the application window and components."""
        self.app = ttkB.Window(themename='solar')
        self.app.title('Cyperfx')
        img = PhotoImage(file='icon.png')
        self.app.iconphoto(False, img)
        self.app.geometry('770x550')
        self.app.minsize(height=550, width=770)
        self.app.maxsize(height=550, width=770)

        # Initialize UI components
        self.create_gui()

        # Instantiate the DiscManager class (no arguments required)
        self.disc_manager = DiscManager()

        # Start monitoring functions
        self.update_cpu_meter()
        self.update_ram_meter()

        # Start monitoring disc data
        self.update_disc_data()

        # Start the main event loop
        self.app.mainloop()

    def create_gui(self):
        """Create the GUI components."""
        # Create main page label
        self.page_name = ttkB.Label(self.app, text='System Monitor', font='bold 15')
        self.page_name.place(x=300, y=5)

        # Create frames for CPU, RAM, and disc usage
        self.create_cpu_frame()
        self.create_disc_frame()
        self.create_footer()

        # Create buttons
        self.create_buttons()

    def create_cpu_frame(self):
        """Create the CPU & RAM usage frame."""
        self.cpu_frame = ttkB.LabelFrame(self.app, text='CPU & RAM Usage', height=170, width=325)
        self.cpu_frame.place(x=50, y=40)

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

        # Create RAM meter
        self.ram_meter = ttkB.Meter(
            self.cpu_frame,
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
        self.ram_meter.place(x=200, y=10)

    def create_disc_frame(self):
        """Create the disc usage frame."""
        self.disc_frame = ttkB.LabelFrame(self.app, text='Disc Usage', height=250, width=650)
        self.disc_frame.place(x=50, y=220)

        # Create disc free meter
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
        """Create the watermark with the author's name."""
        self.waterMark = ttkB.Label(text='Kagiso Motlhaoleng', font='Helvetica 20 bold')
        self.waterMark.place(x=400, y=110)
        self.waterMark = ttkB.Label(text='ALX Africa C18', font='Helvetica 10')
        self.waterMark.place(x=400, y=150)

    def create_buttons(self):
        """Create buttons for the application."""
        self.buttons = ttkB.Frame(self.app)
        self.buttons.place(x=50, y=500, width=670, height=50)

        # Create exit button
        self.exit_button = ttkB.Button(
            self.buttons,
            text='Exit',
            command=self.quit_app,
            underline=0,
            style='info.Outline.TButton'
        )
        self.exit_button.place(x=0, y=0)

        # Create malware scan button
        self.malware_scan = ttkB.Button(
            self.buttons,
            text='Scan Malware',
            underline=0,
            style='warning.TButton',
            command=self.run_malware_scan
        )
        self.malware_scan.place(x=535, y=0)

        # Create disc manager button
        self.new_button = ttkB.Button(
            self.buttons,
            text='Clean Disc',
            command=self.start_disc_manager,
            underline=0,
            style='primary.Outline.TButton'
        )
        self.new_button.place(x=415, y=0)
#------------------------EVENT FUNCTIONS-------------------------#
#------------------------EVENT FUNCTIONS-------------------------#
#------------------------EVENT FUNCTIONS-------------------------#
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

if __name__ == '__main__':
    app = SystemMonitorApp()
