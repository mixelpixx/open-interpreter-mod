import platform

class Tools:
    def __init__(self, computer):
        self.computer = computer
        self._system = platform.system()

    def find_process(self, process_name):
        """
        Find a running process by name.
        """
        import psutil
        for proc in psutil.process_iter(['name', 'exe']):
            try:
                if process_name.lower() in proc.info['name'].lower():
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return None

    def get_process_info(self, process):
        """
        Get detailed information about a process.
        """
        info = {
            'pid': process.pid,
            'name': process.name(),
            'exe': process.exe(),
            'cwd': process.cwd(),
            'user': process.username(),
            'cpu_percent': process.cpu_percent(),
            'memory_percent': process.memory_percent(),
            'connections': len(process.connections()),
            'threads': len(process.threads()),
            'children': [child.pid for child in process.children()]
        }
        return info

    def get_windows_services(self):
        """
        Get list of Windows services and their status.
        Windows-specific functionality.
        """
        if self._system != 'Windows':
            return None
            
        import wmi
        c = wmi.WMI()
        services = []
        for service in c.Win32_Service():
            services.append({
                'name': service.Name,
                'display_name': service.DisplayName,
                'status': service.State,
                'start_mode': service.StartMode
            })
        return services

    def get_network_connections(self):
        """
        Get information about active network connections.
        """
        import psutil
        connections = []
        for conn in psutil.net_connections():
            connections.append({
                'fd': conn.fd,
                'family': conn.family,
                'type': conn.type,
                'local_address': conn.laddr,
                'remote_address': conn.raddr,
                'status': conn.status,
                'pid': conn.pid
            })
        return connections

    def get_windows_registry_value(self, key_path, value_name):
        """
        Safely read a Windows registry value
        """
        if self._system != 'Windows':
            return None
            
        import winreg
        try:
            root_key = winreg.HKEY_LOCAL_MACHINE
            if key_path.startswith("HKEY_CURRENT_USER"):
                root_key = winreg.HKEY_CURRENT_USER
                key_path = key_path.replace("HKEY_CURRENT_USER\\", "")
            elif key_path.startswith("HKEY_LOCAL_MACHINE"):
                key_path = key_path.replace("HKEY_LOCAL_MACHINE\\", "")
                
            key = winreg.OpenKey(root_key, key_path, 0, winreg.KEY_READ)
            value, type_id = winreg.QueryValueEx(key, value_name)
            return value
        except WindowsError:
            return None
