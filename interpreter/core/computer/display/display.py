import platform

class Display:
    def __init__(self, computer):
        self.computer = computer
        self._screenshot = None
        self._system = platform.system()

    def view(self):
        """
        Capture a screenshot and return the computer vision results
        """
        screenshot = self.computer.capture_screenshot()
        self._screenshot = screenshot
        return self.computer.vision.query(screenshot)

    def get_window_info(self):
        """Get information about all visible windows"""
        if self._system == 'Windows':
            import win32gui
            def callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    windows.append({'handle': hwnd, 'title': win32gui.GetWindowText(hwnd)})
            windows = []
            win32gui.EnumWindows(callback, windows)
            return windows
        return None
