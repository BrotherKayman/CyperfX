"""Read-only local system snapshot for CyperfX Version 2."""
import json
import platform
import socket
from datetime import datetime, timezone
import psutil

def gb(value):
    return round(value / (1024 ** 3), 2)

def collect_snapshot():
    vm = psutil.virtual_memory()
    disks, seen = [], set()
    for part in psutil.disk_partitions(all=False):
        if part.mountpoint in seen:
            continue
        seen.add(part.mountpoint)
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except (PermissionError, OSError):
            continue
        disks.append({
            "mountpoint": part.mountpoint, "filesystem": part.fstype or "",
            "total_gb": gb(usage.total), "free_gb": gb(usage.free),
            "used_percent": round(usage.percent, 1)
        })
    try:
        battery = psutil.sensors_battery()
    except (AttributeError, OSError):
        battery = None
    cpu = psutil.cpu_percent(interval=0.4)
    notes = []
    if vm.percent >= 90:
        notes.append("Memory use is high (%.0f%%). Check active applications and memory pressure." % vm.percent)
    if cpu >= 90:
        notes.append("CPU use was high during this short sample (%.0f%%). Repeat the test to confirm." % cpu)
    for disk in disks:
        if disk["used_percent"] >= 90:
            notes.append("Storage on %s is nearly full (%.0f%% used)." % (disk["mountpoint"], disk["used_percent"]))
    return {
        "computer_name": socket.gethostname(), "operating_system": platform.system(),
        "os_release": platform.release(), "processor": platform.processor() or platform.machine() or "Unknown",
        "logical_processors": psutil.cpu_count(logical=True) or 0, "cpu_percent": cpu,
        "memory_total_gb": gb(vm.total), "memory_available_gb": gb(vm.available),
        "memory_percent": round(vm.percent, 1), "disks": disks,
        "battery_percent": round(battery.percent) if battery else None,
        "battery_plugged_in": bool(battery.power_plugged) if battery else None,
        "collected_at": datetime.now(timezone.utc).isoformat(), "notes": notes
    }

if __name__ == "__main__":
    print(json.dumps(collect_snapshot(), ensure_ascii=False))
