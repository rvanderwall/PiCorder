from datetime import datetime


class Logger:
    def __init__(self, preamble):
        self.preamble = preamble

    def info(self, msg):
        self._log(f"INFO: {msg}")

    def error(self, msg):
        self._log(f"ERROR: {msg}")

    def _log(self, msg):
        t = datetime.now()
        print(f"{t}:{self.preamble}: {msg}")
