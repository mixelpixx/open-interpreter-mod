import os
import platform
import winreg
import wmi
import win32api
import win32con
import win32security
import win32service
import win32serviceutil

class WindowsTools:
    """Windows-specific system tools and utilities."""
    
    def __init__(self):
        self._wmi = wmi.WMI()
    
    def get_windows_version(self):
        """Get detailed Windows version information."""
        return {
            'version': platform.version(),
            'release': platform.release(),
            'build': platform.win32_ver()[1],
            'architecture': platform.machine()
        }
    
    def get_services(self):
        """Get list of Windows services and their status."""
        services = []
        for service in self._wmi.Win32_Service():
            services.append({
                'name': service.Name,
                'display_name': service.DisplayName,
                'status': service.State,
                'start_mode': service.StartMode,
                'path': service.PathName
            })
        return services
    
    def manage_service(self, service_name, action='status'):
        """Manage Windows services (start/stop/restart/status)."""
        try:
            if action == 'status':
                return win32serviceutil.QueryServiceStatus(service_name)[1]
            elif action == 'start':
                win32serviceutil.StartService(service_name)
                return "Service started successfully"
            elif action == 'stop':
                win32serviceutil.StopService(service_name)
                return "Service stopped successfully"
            elif action == 'restart':
                win32serviceutil.RestartService(service_name)
                return "Service restarted successfully"
        except Exception as e:
            return f"Error managing service: {str(e)}"
    
    def get_registry_value(self, key_path, value_name):
        """Safely read a Windows registry value."""
        try:
            root_key = winreg.HKEY_LOCAL_MACHINE
            if key_path.startswith("HKEY_CURRENT_USER"):
                root_key = winreg.HKEY_CURRENT_USER
                key_path = key_path.replace("HKEY_CURRENT_USER\\", "")
            elif key_path.startswith("HKEY_LOCAL_MACHINE"):
                key_path = key_path.replace("HKEY_LOCAL_MACHINE\\", "")
                
            key = winreg.OpenKey(root_key, key_path, 0, winreg.KEY_READ)
            value, type_id = winreg.QueryValueEx(key, value_name)
            return {'value': value, 'type': type_id}
        except WindowsError as e:
            return {'error': str(e)}
    
    def set_registry_value(self, key_path, value_name, value, value_type=winreg.REG_SZ):
        """Safely write a Windows registry value."""
        try:
            root_key = winreg.HKEY_LOCAL_MACHINE
            if key_path.startswith("HKEY_CURRENT_USER"):
                root_key = winreg.HKEY_CURRENT_USER
                key_path = key_path.replace("HKEY_CURRENT_USER\\", "")
            elif key_path.startswith("HKEY_LOCAL_MACHINE"):
                key_path = key_path.replace("HKEY_LOCAL_MACHINE\\", "")
                
            key = winreg.CreateKey(root_key, key_path)
            winreg.SetValueEx(key, value_name, 0, value_type, value)
            winreg.CloseKey(key)
            return "Registry value set successfully"
        except WindowsError as e:
            return {'error': str(e)}
    
    def get_disk_info(self):
        """Get detailed information about disk drives."""
        drives = []
        for drive in self._wmi.Win32_LogicalDisk():
            drives.append({
                'device_id': drive.DeviceID,
                'volume_name': drive.VolumeName,
                'size': drive.Size,
                'free_space': drive.FreeSpace,
                'filesystem': drive.FileSystem,
                'drive_type': drive.DriveType
            })
        return drives
    
    def get_startup_items(self):
        """Get list of startup programs."""
        startup_locations = [
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            r"Software\Microsoft\Windows\CurrentVersion\RunOnce"
        ]
        
        startup_items = []
        for location in startup_locations:
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, location)
                i = 0
                while True:
                    try:
                        name, value, type = winreg.EnumValue(key, i)
                        startup_items.append({
                            'name': name,
                            'command': value,
                            'location': location
                        })
                        i += 1
                    except WindowsError:
                        break
            except WindowsError:
                continue
        return startup_items
