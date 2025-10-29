#! /usr/bin/env python3
import sys
import time
from PyQt6.QtCore import QTimer
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Загружаем пользовательский интерфейс из файла .ui
        uic.loadUi("ui/main_window.ui", self)
        self.btn_start.clicked.connect(self.on_btn_start_click)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = 0
        
    def start_countdown(self, t: int):
        self.remaining_time = t
        self.timer.start(1000)  # запускает таймер с интервалом 1 секунда
        
    def update_timer(self):
        if self.remaining_time > 0:
            mins, secs = divmod(self.remaining_time, 60)
            timer_display = '{:02d}:{:02d}'.format(mins, secs)
            self.label_time.setText(timer_display)
            self.remaining_time -= 1
        else:
            self.timer.stop()  # останавливает таймер, когда время истекает
        

    def on_btn_start_click(self):
        self.start_countdown(10)
        
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
