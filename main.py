import os
import platform
import subprocess
import sys
import shutil

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QMessageBox
)


class WebToDesktopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Создание EXE из ссылки")
        self.setFixedSize(400, 150)

        layout = QVBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Вставьте ссылку (например, https://chat.openai.com)")
        layout.addWidget(self.url_input)

        self.create_button = QPushButton("Создать .exe")
        self.create_button.clicked.connect(self.create_app)
        layout.addWidget(self.create_button)

        self.status = QLabel("")
        layout.addWidget(self.status)

        self.setLayout(layout)

    def generate_script(self, url):
        # Генерация кода Python, который будет открывать нужный URL
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

    def create_app(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Ошибка", "Введите URL.")
            return

        title = url.replace("https://", "").replace("http://", "").split("/")[0].replace('.', '_')
        dist_dir = os.path.abspath("dist")

        # Название exe-файла
        exe_name = f"{title}_app.exe"
        exe_path = os.path.join(dist_dir, exe_name)

        # Временный .py-файл, из которого будет собираться .exe
        temp_script = f"{title}_temp_script.py"
        with open(temp_script, "w", encoding="utf-8") as f:
            f.write(self.generate_script(url))

        self.status.setText("Сборка .exe, пожалуйста подождите...")

        # Команда сборки через PyInstaller
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
            self.status.setText(f"Ошибка сборки: {e}")
            return

        # Очистка временных файлов
        if os.path.exists(temp_script):
            os.remove(temp_script)
        if os.path.exists("build"):
            shutil.rmtree("build")
        spec_file = f"{title}_app.spec"
        if os.path.exists(spec_file):
            os.remove(spec_file)

        if os.path.exists(exe_path):
            self.status.setText(f"✔ Создано: {exe_path}")
            QMessageBox.information(self, "Успех", f"EXE-файл создан:\n{exe_path}")
        else:
            self.status.setText("⚠ Не удалось создать EXE.")
            QMessageBox.warning(self, "Ошибка", "EXE-файл не был создан.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebToDesktopApp()
    window.show()
    sys.exit(app.exec_())
