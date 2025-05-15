###########################################################
# WebConvertor.py
# CONVERTER WEBP to JPEG/PNG
# QT5 GUI
#-----------------------------------------------------------
# Created ChetGPT:
# Создать на python и QT5 конвертер для папки
# с изображениями webp в формат jpeg.
###########################################################
# Writing sgiman (May 2025)

"""
 - Выбирается папка с .webp изображениями.
 - Выбирается папка для сохранения .jpeg файлов.
 - Все .webp файлы рекурсивно конвертируются и сохраняются как .jpeg, структура папок сохраняется.
 - Есть прогресс-бар и уведомление о завершении

 - Настройка качества JPEG — слайдер от 1 до 100.
 - Удаление исходных файлов .webp — через чекбокс.
 - Лог ошибок в файл error_log.txt.
 - Поддержка drag-and-drop для исходной папки.

 ✅ Drag-and-drop Поддержка для папок и отдельных файлов
 ✅ JPEG/PNG	Поддержка форматов вывода
 ✅ Качество	Устанавливается для JPEG
 ✅ Логи	error_log.txt и success_log.txt
 ✅ Удаление .webp	По выбору пользователя
 ✅ Конвертация файлов	Можно выбрать как папку, так и конкретные файлы
"""

#
# pyinstaller -w WebConvertor.py
#

import os
from PIL import Image

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog,
    QLabel, QMessageBox, QProgressBar, QCheckBox, QSlider, QComboBox
)

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.uic.Compiler.qtproxies import QtGui

from PyQt5 import QtWidgets, QtGui
#from PyQt5.QtWidgets import *
#from PyQt5.QtCore import *

#////////////////////////////////////////////////////////////////
# ConverterThread (CLASS)
# Поток конвертирования
#////////////////////////////////////////////////////////////////
class ConverterThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    #-----------------------------------------------------------
    # CONSTRUCTOR
    #-----------------------------------------------------------
    def __init__(self, file_list, dst_folder, quality=85, delete_original=False, out_format="JPEG"):
        super().__init__()
        self.file_list = file_list                  # список имен файлов
        self.dst_folder = dst_folder                # попка с результатом
        self.quality = quality                      # качество
        self.delete_original = delete_original      # флаг дл удаления оригинала
        self.out_format = out_format.upper()        # выходной формат

    #-----------------------------------------------------------
    # run()
    # ЗПУСК ПРОЦЕССА КОНВЕРТИРОВАНИЯ
    #-----------------------------------------------------------
    def run(self):
        os.makedirs(self.dst_folder, exist_ok=True)                     # создать папку с результатом, если не существует
        error_log = open("error_log.txt", "w", encoding="utf-8")        # лог ошибок
        success_log = open("success_log.txt", "w", encoding="utf-8")    # лог с успешным завершением

        total = len(self.file_list)     # общее кол-во файлов

        # *** ЦИКЛ КОНВЕРТАЦИИ WEBP->JPG/PNG ***
        for i, filepath in enumerate(self.file_list, 1):
            try:
                # Сформировать пути к файлам
                rel_path = os.path.basename(filepath) if len(self.file_list) == 1 else os.path.relpath(filepath, os.path.commonpath(self.file_list))
                dst_path = os.path.join(self.dst_folder, os.path.splitext(rel_path)[0] + (".png" if self.out_format == "PNG" else ".jpg"))
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)

                # Файловые операции и конвертация (jpg/png)
                with Image.open(filepath) as im:
                    rgb_im = im.convert('RGB')     # *** CONVERT!!! ***
                    # Если выбран JPEG - сохранить в .jpg, иначе в .png
                    if self.out_format == "JPEG":
                        rgb_im.save(dst_path, self.out_format, quality=self.quality)
                    else:
                        rgb_im.save(dst_path, self.out_format)
                success_log.write(f"Успешно: {filepath} → {dst_path}\n")

                # Если разрешено удаление - удалить оригиналы
                if self.delete_original:
                    os.remove(filepath)

            # Исключение в случае ошибки
            except Exception as e:
                error_log.write(f"Ошибка при обработке {filepath}:\n{e}\n\n")

            # Значения для progress-bar
            self.progress.emit(int(i / total * 100))

        # Закрыть все логи и завершить поток конвертации
        error_log.close()
        success_log.close()
        self.finished.emit()


#////////////////////////////////////////////////////////////////
# WebpConverter()
# Главный класс (QT5 GUI)
#////////////////////////////////////////////////////////////////
class WebpConverter(QWidget):

    #************************************************************
    # CONSTRUCTOR
    #************************************************************
    def __init__(self):
        super().__init__()

        # INIT GUI
        self.setWindowTitle("Конвертер изображений WebP → JPEG/PNG")    # title
        self.setWindowIcon(QtGui.QIcon('plus.ico'))                     # icon
        self.setFixedSize(450, 360)                                     # size
        self.setAcceptDrops(True)                                       # Drag & Drop

        self.layout = QVBoxLayout()                                     # layout

        #====================================================================================
        # ELEMENTS UI
        #====================================================================================

        #------------------------------------------------------------------------------------
        # Info Label
        #------------------------------------------------------------------------------------
        self.info_label = QLabel("Перетащите файлы или папки, или выберите вручную.")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.info_label)

        #------------------------------------------------------------------------------------
        # File Button
        #------------------------------------------------------------------------------------
        self.file_button = QPushButton("Выбрать отдельные файлы")
        self.file_button.setStyleSheet('color:white; font-size: 14px; background:#1565C0')
        self.file_button.clicked.connect(self.select_files)
        self.layout.addWidget(self.file_button)

        #------------------------------------------------------------------------------------
        # Folder Button
        #------------------------------------------------------------------------------------
        self.folder_button = QPushButton("Выбрать папку с изображениями")
        self.folder_button.setStyleSheet('color:black; font-size: 14px; background:#e8e8e8')
        self.folder_button.clicked.connect(self.select_folder)
        self.layout.addWidget(self.folder_button)

        #------------------------------------------------------------------------------------
        # Label - FOLDER DIST
        #------------------------------------------------------------------------------------
        self.dst_label = QLabel("Папка назначения:")
        self.layout.addWidget(self.dst_label)

        #------------------------------------------------------------------------------------
        # Button - FOLDER DIST
        #------------------------------------------------------------------------------------
        self.dst_button = QPushButton("Выбрать папку назначения")
        self.dst_button.setStyleSheet('color:black; font-size: 14px; background:#e8e8e8')
        self.dst_button.clicked.connect(self.select_dest_folder)
        self.layout.addWidget(self.dst_button)

        #------------------------------------------------------------------------------------
        # Combobox - format (jpg,png)
        #------------------------------------------------------------------------------------
        self.format_combo = QComboBox()
        self.format_combo.addItems(["JPEG", "PNG"])
        self.layout.addWidget(QLabel("Формат вывода:"))
        self.layout.addWidget(self.format_combo)

        #------------------------------------------------------------------------------------
        # Label - Quality (jpeg)
        #------------------------------------------------------------------------------------
        self.quality_label = QLabel("Качество JPEG: 85")
        self.layout.addWidget(self.quality_label)

        #------------------------------------------------------------------------------------
        # Slider  - Quality (85 - default)
        #------------------------------------------------------------------------------------
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(1, 100)
        self.quality_slider.setValue(85)
        self.quality_slider.valueChanged.connect(self.update_quality_label)
        self.layout.addWidget(self.quality_slider)

        #------------------------------------------------------------------------------------
        # Check Box - "DELETE *.webp"
        #------------------------------------------------------------------------------------
        self.delete_checkbox = QCheckBox("Удалять исходные .webp файлы")
        self.layout.addWidget(self.delete_checkbox)

        #------------------------------------------------------------------------------------
        # Button - "CONVERTING"
        #------------------------------------------------------------------------------------
        self.convert_button = QPushButton("Конвертировать")
        self.convert_button.setStyleSheet('color:white; font-size: 14px; background:#ab1d13')
        # Connect to events
        self.convert_button.clicked.connect(self.convert_images)
        self.convert_button.setEnabled(False)
        self.layout.addWidget(self.convert_button)

        #------------------------------------------------------------------------------------
        # Progress Bar
        #------------------------------------------------------------------------------------
        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)     # layout

        self.src_files = []             # src buffer
        self.dst_folder = ''            # dist folder


    #=============================================================
    # Обработчики событий (слоты)
    #=============================================================

    #-------------------------------------------------------------
    # update_quality_label()
    # Обновить значение метки для качества
    #-------------------------------------------------------------
    def update_quality_label(self, value):
        self.quality_label.setText(f"Качество JPEG: {value}")

    #-------------------------------------------------------------
    # select_files()
    # Выбрать файлы *.webp
    #-------------------------------------------------------------
    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Выберите изображения WebP", "", "WebP файлы (*.webp)")
        print(files)    # test
        if files:
            self.src_files = files
            self.info_label.setText(f"Выбрано файлов: {len(files)}")
            self.check_ready()

    #-------------------------------------------------------------
    # select_folder()
    # Выбрать папку с изображениями *.webp
    #-------------------------------------------------------------
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder:
            self.src_files = []
            for root, _, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith(".webp"):
                        self.src_files.append(os.path.join(root, file))
            self.info_label.setText(f"Найдено изображений: {len(self.src_files)}")
            self.check_ready()

    #-------------------------------------------------------------
    # select_dest_folder()
    # Выбрать папку назначения для *.jpg, *.png
    #-------------------------------------------------------------
    def select_dest_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку назначения")
        if folder:
            self.dst_folder = folder
            self.dst_label.setText(f"Папка назначения: {folder}")
            self.check_ready()

    #-------------------------------------------------------------
    # check_ready()
    # Поверка готовности выбранных файлов и папок
    #-------------------------------------------------------------
    def check_ready(self):
        if self.src_files and self.dst_folder:
            self.convert_button.setEnabled(True)

    #-------------------------------------------------------------
    # convert_images()
    # Конвертировать выбранные изображения
    #-------------------------------------------------------------
    def convert_images(self):
        self.convert_button.setEnabled(False)               # запретить кнопку "КОНВЕРТИРОВАТЬ"
        quality = self.quality_slider.value()               # установить качество
        delete_original = self.delete_checkbox.isChecked()  # сбросить checkbox для удаления оригиналов
        out_format = self.format_combo.currentText()        # установить выходной формат

        # КОНВЕРТИРОВАНИЕ (поток)
        self.thread = ConverterThread(
            self.src_files,
            self.dst_folder,
            quality=quality,
            delete_original=delete_original,
            out_format=out_format
        )
        self.thread.progress.connect(self.progress_bar.setValue)    # подключение progress-bar
        self.thread.finished.connect(self.on_finished)              # подключение для финализации
        self.thread.start()                                         # запустить поток конвертирования

    #-------------------------------------------------------------
    # on_finished()
    # ФИНАЛИАЗАЦИЯ
    #-------------------------------------------------------------
    def on_finished(self):
        QMessageBox.information(self, "Готово", "Конвертация завершена!")
        self.progress_bar.setValue(0)           # сбросить progress-bar
        self.convert_button.setEnabled(True)    # разрешить кнопку конвертирования

    #-------------------------------------------------------------
    # dragEnterEvent()
    # Отслеживание событий "DRAG & DROP"
    #-------------------------------------------------------------
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    #-------------------------------------------------------------
    # dropEvent()
    # Обработчик события "DROP"
    #-------------------------------------------------------------
    def dropEvent(self, event):
        paths = [url.toLocalFile() for url in event.mimeData().urls()] # найденные пути к файлам

        all_files = []  # массив имен файлов

        # Заполнить массив файлов с изображениями *.webp
        for path in paths:
            if os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        if file.lower().endswith('.webp'):
                            all_files.append(os.path.join(root, file))
            elif path.lower().endswith('.webp'):
                all_files.append(path)

        if all_files:
            self.src_files = all_files
            self.info_label.setText(f"Найдено изображений: {len(all_files)}")
            self.check_ready()


#*****************************
# START
#*****************************
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)    # create application
    window = WebpConverter()        # create window for converter
    window.show()                   # show
    sys.exit(app.exec_())           # exec & exit for error

