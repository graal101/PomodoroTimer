"""Модуль диалогов инфо-сообщений."""
from PyQt6.QtWidgets import QDialog, QFileDialog, QFontDialog, QMessageBox, QWidget


def message(self, title: str, board_text: str, ico=1):
        """Информационное окно."""
        msg = QMessageBox()
        if ico == 1:
            msg.setIcon(QMessageBox.Icon.Information)
        if ico == 2:
            msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(board_text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()


class FileDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.filter_dialog = 'All Files (*.*);;SQLite db Files (*.db);;SQLite Files (*.sqlite3)'

    def open_file_dialog(self):
        """Диалог открытия файла."""
        options = QFileDialog.Option.DontUseNativeDialog
        file_dialog = QFileDialog(self)
        file_dialog.setOptions(options)
        file_dialog.setNameFilter(self.filter_dialog)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)

        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            return file_path
        return None

    def save_file_dialog(self):
        """Диалог закрытия файла."""
        options = QFileDialog.Option.DontUseNativeDialog
        file_dialog = QFileDialog(self)
        file_dialog.setOptions(options)
        file_dialog.setNameFilter(self.filter_dialog)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)

        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            return file_path
        return None

    def font_dialog(self):
        """Диалог выбора шрифта."""
        font, ok = QFontDialog.getFont()
        if ok:
            return font
        return None
