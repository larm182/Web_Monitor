
import psutil

def get_system_metrics():
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "net_sent": psutil.net_io_counters().bytes_sent,
        "net_recv": psutil.net_io_counters().bytes_recv
    }

def get_top_processes(limit=5):
    processes = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent"]):
        try:
            processes.append(p.info)
        except psutil.NoSuchProcess:
            continue
    sorted_procs = sorted(processes, key=lambda x: x["cpu_percent"], reverse=True)
    return sorted_procs[:limit]
