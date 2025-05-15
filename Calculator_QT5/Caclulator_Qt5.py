# coding=utf-8
# **********************************************************
# ChatGPT - Simple Calculator (Python3 + QT5)
# ----------------------------------------------------------
# Python 3.13.3
# jetBrain PyCharm 2024.2.3
# ChatGPT - Design
# ----------------------------------------------------------
# pip install pyqt5
# python -m nuitka --windows-console-mode=disable
# **********************************************************
# ChatGPT, 2025
# Writing sgiman, 2025
#

#
# pyinstaller -w Caclulator_Qt5.py
#

import sys

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout,
                             QPushButton, QLineEdit)

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


#########################################################
# CALCULATOR (QT5)
#########################################################
class Calculator(QWidget):
    # -------------------------------------------------------
    # SETUP
    # -------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.input = None
        self.setWindowTitle("Simple Calculator (QT5)")
        self.setFixedSize(300, 400)
        self.setStyleSheet("background-color: #2e3440;")

        self.create_ui()

    # -------------------------------------------------------
    # CREATE UI
    # -------------------------------------------------------
    def create_ui(self):
        # Поле ввода
        self.input = QLineEdit()
        self.input.setFont(QFont("Arial", 24))
        self.input.setStyleSheet("color: #eceff4; background-color: #4c566a; border: none; padding: 10px;")
        self.input.setAlignment(Qt.AlignRight)
        self.input.setReadOnly(True)

        # Сетка кнопок
        buttons_layout = QGridLayout()
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('C', 3, 2), ('+', 3, 3),
            ('=', 4, 0, 1, 4)
        ]

        for btn in buttons:
            text = btn[0]
            row = btn[1]
            col = btn[2]
            rowspan = btn[3] if len(btn) > 3 else 1
            colspan = btn[4] if len(btn) > 4 else 1

            button = QPushButton(text)
            button.setFont(QFont("Arial", 18))

            # Специальный цвет для кнопки "="
            if text == "=":
                button.setStyleSheet(
                    "QPushButton { background-color: #bf616a; color: #eceff4; border: none; padding: 20px; }"
                    "QPushButton:hover { background-color: #d08770; }"
                )
            else:
                button.setStyleSheet(
                    "QPushButton { background-color: #434c5e; color: #eceff4; border: none; padding: 20px; }"
                    "QPushButton:hover { background-color: #5e81ac; }"
                )

            button.clicked.connect(self.on_button_clicked)
            buttons_layout.addWidget(button, row, col, rowspan, colspan)

        # Основной макет
        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    # ---------------------------------------------------
    # Нажатие кнопок
    # on_button_clicked()
    # ---------------------------------------------------
    def on_button_clicked(self):
        button = self.sender()
        text = button.text()

        # RESET & QUEL & ERROR (exept)
        if text == "C":
            self.input.clear()  # очистить
        elif text == "=":
            try:
                result = str(round(eval(self.input.text()), 4))  # вычислить и округлить
                self.input.setText(result)
            except Exception:
                self.input.setText("Ошибка")
        else:
            self.input.setText(self.input.text() + text)


########################################################
# MAIN (START)
########################################################
if __name__ == "__main__":
    # Start Application
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()

    # Console
    print('*' * 42)
    print('ChatGPT Simple Calculator (python3 + QT5)')
    print('*' * 42)

    # Exit
    # window.setWindowTitle('SIMPLE CALCULATOR')
    window.setWindowIcon(QIcon('python.ico'))
    sys.exit(app.exec_())
