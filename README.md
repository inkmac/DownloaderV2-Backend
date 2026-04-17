### Required Assets for Project
- static/
  - index.html      # main frontend page
- assets/
  - ffmpeg/         # ffmpeg binary for media processing
    - ffmpeg.exe


### Cython Compile

```bash
python setup.py build_ext --inplace
```


### Compile for Production by Pyinstaller

Windows:
```bash
pyinstaller -w -n downloader --add-data "assets;assets" --add-data "static;static" main.py
```

macOS:
```bash
pyinstaller -w -n downloader --add-data "assets:assets" --add-data "static:static" main.py
```
