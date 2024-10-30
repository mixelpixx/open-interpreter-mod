import os
import shutil
import platform

class Files:
    def __init__(self, computer):
        self.computer = computer
        self._system = platform.system()

    def list(self, path="."):
        """List files in directory"""
        return os.listdir(path)

    def write(self, path, content):
        """Write content to file"""
        with open(path, 'w') as f:
            f.write(content)

    def get_windows_drives(self):
        """
        List all available Windows drives
        """
        if self._system != 'Windows':
            return None
            
        import win32api
        drives = []
        for letter in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
            try:
                info = win32api.GetVolumeInformation(letter)
                drives.append({
                    'letter': letter,
                    'label': info[0],
                    'filesystem': info[4]
                })
            except:
                continue
        return drives
