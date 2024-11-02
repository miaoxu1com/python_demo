rem 不能使用--one-file否则必报错
D:/pyview_demo/.venv/Scripts/python.exe -m nuitka --debug --assume-yes-for-downloads --output-filename=pywebview_demo --windows-disable-console --windows-icon-from-ico=D:/descrpypython/main.ico --remove-output --no-pyi-file --assume-yes-for-downloads --output-dir=D:/pyview_demo/nuitka_output --plugin-enable=pywebview D:/pyview_demo/pywebview_demo.py
pause
