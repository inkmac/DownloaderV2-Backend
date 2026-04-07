from yt_dlp import YoutubeDL


class SignalYoutubeDL(YoutubeDL):
    def __init__(self, *args, console_signal, **kwargs):
        super().__init__(*args, **kwargs)
        self.console_signal = console_signal

    def to_stdout(self, message, **kwargs):
        if self.console_signal:
            self.console_signal.emit(message)
        else:
            super().to_stdout(message, **kwargs)
