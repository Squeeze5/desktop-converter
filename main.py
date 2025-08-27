import os
import subprocess
import sys
import shutil
from threading import Thread

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QMessageBox
)


class WorkerSignals(QObject):
    status = pyqtSignal(str)
    success = pyqtSignal(str, str)  # title, message
    warning = pyqtSignal(str, str)
    critical = pyqtSignal(str, str)
    open_folder = pyqtSignal(str)
    enable_button = pyqtSignal()


class WebToDesktopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create EXE from URL")
        self.setFixedSize(400, 150)

        layout = QVBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste a URL (e.g., https://chat.openai.com)")
        layout.addWidget(self.url_input)

        self.create_button = QPushButton("Build .exe")
        self.create_button.clicked.connect(self.start_build_thread)
        layout.addWidget(self.create_button)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        # Signals
        self.signals = WorkerSignals()
        self.signals.status.connect(self.update_status)
        self.signals.success.connect(self.show_info)
        self.signals.warning.connect(self.show_warning)
        self.signals.critical.connect(self.show_critical)
        self.signals.open_folder.connect(self.open_folder)
        self.signals.enable_button.connect(lambda: self.create_button.setEnabled(True))

    def generate_script(self, url):
        return f"""
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView

app = QApplication(sys.argv)
web = QWebEngineView()
web.load(QUrl("{url}"))
web.setWindowTitle("Web App - {url}")
web.show()
sys.exit(app.exec_())
"""

    def start_build_thread(self):
        self.create_button.setEnabled(False)
        self.signals.status.emit("Building .exe... Please wait.")
        thread = Thread(target=self.create_app)
        thread.start()

    def create_app(self):
        url = self.url_input.text().strip()
        if not url:
            self.signals.warning.emit("Input Error", "Please enter a valid URL.")
            self.signals.enable_button.emit()
            return

        title = url.replace("https://", "").replace("http://", "").split("/")[0].replace('.', '_')
        dist_dir = os.path.abspath("dist")
        exe_name = f"{title}_app.exe"
        exe_path = os.path.join(dist_dir, exe_name)

        temp_script = f"{title}_temp_script.py"
        with open(temp_script, "w", encoding="utf-8") as f:
            f.write(self.generate_script(url))

        cmd = [
            "pyinstaller",
            "--onefile",
            "--noconsole",
            "--name", f"{title}_app",
            temp_script
        ]

        try:
            subprocess.run(cmd, check=True)
        except Exception as e:
            self.signals.status.emit(f"Build error: {e}")
            self.signals.critical.emit("Build Error", f"Failed to build EXE:\n{e}")
            self.signals.enable_button.emit()
            return

        # Cleanup
        if os.path.exists(temp_script):
            os.remove(temp_script)
        if os.path.exists("build"):
            shutil.rmtree("build")
        spec_file = f"{title}_app.spec"
        if os.path.exists(spec_file):
            os.remove(spec_file)

        if os.path.exists(exe_path):
            self.signals.status.emit(f"✔ EXE Created: {exe_path}")
            self.signals.success.emit("Success", f"EXE file has been successfully created:\n{exe_path}")
            self.signals.open_folder.emit(dist_dir)
        else:
            self.signals.status.emit("⚠ EXE creation failed.")
            self.signals.warning.emit("Error", "EXE file was not created.")

        self.signals.enable_button.emit()

    # GUI methods
    def update_status(self, text):
        self.status_label.setText(text)

    def show_info(self, title, message):
        QMessageBox.information(self, title, message)

    def show_warning(self, title, message):
        QMessageBox.warning(self, title, message)

    def show_critical(self, title, message):
        QMessageBox.critical(self, title, message)

    def open_folder(self, path):
        if os.name == "nt":  # Windows
            os.startfile(path)
        else:
            # Linux / Mac
            subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", path])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebToDesktopApp()
    window.show()
    sys.exit(app.exec_())
