#! /usr/bin/env python3
import sys
from libs.sound import Sound
from Dialogs.dialogs import FileDialog
from PyQt6.QtCore import QTimer
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon
from PyQt6.QtGui import QIcon

TIMER_INTERVAL = 1000  # Интервал таймера в миллисекундах.
SOUND_START_FREQUENCY = 1200  # Частота звука при старте (гц).
SOUND_STOP_FREQUENCY = 1200  # Частота звука при остановке (гц).
SOUND_START_DURATION = 2500  # Продолжительность звука при старте в миллисекундах.
SOUND_STOP_DURATION = 1000  # Продолжительность звука при остановке  в миллисекундах.


class PauseState():
    """Класс для фиксации времен при паузе."""
    def __init__(self):
        self.t_work = 0  # Время осчёта для работы
        self.t_rest = 0  # Время отсчёта для отдыха

    def start_state(self): # Устанавливает начально/стартовые условия
        self.t_work = 0
        self.t_rest = 0
      

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Загружаем пользовательский интерфейс из файла .ui
        uic.loadUi('ui/main_window.ui', self)
        self.btn_start.clicked.connect(self.on_btn_start_click)
        self.btn_stop.clicked.connect(self.on_btn_stop)
        self.btn_pause.clicked.connect(self.on_btn_pause)
        self.mn_quit.triggered.connect(self.app_quit)
        self.mn_font.triggered.connect(self.app_font)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("ico/rotten-tomatoes-logo.png"))
        self.tray_icon.activated.connect(self.on_tray_icon_click)
        
        self.is_working = True  # Флаг, указывающий, идет ли сейчас работа или отдых
        self.work_duration = 0
        self.rest_duration = 0
        self.remaining_time = 0  # Добавлено для отслеживания оставшегося времени
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = 0
        
        self.tray_icon.show()

    def start_countdown(self, t: int):
        """Функция запуска таймера."""
        self.remaining_time = t
        self.Bar_work.setMaximum(t)
        self.Bar_work.setValue(0)

        if self.is_working:
            self.label_time.setText('Работа!')
        else:
            self.label_time.setText('Отдых!')
        
        self.timer.start(TIMER_INTERVAL)  # запускает таймер с интервалом 1 секунда

    def update_timer(self):
        """Обновление таймера."""
        if self.remaining_time > 0:
            mins, secs = divmod(self.remaining_time, 60)
            timer_display = '{:02d}:{:02d}'.format(mins, secs)
            self.label_time.setText(f'Работа - {timer_display}' if self.is_working else f'Отдых - {timer_display}')
            self.Bar_work.setValue(self.Bar_work.maximum() - self.remaining_time)
            self.remaining_time -= 1
        else:
            self.timer.stop()
            self.sound_mod('stop')  # Проигрываем звук при переключении режимов
            if self.is_working:
                self.is_working = False  # Переключаемся на отдых
                self.start_countdown(self.rest_duration)  # Запускаем отдых
                self.sound_mod('start')  # Проигрываем сигнал начала отдыха
            else:
                self.is_working = True  # Переключаемся на работу
                self.start_countdown(self.work_duration)  # Запускаем работу
                self.sound_mod('start')  # Проигрываем сигнал начала работы

    def on_btn_start_click(self):
        """Обработка нажатия кнопки 'Старт'."""
        self.sound_mod('start')

        # Считываем время работы и отдыха только в первый раз.
        if self.work_duration == 0 and self.rest_duration == 0:
            self.work_duration = self.spin_work.value() * 60
            self.rest_duration = self.spin_rest.value() * 60
            self.spin_work.setEnabled(False)
            self.spin_rest.setEnabled(False)

        if not self.timer.isActive():
            self.start_countdown(self.remaining_time if self.remaining_time > 0 else self.work_duration)
            self.btn_start.setEnabled(False)
        
    def on_btn_stop(self):
        """Обработчик нажатия кнопки 'Стоп'."""
        self.timer.stop()
        p.start_state()  # Сброс состояния
        self.Bar_work.setValue(0)
        self.label_time.setText('Null')
        self.btn_start.setEnabled(True)
        self.is_working = True  # Сброс состояния
        self.remaining_time = 0 # Сброс состояния
        

    def on_btn_pause(self):
        """Обработчик нажатия кнопки 'Пауза'."""
        if self.timer.isActive():
            self.timer.stop()  # Останавливаем таймер, если он запущен
            self.btn_start.setEnabled(True)  # Включаем кнопку 'Старт'
            self.label_time.setText('Пауза')  # Указываем, что таймер на паузе


    def on_tray_icon_click(self, reason):
        """Появление/скрытие окна при кликание по трею."""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isHidden():
                self.show()
                self.activateWindow()
            else:
                self.hide()
           
#========================================================================

    def app_font(self):
        """Выбор шрифтов в приложении."""
        font_open = FileDialog()
        fsize = font_open.font_dialog()
        if fsize:
            print(fsize)
            self.label_time.setFont(fsize)

    def sound_mod(self, mode):
        if mode == 'stop':
            for _ in range(3):
                snd = Sound(SOUND_STOP_FREQUENCY, SOUND_STOP_DURATION)
                snd.play_sound()
        if mode == 'start':
            snd = Sound(SOUND_START_FREQUENCY, SOUND_START_DURATION)
            snd.play_sound()
        
    def app_quit(self):
        quit()


if __name__ == '__main__':
    p = PauseState()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
