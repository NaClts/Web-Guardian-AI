import helper__safe_write
import subprocess
import sys
import time
from pathlib import Path


class Stopwatch:

    def __init__(self):
        self.start_time = None
        self.elapsed_time = None
        self.safe_write_py_path = str(Path(helper__safe_write.__file__).resolve())

    def start(self):
        self.start_time = time.perf_counter()
    
    def stop(self):
        if self.start_time is not None:
            self.elapsed_time = time.perf_counter() - self.start_time
        else:
            raise Exception("Stopwatch has not been started yet")

    def write(self, path):
        if self.elapsed_time is not None:
            subprocess.Popen(
                [
                    sys.executable,
                    self.safe_write_py_path,
                    path,
                    f"Elapsed time: {self.elapsed_time:.6f} second(s)"
                ],
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                close_fds=True
            )
        else:
            raise Exception("Stopwatch has not been stopped yet")
