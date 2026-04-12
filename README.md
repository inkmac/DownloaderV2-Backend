### required python package for project

```bash
pip install pyside6 fastapi browser_cookie3 yt-dlp uvicorn pyinstaller
```


### Compile for Production by Pyinstaller

Windows:
```bash
pyinstaller -w -F -n downloader --add-data "assets;assets" --add-data "static;static" main.py
```

macOS:
```bash
pyinstaller -w -F -n downloader --add-data "assets:assets" --add-data "static:static" main.py
```
