#! /usr/bin/env python3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Загружаем пользовательский интерфейс из файла .ui
        uic.loadUi("ui/main_window.ui", self)

        # Пример получения кнопки по имени из ui-файла и подключения сигнала
        #self.pushButton.clicked.connect(self.on_button_click)

    #def on_button_click(self):
    #    QMessageBox.information(self, "Сообщение", "Кнопка нажата!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
