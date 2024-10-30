import os
import shutil
import platform
from pathlib import Path

class Files:
    def __init__(self, computer):
        self.computer = computer
        
    def normalize_path(self, path):
        return str(Path(path).resolve())
        
    def list(self, path="."):
        return os.listdir(self.normalize_path(path))

    def write(self, path, content):
        path = self.normalize_path(path)
        with open(path, 'w') as f:
            f.write(content)

    def read(self, path):
        path = self.normalize_path(path)
        with open(path, 'r') as f:
            return f.read()

    def append(self, path, content):
        path = self.normalize_path(path)
        with open(path, 'a') as f:
            f.write(content)

    def delete(self, path):
        path = self.normalize_path(path)
        os.remove(path)

    def copy(self, src, dst):
        src = self.normalize_path(src)
        dst = self.normalize_path(dst)
        shutil.copy(src, dst)

    def move(self, src, dst):
        src = self.normalize_path(src)
        dst = self.normalize_path(dst)
        shutil.move(src, dst)

    def mkdir(self, path):
        path = self.normalize_path(path)
        os.makedirs(path, exist_ok=True)

    def rmdir(self, path):
        path = self.normalize_path(path)
        shutil.rmtree(path)

    def exists(self, path):
        path = self.normalize_path(path)
        return os.path.exists(path)

    def is_file(self, path):
        path = self.normalize_path(path)
        return os.path.isfile(path)

    def is_dir(self, path):
        path = self.normalize_path(path)
        return os.path.isdir(path)

    def get_size(self, path):
        path = self.normalize_path(path)
        return os.path.getsize(path)

    def get_modified_time(self, path):
        path = self.normalize_path(path)
        return os.path.getmtime(path)
