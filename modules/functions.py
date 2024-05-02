from main import *
import psutil

from tkinter import filedialog, messagebox
import os
from malware_scan import clamd
from malware_scan import scan_info


scan_info.config(text="This is new information")
#functions
#-------Malware Scan


def scan_file(file_path):
    
    result = clamd.scan_file(file_path)
    if result[file_path][0] == 'FOUND':
        messagebox.showwarning("Malware Detected", f"Malware found in file: {file_path}\nType: {result[file_path][1]}")
    else:
        
        print(f"No malware found in file: {file_path}")

# Function to scan a directory
def scan_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            scan_file(file_path)


def full_scan():
    root_path = os.path.abspath('/')
    scan_directory(root_path)

def choose_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        scan_directory(directory_path)

#---------------

def processes():
    for proc in psutil.process_iter():
        try:
            
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'status'])
            app.after(1000, print(pinfo))
        except psutil.NoSuchProcess:

            pass
        else:
            print(pinfo)

def quit():
    app.quit()
#cpu



#Network
def network_data():
    network_sent = psutil.net_io_counters().bytes_sent 
    network_received = psutil.net_io_counters().bytes_recv
    print(f'bytes received: {network_received}')

