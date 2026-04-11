### Compile for Production by Pyinstaller

Windows:
```bash
pyinstaller -w -F -n downloader --add-data "assets;assets" --add-data "static;static" main.py
```

macOS:
```bash
pyinstaller -w -F -n downloader --add-data "assets:assets" --add-data "static:static" main.py
```
