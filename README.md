# Web Page to Desktop App Converter

A simple program that converts any website into a standalone **Windows
application (.exe)**.  
The GUI, built with **PyQt5**, allows you to paste a link and build the
app with a single click. The latest version ensures a **responsive interface** even during builds, and automatically opens the output folder once the `.exe` is ready.

## 🚀 Features

- Convert any URL (e.g., `https://youtube.com`) into an executable app.
- Standalone window with an embedded browser (**QWebEngineView**).
- Build as a single `.exe` file using **PyInstaller**.
- Responsive interface during build (runs in a separate thread).
- Automatic cleanup of temporary build files.
- **Button disabled while building** to prevent multiple clicks.
- **Automatically opens the folder** containing the generated `.exe` after build.

## 🛠 Requirements

Make sure you have installed:  
- Python **3.8+**
- [PyQt5](https://pypi.org/project/PyQt5/)
- [PyQtWebEngine](https://pypi.org/project/PyQtWebEngine/)
- [PyInstaller](https://pyinstaller.org/en/stable/)

Install dependencies with:

```bash
pip install PyQt5 PyQtWebEngine pyinstaller

```

## ⚙ Usage

1.  Launch the program.
2.  Paste the website URL into the input field.
3.  Click **Create .exe**.
4.  Wait for the build to finish (usually under a minute).
5.  The generated `.exe` will be available inside the `dist/` folder.
6. The output folder will automatically open when the build completes.

## 📂 Example

-   Input: `https://youtube.com`
-   Output: `dist/youtube_com_app.exe`
-   Running the app opens a standalone window that loads the website.

## ⚠ Troubleshooting

-   If PyInstaller throws an error, ensure the project path does not
    contain non-Latin characters.
-   First-time builds may take longer.
-   Supported only on Windows. Linux/macOS support may require adjusting the build process.

## 📝 License

MIT License. Free to use for personal and commercial projects.
