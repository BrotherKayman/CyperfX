import platform
import psutil
from tkinter import Tk, filedialog, messagebox
from ttkbootstrap import Style
from ttkbootstrap.widgets import Treeview, Button
import webbrowser  # For opening the default email app
import subprocess
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Import libraries specific to each operating system
os_name = platform.system()



# Platform-specific imports
if os_name == "Windows":
    import wmi  # Only used on Windows
elif os_name in ["Linux", "Darwin"]:
    import subprocess  # Used for running commands on Linux and macOS

# Create the main application window
style = Style(theme="solar")
root = style.master
root.title("Computer Diagnostic Tool")

# Define column headers for the Treeview widget
columns = ("Component", "Health Status", "Details", "Potential Solutions")
treeview = Treeview(root, columns=columns, show="headings")
treeview.heading("Component", text="Component")
treeview.heading("Health Status", text="Health Status")
treeview.heading("Details", text="Details")
treeview.heading("Potential Solutions", text="Potential Solutions")

# Adjust column widths
treeview.column("Component", width=120)
treeview.column("Health Status", width=100)
treeview.column("Details", width=300)
treeview.column("Potential Solutions", width=300)

# Pack the Treeview widget to fill the window
treeview.pack(fill="both", expand=True)

# Define potential solutions for warnings
potential_solutions = {
    "High temperature": "Check CPU cooling system, clean heatsinks and fans.",
    "High usage": "Check for resource-intensive applications or processes.",
    "Driver updates needed": "Update drivers using the respective update tool.",
    "No network activity": "Check network connections and settings.",
    "High storage usage": "Clear unnecessary files and optimize storage."
}

# Function to add results to the Treeview
def add_result_to_treeview(component, health_status, details, solutions=""):
    """Add diagnostic result to the Treeview."""
    style_map = {"Good": "success", "Warning": "warning", "Error": "danger"}
    treeview.insert("", "end", values=(component, health_status, details, solutions), tags=(style_map.get(health_status, "success")))

    # Apply styles to rows
    treeview.tag_configure("success", background="#d4edda")
    treeview.tag_configure("danger", background="#f8d7da")
    treeview.tag_configure("warning", background="#fff3cd")

# Function to clear the Treeview before adding new results
def clear_treeview():
    """Clear the Treeview before refreshing diagnostics."""
    for item in treeview.get_children():
        treeview.delete(item)

# Define functions to check the health of each component based on the operating system

def check_cpu_health():
    """Check CPU health."""
    try:
        cpu_temp = psutil.sensors_temperatures().get("coretemp")
        if cpu_temp:
            cpu_temp_current = cpu_temp[0].current
            if cpu_temp_current > 80:  # Adjust threshold as needed
                add_result_to_treeview("CPU", "Warning", f"High temperature: {cpu_temp_current}°C", potential_solutions["High temperature"])
            else:
                add_result_to_treeview("CPU", "Good", f"Temperature: {cpu_temp_current}°C")
        else:
            add_result_to_treeview("CPU", "Good", "CPU temperature data not available")
    except Exception as e:
        add_result_to_treeview("CPU", "Error", f"Unable to check CPU health: {e}")

def check_memory_health():
    """Check memory health."""
    mem = psutil.virtual_memory()
    if mem.percent > 90:
        add_result_to_treeview("Memory", "Warning", f"High usage: {mem.percent}%", potential_solutions["High usage"])
    else:
        add_result_to_treeview("Memory", "Good", f"Usage: {mem.percent}%")

def check_storage_health():
    """Check storage health."""
    try:
        disks = psutil.disk_partitions()
        for disk in disks:
            usage = psutil.disk_usage(disk.mountpoint)
            if usage.percent > 90:
                add_result_to_treeview("Storage", "Warning", f"High usage on {disk.mountpoint}: {usage.percent}%", potential_solutions["High storage usage"])
            else:
                add_result_to_treeview("Storage", "Good", f"Usage on {disk.mountpoint}: {usage.percent}%")
    except Exception as e:
        add_result_to_treeview("Storage", "Error", f"Unable to check storage health: {e}")

def check_gpu_health():
    """Check GPU health."""
    try:
        os_name = platform.system()
        if os_name == "Windows":
            # Check GPU health on Windows using WMI
            c = wmi.WMI()
            gpus = c.Win32_VideoController()
            if not gpus:
                add_result_to_treeview("GPU", "Not Found", "No GPU found")
                return
            
            for gpu in gpus:
                if gpu.Status != "OK":
                    add_result_to_treeview("GPU", "Warning", f"Potential issue with GPU: {gpu.Caption} - Status: {gpu.Status}")
                else:
                    add_result_to_treeview("GPU", "Good", f"GPU: {gpu.Caption} - Status: OK")
        
        elif os_name in ["Linux", "Darwin"]:
            # Check GPU health on Linux and macOS
            command = None
            if os_name == "Linux":
                command = "nvidia-smi -q"  # For NVIDIA GPUs
            elif os_name == "Darwin":
                command = "system_profiler SPDisplaysDataType"  # For macOS

            if command:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result.returncode == 0 and ("NVIDIA" in result.stdout or "AMD" in result.stdout or "Intel" in result.stdout):
                    add_result_to_treeview("GPU", "Good", "GPU health is good")
                else:
                    add_result_to_treeview("GPU", "Not Found", "No GPU or unsupported GPU found")

    except Exception as e:
        add_result_to_treeview("GPU", "Error", f"Unable to check GPU health: {e}")

def check_network_health():
    """Check network health."""
    net_io = psutil.net_io_counters()
    if net_io.bytes_sent == 0 and net_io.bytes_recv == 0:
        add_result_to_treeview("Network", "No Activity", "No network activity detected", potential_solutions["No network activity"])
    else:
        add_result_to_treeview("Network", "Good", "Network health is good")

# Diagnostic functions for each operating system

def diagnose_windows():
    """Diagnose the Windows system and check drivers."""
    check_cpu_health()
    check_memory_health()
    check_storage_health()
    check_gpu_health()
    check_network_health()
    
    # Check for driver updates using WMI
    try:
        c = wmi.WMI()
        potential_issues = []
        for driver in c.Win32_PnPSignedDriver():
            potential_issues.append(
                f"Driver for {driver.DeviceName} (Provider: {driver.DriverProvider}) - Version: {driver.DriverVersion}"
            )
        
        if potential_issues:
            add_result_to_treeview("Drivers", "Warning", "Some drivers may need updating", potential_solutions["Driver updates needed"])
        else:
            add_result_to_treeview("Drivers", "Good", "All drivers are up-to-date")
    except Exception as e:
        add_result_to_treeview("Drivers", "Error", f"Unable to check driver updates: {e}")

def diagnose_linux():
    """Diagnose the Linux system and check drivers."""
    check_cpu_health()
    check_memory_health()
    check_storage_health()
    check_gpu_health()
    check_network_health()
    
    # Check for driver updates on Linux
    try:
        command = "apt list --upgradable"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if "No packages found" not in result.stdout:
            add_result_to_treeview("Drivers", "Warning", "Some drivers may need updating", potential_solutions["Driver updates needed"])
        else:
            add_result_to_treeview("Drivers", "Good", "All drivers are up-to-date")
    except Exception as e:
        add_result_to_treeview("Drivers", "Error", f"Unable to check driver updates: {e}")

def diagnose_mac():
    """Diagnose the macOS system and check drivers."""
    check_cpu_health()
    check_memory_health()
    check_storage_health()
    check_gpu_health()
    check_network_health()
    
    # Use the `softwareupdate` command to check for system and driver updates
    try:
        command = "softwareupdate --list"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if "No new software available" not in result.stdout:
            add_result_to_treeview("Drivers", "Good", "All drivers are up-to-date")
        else:
            add_result_to_treeview("Drivers", "Warning", "Some drivers may need updating", potential_solutions["Driver updates needed"])
    except Exception as e:
        add_result_to_treeview("Drivers", "Error", f"Unable to check driver updates: {e}")

# Main function to diagnose the computer based on the operating system

def diagnose_computer():
    """Diagnose the computer based on the operating system."""
    clear_treeview()
    os_name = platform.system()
    
    if os_name == "Windows":
        diagnose_windows()
    elif os_name == "Linux":
        diagnose_linux()
    elif os_name == "Darwin":
        diagnose_mac()
    else:
        add_result_to_treeview("Diagnosis", "Unsupported OS", "Unsupported operating system")

# Function to refresh diagnostics every second
def refresh_diagnostics():
    """Refresh diagnostic results every second."""
    diagnose_computer()
    root.after(1000, refresh_diagnostics)

# Function to display computer information
def display_computer_info():
    """Display computer information."""
    clear_treeview()
    os_name = platform.system()
    
    if os_name == "Windows":
        c = wmi.WMI()

        # CPU information
        cpu_info = c.Win32_Processor()[0]
        add_result_to_treeview("CPU Info", "", f"Type: {cpu_info.Name}\nManufacturer: {cpu_info.Manufacturer}\nGeneration: {cpu_info.Description}\nClock Speed: {cpu_info.MaxClockSpeed / 1000} GHz")
        
        # RAM information
        memory_info = psutil.virtual_memory()
        add_result_to_treeview("RAM Info", "", f"Size: {memory_info.total / 1024**3} GB\nType: {memory_info.type}")
        
        # Storage information
        disk_info = psutil.disk_partitions()
        for disk in disk_info:
            usage = psutil.disk_usage(disk.mountpoint)
            add_result_to_treeview("Storage Info", "", f"Type: {disk.fstype}\nSize: {usage.total / 1024**3} GB")
        
        # Add any other necessary information
        
    elif os_name == "Linux":
        # CPU information
        cpu_info = subprocess.check_output(['lscpu']).decode('utf-8')
        add_result_to_treeview("CPU Info", "", cpu_info)
        
        # RAM information
        memory_info = subprocess.check_output(['free', '-h']).decode('utf-8')
        add_result_to_treeview("RAM Info", "", memory_info)
        
        # Storage information
        disk_info = subprocess.check_output(['df', '-h']).decode('utf-8')
        add_result_to_treeview("Storage Info", "", disk_info)
        
        
    elif os_name == "Darwin":
        # Add macOS specific information retrieval
        pass

    # Now, diagnose the rest of the computer components
    diagnose_computer()

# Display computer information before diagnosing
display_computer_info()


# Function to convert Treeview data to a PDF file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def convert_treeview_to_pdf(file_path):
    """Convert Treeview data to a PDF file."""
    # Create a document with the specified file path
    doc = SimpleDocTemplate(file_path, pagesize=letter)

    # Prepare the data for the table
    data = []
    
    # Add the headers as the first row
    headers = [treeview.heading(col)["text"] for col in columns]
    data.append(headers)
    
    # Add the data from the Treeview to the data list
    for item in treeview.get_children():
        row_values = treeview.item(item)["values"]
        data.append(row_values)

    # Create a Table with the data
    table = Table(data)
    
    # Define a style for the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ])
    
    # Apply the style to the table
    table.setStyle(style)
    
    # Build the document with the table
    elements = [table]
    doc.build(elements)


# Function to send an email with a PDF attachment
def send_email_with_pdf():
    """Open the default email client with a PDF attachment."""
    # Ask the user to select a location to save the PDF
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if not file_path:
        return
    
    # Convert Treeview data to PDF
    convert_treeview_to_pdf(file_path)
    
    # Create a mailto URL with the attachment file path
    recipient = "kagisocreative@gmail.com"  # Add recipient email
    subject = "Computer Diagnostic Report"
    body = "Please find the attached computer diagnostic report."
    
    # Create mailto URL
    mailto_url = f"mailto:{recipient}?subject={subject}&body={body}&attachment={file_path}"
    
    # Open the mailto URL in the default email client
    webbrowser.open(mailto_url)


def save_pdf_only():
    """Save the PDF file without sending it via email."""
    # Ask the user to select a location to save the PDF
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if not file_path:
        return
    
    # Convert Treeview data to PDF
    convert_treeview_to_pdf(file_path)
    print(f"PDF saved at: {file_path}")

# Create a button to send an email with a PDF attachment
send_email_button = Button(root, text="Send Email with PDF", command=send_email_with_pdf)
send_email_button.pack(side="left", padx=5)

# Create a button to save the PDF only
save_pdf_button = Button(root, text="Save PDF", command=save_pdf_only)
save_pdf_button.pack(side="left", padx=5)

# Start the diagnostic process and main loop
refresh_diagnostics()
root.mainloop()
