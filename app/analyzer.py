import psutil
import os
import platform
import datetime

class SystemAnalyzer:
    """System analyzer class to collect system information safely."""

    @staticmethod
    def get_system_info():
        """Get general system information as a dictionary."""
        info = {
            "os": platform.system(),
            "os_release": platform.release(),
            "os_version": platform.version(),
            "hostname": platform.node(),
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage(os.path.abspath(os.sep)).percent,
            "boot_time": datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        }
        return info

    @staticmethod
    def get_open_ports():
        """Safe local port visibility check using psutil. Returns a list of dicts."""
        open_ports = []
        try:
            connections = psutil.net_connections(kind='inet')
            for conn in connections:
                if conn.status == 'LISTEN':
                    port_info = {
                        "port": conn.laddr.port,
                        "address": f"{conn.laddr.ip}:{conn.laddr.port}",
                        "status": conn.status,
                        "pid": conn.pid or "N/A"
                    }
                    if conn.pid:
                        try:
                            proc = psutil.Process(conn.pid)
                            port_info["process_name"] = proc.name()
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            port_info["process_name"] = "Unknown"
                    else:
                        port_info["process_name"] = "N/A"
                    open_ports.append(port_info)
        except (psutil.AccessDenied, PermissionError):
            return [{"error": "Access denied to network connections. Check permissions."}]
        return sorted(open_ports, key=lambda x: x['port'])

    @staticmethod
    def get_top_processes():
        """Get top processes by CPU/memory usage. Returns a list of dicts."""
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        except Exception:
            return []
        top_cpu = sorted(processes, key=lambda x: (x['cpu_percent'], x['memory_percent']), reverse=True)[:10]
        return top_cpu

    @staticmethod
    def analyze_resource_usage():
        """Analyze resource usage and flag unusual spikes."""
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        flags = []
        if cpu > 80:
            flags.append("High CPU usage detected (>80%). Check for resource-intensive processes.")
        if mem > 90:
            flags.append("High memory usage detected (>90%). Your system may experience performance issues.")
        return {"cpu": cpu, "memory": mem, "flags": flags}