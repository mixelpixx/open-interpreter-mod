from .tools.tools import Tools
from .tools.windows_tools import WindowsTools

class Computer:
    def __init__(self):
        self.tools = Tools(self)
        self.windows = WindowsTools() if platform.system() == "Windows" else None
