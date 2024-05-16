import tkinter as tk
from tkinter import ttk
import psutil
from PIL import Image
import ttkbootstrap as ttkB
import platform
import subprocess

Image.CUBIC = Image.BICUBIC

class Cyperfx:
    def __init__(self):
        """Initialize App window and Components"""
        self.disc_clean_tab = None
        self.sys_monitor_tab = None
        self.temperature_meter = None 

    def App(self):
        self.app = ttkB.Window(themename='superhero')
        self.app.title('CyperfX')
        self.app.geometry('800x700')
        self.app.maxsize(width=860, height=650)
        self.app.minsize(width=860, height=650)

        # GUI Function Calls
        self.create_gui()
        self.create_buttons()
        self.update_cpu_meter()
        self.update_ram_meter()
        self.update_system_temperature()
        self.update_disc_data()

        # Start the application
        self.app.mainloop()

    def create_gui(self):
        # Create main panel
        self.main_panel = tk.PanedWindow(self.app, width=1200, height=650, bg='#17a2b8')
        self.main_panel.place(x=0, y=0, width=1200)

        # Create Frame for tabs
        self.monitor_tabs = ttkB.Frame(self.app, height=500, width=700, style='info.Frame')
        self.monitor_tabs.place(x=150, y=80)

        # Sys Monitor
        self.sys_monitor_tab = ttkB.Frame(self.monitor_tabs)
        self.sys_monitor_tab.place(relwidth=1, relheight=1)

        # Create CPU & RAM Usage in System Monitor tab
        self.usage = ttkB.Frame(self.sys_monitor_tab, height=200, width=600)
        self.usage.place(x=70, y=50)

        self.title = ttk.Label(self.sys_monitor_tab, text='CPU and RAM Use')
        self.title.place(x=10, y=10)

        # Create CPU meter
        self.cpu_meter = ttkB.Meter(
            self.usage,
            metersize=150,
            bootstyle='',
            stripethickness=20,
            amounttotal=100,
            subtext='CPU Usage',
            textright='%',
            subtextfont='Helvetica 8',
            interactive=False,
            metertype='full'
        )
        self.cpu_meter.place(x=10, y=15)

        # Create RAM meter
        self.ram_meter = ttkB.Meter(
            self.usage,
            metersize=150,
            bootstyle='',
            stripethickness=20,
            amounttotal=100,
            subtext='RAM Usage',
            textright='%',
            subtextfont='Helvetica 8',
            interactive=False,
            metertype='full'
        )
        self.ram_meter.place(x=200, y=15)

        # Create Temperature meter
        self.temperature_meter = ttkB.Meter(
            self.usage,
            metersize=150,
            bootstyle='',
            stripethickness=20,
            amounttotal=100,
            subtext='Temperature',
            textright='°C', 
            subtextfont='Helvetica 8',
            interactive=False,
            metertype='full'
        )
        self.temperature_meter.place(x=390, y=15)
        
        # Create Canvas for the line
        self.canvas = tk.Canvas(self.sys_monitor_tab, width=550, height=2, bg='#17a2b8', highlightthickness=0)
        self.canvas.place(x=110, y=260)
        # Draw a line on the Canvas
        self.canvas.create_line(0, 1, 650, 1, fill='white')
        
        #------------------------------------------------------------------------
        # Add Disc frame
        self.disc_frame = ttkB.Frame(self.sys_monitor_tab, height=250, width=650)
        self.disc_frame.place(x=70, y=270)

        self.label_title = ttkB.Label(self.sys_monitor_tab, text='Disc Monitor')
        self.label_title.place(x=10, y=250)

        # Create disc free meter
        self.disc_free = ttkB.Meter(
            self.disc_frame,
            metersize=160,
            bootstyle='',
            stripethickness=20,
            amounttotal=10,
            subtext='Disc Available',
            textright='GB', 
            subtextfont='Helvetica 8',
            interactive=False,
            metertype='full'
        )
        self.disc_free.place(x=10, y=35)
        
        # Create disc usage progress bar and label
        self.disc_usage_label = ttkB.Label(
            self.disc_frame,
            text='Disc Usage'
        )
        self.disc_usage_label.place(x=230, y=135)
        
        # Create disc usage progress bar
        self.disc_usage = ttkB.Progressbar(
            self.disc_frame,
            style='info.Horizontal.TProgressBar',
            length=200,
            value=psutil.disk_usage('/').percent
        )
        self.disc_usage.place(x=310, y=130, height=30)

        # Create disc usage value label
        self.disc_usage_value = ttkB.Label(
            self.disc_frame,
            text=f'{self.disc_usage["value"]:.2f}%'
        )
        self.disc_usage_value.place(x=520, y=135)

        # Create disc used label and progress bar
        self.disc_used_label = ttkB.Label(
            self.disc_frame,
            text='Disc Used'
        )
        self.disc_used_label.place(x=230, y=85)

        self.disc_used = ttkB.Progressbar(
            self.disc_frame,
            style='info.Horizontal.TProgressBar',
            length=200,
            value=0
        )
        self.disc_used.place(x=310, y=85, height=30)

        self.disc_used_value = ttkB.Label(
            self.disc_frame,
            text='0.00 GB'
        )
        self.disc_used_value.place(x=520, y=85)
      
        # Initially show the System Monitor tab
        self.show_sys_monitor()

    def create_buttons(self):
        # Create Sys Monitor buttons
        self.sys_monitor_button = ttkB.Button(self.app, text='\nSystem Monitor', style='info', command=self.show_sys_monitor)
        self.sys_monitor_button.place(y=100, x=10, height=100, width=140)

        self.disc_clean_button = ttkB.Button(self.app, text='\nDisc Cleaner', style='info.TButton',
                                             command=self.show_disc_clean)
        self.disc_clean_button.place(y=190, x=10, height=100, width=140)

        self.mal_scanner_button = ttkB.Button(self.app, text='\nMalware Scanner', style='info.TButton',
                                              command=self.show_mal_scan)
        self.mal_scanner_button.place(y=280, x=10, height=100, width=140)

        self.diagnose_button = ttkB.Button(self.app, text='\nDiagnose', style='info.TButton', command=self.diagnose)
        self.diagnose_button.place(y=370, x=10, height=100, width=140)

        self.tech_button = ttkB.Button(self.app, text='\nTech Help', style='info.TButton', command=self.tech_help) 
        self.tech_button.place(y=460, x=10, height=100, width=140)
        
        self.exit_button = ttkB.Button(self.app, text='Exit', style='danger', command=self.quit_app)
        self.exit_button.place(y=600, x=800)

    def update_cpu_meter(self):
        """Update the CPU meter."""
        cpu_percent = psutil.cpu_percent()
        self.cpu_meter['amountused'] = cpu_percent
        if cpu_percent >= 70.00:
            self.cpu_meter.configure(bootstyle='danger')
        elif cpu_percent >= 50.00:
            self.cpu_meter.configure(bootstyle='warning')
        else:
            self.cpu_meter.configure(bootstyle='success')
        self.app.after(1000, self.update_cpu_meter)

    def update_ram_meter(self):
        """Update the RAM meter"""
        ram_percent = psutil.virtual_memory().percent
        self.ram_meter['amountused'] = ram_percent
        if ram_percent >= 70.00:
            self.ram_meter.configure(bootstyle='danger')
        elif ram_percent >= 50.00:
            self.ram_meter.configure(bootstyle='warning')
        else:
            self.ram_meter.configure(bootstyle='success')
        self.app.after(1000, self.update_ram_meter)

    def update_system_temperature(self):
        """Update the system temperature."""
        temperature = self.get_system_temperature()
        if temperature is not None:
            try:
                temperature = float(temperature)
                self.temperature_meter['amountused'] = temperature
            except ValueError:
                print("Error: Temperature is not a valid float.")
        else:
            print("Error: Unable to retrieve system temperature.")
        self.app.after(1000, self.update_system_temperature)  # Schedule next update

    def get_system_temperature(self):
        """Get the system temperature."""
        system = platform.system()
        try:
            if system == 'Linux':
                # Run the 'sensors' command to get temperature information (Linux-specific)
                output = subprocess.check_output(['sensors'])
                # Parse the output to extract temperature information
                temperature_info = output.decode('utf-8').split('\n')
                temperature = None
                for line in temperature_info:
                    if 'Core' in line:  # Example: 'Core 0:        +50.0°C  (high = +95.0°C, crit = +105.0°C)'
                        temperature_str = line.split(':')[1].strip().split()[0]
                        temperature = float(temperature_str[:-2])  # Extract numeric part and convert to float
                        break
                return temperature
            elif system == 'Windows':
                return "Temperature retrieval not implemented for Windows."
            elif system == 'Darwin':  # macOS
                return "Temperature retrieval not implemented for macOS."
            else:
                return "Unsupported operating system."
        except Exception as e:
            return "Error retrieving system temperature: {}".format(e)
    
    def update_disc_data(self):
        """Update the disc data by updating meters."""
        disk_info = psutil.disk_usage('/')

        # Update the free space meter
        free_gb = disk_info.free / (1024 ** 3)
        self.disc_free['amounttotal'] = disk_info.total / (1024 ** 3)
        self.disc_free['amountused'] = f'{free_gb:.2f}'

        self.disc_usage['value'] = disk_info.percent
        self.disc_usage_value.config(text=f"{disk_info.percent:.2f}%")

        used_gb = disk_info.used / (1024 ** 3)
        self.disc_used['value'] = used_gb
        self.disc_used_value.config(text=f"{used_gb:.2f} GB")

        self.app.after(1000, self.update_disc_data)


    def quit_app(self):
        """Exit the application."""
        self.app.quit()

    def show_sys_monitor(self):
        """Show System Monitor (CPU & RAM Usage)"""
        self.sys_monitor_tab.lift()
        self.sys_monitor_tab.update()

    def show_disc_clean(self):
        """Show Disc Cleaner"""
        subprocess.run(['python3','disc_cleaner.py'])

    def show_mal_scan(self):
        """Show Malware Scanner"""
        subprocess.run(['python3','malware_scanner.py'])

    def diagnose(self):
        subprocess.run(['python3', 'diagnoseTool.py'])

    def tech_help(self):
        subprocess.run(['python3','tech_help.py'])
        
if __name__ == '__main__':
    app = Cyperfx()
    app.App()
