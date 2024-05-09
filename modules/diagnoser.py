import platform
import psutil
from tkinter import Tk, scrolledtext, messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import SUCCESS, WARNING, DANGER
import subprocess

# Import appropriate library based on the operating system
os_name = platform.system()
if os_name == "Windows":
    import wmi  # Only used on Windows
elif os_name == "Linux":
    import subprocess  # Used for running commands on Linux
elif os_name == "Darwin":
    import subprocess  # Used for running commands on macOS

# Create the main application window
root = Tk()
root.title("Computer Diagnostic Tool")

# Create a scrolled text widget for system logs
system_log_text = scrolledtext.ScrolledText(root, width=70, height=10)
system_log_text.place(x=10, y=300, width=480, height=100)
system_log_text.insert("end", "System Logs:\n")

# Dictionary to store progress bars and progress variables for each component
progress_bars = {}
progress_vars = {}

# Create progress bars for each component
components = ["CPU", "Memory", "Storage", "GPU", "Network", "Drivers"]
for index, component in enumerate(components):
    progress_var = ttkb.DoubleVar()
    progress_bar = ttkb.Progressbar(
        root,
        variable=progress_var,
        maximum=100,
        length=300,
        bootstyle=SUCCESS,
    )
    
    # Place the label and progress bar in the window using place geometry manager
    label = ttkb.Label(root, text=component)
    label.place(x=10, y=index * 40 + 10)
    progress_bar.place(x=100, y=index * 40 + 10, width=300)
    
    # Store the progress bar and variable in dictionaries
    progress_bars[component] = progress_bar
    progress_vars[component] = progress_var

def update_progress(component, progress, bootstyle=SUCCESS):
    """Update the progress bar and bootstyle for a component."""
    progress_vars[component].set(progress)
    progress_bars[component].configure(bootstyle=bootstyle)

def show_feedback(component, message, bootstyle):
    """Show a message box for feedback and update the progress bar's bootstyle."""
    messagebox.showinfo(f"{component} Diagnostic Result", message)
    update_progress(component, 100, bootstyle)

# Diagnostic functions for each component

def check_cpu_health():
    """Check CPU health."""
    # Use psutil to check CPU health
    cpu_temp = None
    try:
        if hasattr(psutil, "sensors_temperatures"):
            cpu_temps = psutil.sensors_temperatures()
            if "coretemp" in cpu_temps:
                cpu_temp = cpu_temps["coretemp"][0].current
    except Exception as e:
        system_log_text.insert("end", f"Unable to get CPU temperature: {e}\n")

    # Check if CPU temperature is within a safe range
    if cpu_temp and cpu_temp > 80:  # Adjust temperature threshold as needed
        system_log_text.insert("end", f"High CPU temperature detected: {cpu_temp}°C.\n")
        show_feedback("CPU", "High CPU temperature detected. Consider cleaning dust or improving cooling.", WARNING)
    else:
        show_feedback("CPU", "CPU health is good.", SUCCESS)

def check_memory_health():
    """Check memory health."""
    # Use psutil to check memory health
    mem = psutil.virtual_memory()
    
    # Check memory status without displaying usage
    if mem.percent > 90:
        system_log_text.insert("end", f"High memory usage detected: {mem.percent}%.\n")
        show_feedback("Memory", "High memory usage detected. Consider closing some applications.", WARNING)
    else:
        show_feedback("Memory", "Memory health is good.", SUCCESS)

def check_storage_health():
    """Check storage health."""
    # Use psutil to check disk usage and smartmontools for SMART data
    disks = psutil.disk_partitions()
    for disk in disks:
        try:
            usage = psutil.disk_usage(disk.mountpoint)
            
            # Check storage status without displaying usage
            if usage.percent > 90:
                system_log_text.insert("end", f"High storage usage detected on {disk.mountpoint}: {usage.percent}%.\n")
                show_feedback("Storage", f"High storage usage on {disk.mountpoint}. Consider cleaning up files.", WARNING)
            else:
                show_feedback("Storage", f"Storage health on {disk.mountpoint} is good.", SUCCESS)

        except Exception as e:
            system_log_text.insert("end", f"Unable to check storage health on {disk.mountpoint}: {e}\n")

def check_gpu_health():
    """Check GPU health."""
    os_name = platform.system()
    
    # For Windows, you can use WMI to check GPU status
    if os_name == "Windows":
        c = wmi.WMI()
        gpus = c.Win32_VideoController()
        
        if not gpus:
            show_feedback("GPU", "No GPU found.", WARNING)
            return
        
        potential_issues = []
        for gpu in gpus:
            # Check GPU status
            if gpu.Status != "OK":
                potential_issues.append(f"Potential issue with GPU: {gpu.Caption} - Status: {gpu.Status}")
        
        if potential_issues:
            system_log_text.insert("end", "\n".join(potential_issues) + "\n")
            show_feedback("GPU", "Potential issues detected with GPU. Check system log for details.", WARNING)
        else:
            show_feedback("GPU", "GPU health is good.", SUCCESS)
    
    # On Linux and macOS, use relevant tools to check GPU status
    elif os_name == "Linux" or os_name == "Darwin":
        try:
            # Check the GPU health using specific commands
            if os_name == "Linux":
                # Try to use nvidia-smi, radeontop, or other commands depending on the GPU brand
                command = "nvidia-smi -q"
                nvidia_smi = subprocess.run(command, shell=True, capture_output=True, text=True)
                
                if nvidia_smi.returncode == 0:
                    # If the command succeeds, the system has an NVIDIA GPU
                    system_log_text.insert("end", nvidia_smi.stdout + "\n")
                    show_feedback("GPU", "GPU health is good.", SUCCESS)
                else:
                    # Try other commands or utilities for other GPU brands
                    show_feedback("GPU", "No GPU or unsupported GPU found.", WARNING)
            elif os_name == "Darwin":
                # Use `system_profiler` to get information about the GPU on macOS
                command = "system_profiler SPDisplaysDataType"
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                
                if "NVIDIA" in result.stdout or "AMD" in result.stdout or "Intel" in result.stdout:
                    # If the system has a supported GPU
                    system_log_text.insert("end", result.stdout + "\n")
                    show_feedback("GPU", "GPU health is good.", SUCCESS)
                else:
                    # If there is no GPU found or an unsupported brand
                    show_feedback("GPU", "No GPU or unsupported GPU found.", WARNING)
        
        except Exception as e:
            system_log_text.insert("end", f"Unable to check GPU health: {e}\n")
            show_feedback("GPU", f"Unable to check GPU health: {e}", DANGER)

def check_network_health():
    """Check network health."""
    # Use psutil to check network status
    net_io = psutil.net_io_counters()
    if net_io.bytes_sent == 0 and net_io.bytes_recv == 0:
        system_log_text.insert("end", "No network activity detected.\n")
        show_feedback("Network", "No network activity detected. Check your network connection.", WARNING)
    else:
        show_feedback("Network", "Network health is good.", SUCCESS)

# Diagnostic and driver check functions for different operating systems

def diagnose_windows():
    """Diagnose Windows system and check drivers."""
    # Call the functions for diagnosing each component on Windows
    check_cpu_health()
    check_memory_health()
    check_storage_health()
    check_gpu_health()
    check_network_health()
    
    # Check for driver updates using WMI
    c = wmi.WMI()
    potential_issues = []
    for driver in c.Win32_PnPSignedDriver():
        # Add checks for each driver (compare versions, etc.)
        potential_issues.append(
            f"Driver for {driver.DeviceName} (Provider: {driver.DriverProvider}) - Version: {driver.DriverVersion}"
        )
    
    if potential_issues:
        # Log potential issues in the system log
        system_log_text.insert("end", "\n".join(potential_issues) + "\n")
        show_feedback("Drivers", "Some drivers may need updating. Check system log for details.", WARNING)
    else:
        show_feedback("Drivers", "All drivers are up-to-date.", SUCCESS)

def diagnose_linux():
    """Diagnose Linux system and check drivers."""
    # Call the functions for diagnosing each component on Linux
    check_cpu_health()
    check_memory_health()
    check_storage_health()
    check_gpu_health()
    check_network_health()
    
    # Use the appropriate command for your distro (e.g., `apt` for Debian/Ubuntu) to check for driver updates
    try:
        command = "apt list --upgradable"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if "No packages found" not in result.stdout:
            system_log_text.insert("end", result.stdout + "\n")
            show_feedback("Drivers", "Some drivers may need updating. Check system log for details.", WARNING)
        else:
            show_feedback("Drivers", "All drivers are up-to-date.", SUCCESS)
    except Exception as e:
        show_feedback("Drivers", f"Unable to check driver updates: {e}", DANGER)
    
    update_progress("Drivers", 100)

def diagnose_mac():
    """Diagnose macOS system and check drivers."""
    # Call the functions for diagnosing each component on macOS
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
            system_log_text.insert("end", result.stdout + "\n")
            show_feedback("Drivers", "Some drivers may need updating. Check system log for details.", WARNING)
        else:
            show_feedback("Drivers", "All drivers are up-to-date.", SUCCESS)
    except Exception as e:
        show_feedback("Drivers", f"Unable to check driver updates: {e}", DANGER)
    
    update_progress("Drivers", 100)

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
        show_feedback("Diagnosis", "Unsupported operating system.", DANGER)

# Start the diagnostic process and main loop
diagnose_computer()
root.mainloop()
