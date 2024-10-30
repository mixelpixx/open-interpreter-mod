import psutil
import platform
import subprocess
import win32process

class Tools:
    def __init__(self, computer):
        self.computer = computer

    def get_process(self, name):
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == name:
                return proc.info
        return None

    def get_process_details(self, pid):
        """Get detailed process information."""
        try:
            process = psutil.Process(pid)
            details = {
                'name': process.name(),
                'status': process.status(),
                'cpu_percent': process.cpu_percent(),
                'memory_percent': process.memory_percent(),
                'create_time': process.create_time()
            }
            if platform.system() == "Windows":
                details['priority'] = win32process.GetPriorityClass(process.pid)
            return details
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None

    def run_command(self, command, shell=False):
        try:
            result = subprocess.run(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.CalledProcessError as e:
            return {
                'stdout': e.stdout,
                'stderr': e.stderr,
                'returncode': e.returncode
            }

    def get_system_info(self):
        return {
            'platform': platform.platform(),
            'architecture': platform.architecture(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'system': platform.system(),
            'version': platform.version()
        }
