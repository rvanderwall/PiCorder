

class Logger:
    def __init__(self, preamble):
        self.preamble = preamble

    def info(self, msg):
        print(f"{self.preamble}: INFO: {msg}")

    def error(self, msg):
        print(f"{self.preamble}: ERROR: {msg}")
