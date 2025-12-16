#! /usr/bin/env python3
import sys
import time
from libs.sound import Sound
from Dialogs.dialogs import FileDialog
from PyQt6.QtCore import QTimer
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

# FIX documentation! Linter it!
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Загружаем пользовательский интерфейс из файла .ui
        uic.loadUi("ui/main_window.ui", self)
        self.btn_start.clicked.connect(self.on_btn_start_click)
        self.mn_quit.triggered.connect(self.app_quit)
        self.mn_font.triggered.connect(self.app_font)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = 0
        
    def start_countdown(self, t: int):
        self.remaining_time = t
        self.Bar_work.setMaximum(t)
        self.Bar_work.setValue(0)
        self.timer.start(1000)  # запускает таймер с интервалом 1 секунда
        
    def update_timer(self):
        if self.remaining_time > 0:
            mins, secs = divmod(self.remaining_time, 60)
            timer_display = '{:02d}:{:02d}'.format(mins, secs)
            self.label_time.setText(timer_display)
            self.Bar_work.setValue(self.Bar_work.maximum() - self.remaining_time)
            self.remaining_time -= 1
        else:
            self.timer.stop()  # останавливает таймер, когда время истекает
        

    def on_btn_start_click(self):
        snd = Sound(1200, 2500)
        snd.play_sound()
        w = self.spin_work.value() * 60  # Время задания
        r = self.spin_rest.value() * 60  # Время перерыва
        self.work_rest_fun(w, r)
        self.start_countdown(w)
        
    def app_font(self):
        font_open = FileDialog()
        fsize = font_open.font_dialog()
        if fsize:
            print(fsize)
            self.label_info.setFont(fsize)
            self.label_time.setFont(fsize)

    def work_rest_fun(self, work: int, rest:int, number_bar: int = 0 ):
        pass
        
    def app_quit(self):
        quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
