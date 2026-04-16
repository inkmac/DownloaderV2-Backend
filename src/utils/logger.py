from src.utils.ydl_types import YdlLoggerProtocol


class YdlLogger(YdlLoggerProtocol):
    def __init__(self, buffer: list[str]):
        self.buffer = buffer

    def debug(self, msg):
        print(msg)
        self.buffer.append(f'{msg}\n')

    def warning(self, msg):
        print(msg)
        self.buffer.append(f'[Warning] {msg}\n')

    def error(self, msg):
        print(msg)
        self.buffer.append(f'[Error] {msg}\n')
