# Web Page to Desktop App Converter

A simple program that converts any website into a standalone **Windows
application (.exe)**.\
The GUI built with **PyQt5** allows you to paste a link and build the
app with a single click.

## 🚀 Features

-   Convert any URL (e.g., `https://youtube.com`) into an executable
    app.
-   Standalone window with an embedded browser (**QWebEngineView**).
-   Build as a single `.exe` file using **PyInstaller**.\
-   Automatic cleanup of temporary build files.

## 🛠 Requirements

Make sure you have installed: - Python **3.8+**
- [PyQt5](https://pypi.org/project/PyQt5/)
- [PyQtWebEngine](https://pypi.org/project/PyQtWebEngine/)
- [PyInstaller](https://pyinstaller.org/en/stable/)

Install dependencies with:

``` bash
pip install PyQt5 PyQtWebEngine pyinstaller
```

## 📦 Installation & Run

1.  Clone the repository or download `main.py`.
2.  Install dependencies.
3.  Run the program:

``` bash
python main.py
```

## ⚙ Usage

1.  Launch the program.
2.  Paste the website URL into the input field.
3.  Click **Create .exe**.
4.  Wait for the build to finish (usually under a minute).
5.  The generated `.exe` will be available inside the `dist/` folder.

## 📂 Example

-   Input: `https://youtube.com`
-   Output: `dist/youtube_com_app.exe`
-   Running the app opens a window that loads the website.

## ⚠ Troubleshooting

-   If PyInstaller throws an error, ensure the project path does not
    contain non-Latin characters.
-   First-time builds may take longer.
-   Currently supported only on Windows. For Linux/macOS, adjust the
    build process accordingly.

## 📝 License

MIT License. Free to use for personal and commercial projects.
