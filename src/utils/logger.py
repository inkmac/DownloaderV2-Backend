from src.utils.ydl_types import YdlLoggerProtocol


class YdlLogger(YdlLoggerProtocol):
    def __init__(self, buffer: list[str]):
        self.buffer = buffer

    def debug(self, msg):
        self.buffer.append(msg)

    def warning(self, msg):
        self.buffer.append(f'[Warning] {msg}')

    def error(self, msg):
        self.buffer.append(f'[Error] {msg}')
