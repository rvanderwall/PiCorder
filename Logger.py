from datetime import datetime

class Logger:
    def __init__(self, preamble):
        self.preamble = preamble

    def info(self, msg):
        self._log(f"{self.preamble}: INFO: {msg}")

    def error(self, msg):
        self._log(f"{self.preamble}: ERROR: {msg}")

    def _log(self, msg):
        t = datetime.now()
        print(f"{t}: {msg}")
