class YtLogger:
    def __init__(self, signal):
        self.signal = signal

    def debug(self, msg):
        self.signal.emit(msg)

    def warning(self, msg):
        self.signal.emit(f'[Warning] {msg}')

    def error(self, msg):
        self.signal.emit(f'[Error] {msg}')
