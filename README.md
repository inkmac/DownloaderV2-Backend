### Required Python Package for Project

```bash
pip install pyside6 fastapi browser_cookie3 yt-dlp uvicorn pyinstaller
```


### Required Assets for Project
- static/
  - index.html      # main frontend page
- assets/
  - ffmpeg/         # ffmpeg binary for media processing
    - ffmpeg.exe


### Compile for Production by Pyinstaller

Windows:
```bash
pyinstaller -w -F -n downloader --add-data "assets;assets" --add-data "static;static" main.py
```

macOS:
```bash
pyinstaller -w -F -n downloader --add-data "assets:assets" --add-data "static:static" main.py
```
