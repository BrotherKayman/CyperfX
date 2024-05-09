import platform
import psutil
from ttkbootstrap import Style
from ttkbootstrap.widgets import Treeview
from tkinter import messagebox
import subprocess

# Import appropriate libraries based on the operating system
os_name = platform.system()
if os_name == "Windows":
    import wmi  # Only used on Windows
elif os_name in ["Linux", "Darwin"]:
    import subprocess  # Used for running commands on Linux and macOS

# Create the main application window
style = Style(theme="cyborg")
root = style.master
root.title("Computer Diagnostic Tool")

# Define column headers for the Treeview widget
columns = ("Component", "Health Status", "Details")
treeview = Treeview(root, columns=columns, show="headings")
treeview.heading("Component", text="Component")
treeview.heading("Health Status", text="Health Status")
treeview.heading("Details", text="Details")

# Adjust column widths
treeview.column("Component", width=120)
treeview.column("Health Status", width=100)
treeview.column("Details", width=300)

# Pack the Treeview widget to fill the window
treeview.pack(fill="both", expand=True)

# Add a function to insert results into the Treeview
def add_result_to_treeview(component, health_status, details):
    """Add diagnostic result to the Treeview."""
    # Apply bootstyle based on health status
    style_map = {"Good": "success", "Warning": "warning", "Error": "danger"}
    treeview.insert("", "end", values=(component, health_status, details), tags=(style_map.get(health_status, "success"),))

    # Apply style to rows
    treeview.tag_configure("success", background="#d4edda")
    treeview.tag_configure("danger", background="#f8d7da")
    treeview.tag_configure("warning", background="#fff3cd")

# Define functions for checking the health of each component

def check_cpu_health():
    """Check CPU health."""
    try:
        # Check CPU temperature
        cpu_temp = psutil.sensors_temperatures().get("coretemp")
        if cpu_temp:
            cpu_temp_current = cpu_temp[0].current
            if cpu_temp_current > 80:  # Adjust threshold as needed
                add_result_to_treeview("CPU", "Warning", f"High temperature: {cpu_temp_current}°C")
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
        add_result_to_treeview("Memory", "Warning", f"High usage: {mem.percent}%")
    else:
        add_result_to_treeview("Memory", "Good", f"Usage: {mem.percent}%")

def check_storage_health():
    """Check storage health."""
    try:
        disks = psutil.disk_partitions()
        for disk in disks:
            usage = psutil.disk_usage(disk.mountpoint)
            if usage.percent > 90:
                add_result_to_treeview("Storage", "Warning", f"High usage on {disk.mountpoint}: {usage.percent}%")
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
                command = "nvidia-smi -q"  # For NVIDIA GPUs, adjust for other GPU brands
            elif os_name == "Darwin":
                command = "system_profiler SPDisplaysDataType"
            
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
        add_result_to_treeview("Network", "No Activity", "No network activity detected")
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
            add_result_to_treeview("Drivers", "Warning", "Some drivers may need updating")
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
            add_result_to_treeview("Drivers", "Warning", "Some drivers may need updating")
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
            add_result_to_treeview("Drivers", "Warning", "Some drivers may need updating")
    except Exception as e:
        add_result_to_treeview("Drivers", "Error", f"Unable to check driver updates: {e}")

# Main function to diagnose the computer based on the operating system

def diagnose_computer():
    """Diagnose the computer based on the operating system."""
    os_name = platform.system()
    
    if os_name == "Windows":
        diagnose_windows()
    elif os_name == "Linux":
        diagnose_linux()
    elif os_name == "Darwin":
        diagnose_mac()
    else:
        add_result_to_treeview("Diagnosis", "Unsupported OS", "Unsupported operating system")

# Start the diagnostic process and main loop
diagnose_computer()
root.mainloop()
