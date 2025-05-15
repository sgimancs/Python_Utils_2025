# coding=utf-8
# **********************************************************
# ChatGAPT - Simple Calculator (Python3 + QT5)
# ----------------------------------------------------------
# Python 3.13.3
# jetBrain PyCharm 2024.2.3
# ChatGPT - Design
# ----------------------------------------------------------
# pip install pyqt5
# python -m nuitka --windows-console-mode=disable
# **********************************************************
# ru.stackoverflow.com, 2025
# Writing sgiman, 2025
#
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon

# *********************************************************
# Ui_Dialog (class)
# *********************************************************
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(452, 360)
        Dialog.setStyleSheet("background-color:#fbf5eb;\n"
                             "")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(10, 70, 381, 31))
        self.lineEdit.setStyleSheet("color:#1db823;\n"
                                    "font: 10pt \"Tw Cen MT Condensed Extra Bold\";\n"
                                    "background-color:#0a2c40;\n"
                                    "border:none;")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 130, 111, 31))
        self.pushButton.setStyleSheet("\n"
                                      "QPushButton {\n"
                                      "\n"
                                      "    color:white;\n"
                                      "    font: 8pt \"MS Serif\";\n"
                                      "    font: 11pt \"MS Shell Dlg 2\";\n"
                                      "    background-color:#620101;\n"
                                      "    border:none;\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:hover {\n"
                                      "    background-color:silver;\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:pressed {\n"
                                      "    background-color:red;\n"
                                      "}\n"
                                      "\n"
                                      "\n"
                                      "")
        self.pushButton.setObjectName("pushButton")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 240, 381, 31))
        self.lineEdit_2.setStyleSheet("color:#1db823;\n"
                                      "font: 10pt \"Tw Cen MT Condensed Extra Bold\";\n"
                                      "background-color:#0a2c40;\n"
                                      "border:none;")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 300, 111, 31))
        self.pushButton_2.setStyleSheet("\n"
                                        "QPushButton {\n"
                                        "\n"
                                        "    color: white;\n"
                                        "    font: 8pt \"MS Serif\";\n"
                                        "    font: 11pt \"MS Shell Dlg 2\";\n"
                                        "    background-color:#620101;\n"
                                        "    border:none;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover {\n"
                                        "    background-color:silver;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:pressed {\n"
                                        "    background-color:red;\n"
                                        "}\n"
                                        "\n"
                                        "")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 401, 31))
        self.label.setStyleSheet("font: 9pt \"MV Boli\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 190, 411, 31))
        self.label_2.setStyleSheet("font: 9pt \"MV Boli\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(156, 282, 291, 61))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(156, 112, 291, 61))
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    # ---------------------------------------------------------------
    #  retranslateUi()
    # ---------------------------------------------------------------
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("Dialog", "Преобразовать", None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate("Dialog", "Преобразовать", None, -1))
        self.label.setText(
            QtWidgets.QApplication.translate("Dialog", "    Перевести из десятичной системы исчисления в двоичную:",
                                             None, -1))
        self.label_2.setText(
            QtWidgets.QApplication.translate("Dialog", "    Перевести из двоичной системы исчисления в десятичную:",
                                             None, -1))


# *********************************************************
#  Bincalc (class)
# *********************************************************
class Bincalc(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Bincalc, self).__init__(parent)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.binarik)
        self.pushButton_2.clicked.connect(self.binarik_2)

    # ---------------------------------------------------------------
    #  binarik()
    # ---------------------------------------------------------------
    def binarik(self):
        num = int(self.lineEdit.text())
        newNum = ''
        while num > 0:
            newNum = str(num % 2) + newNum
            num //= 2
        self.label_4.setText(newNum)

    # ---------------------------------------------------------------
    #  binarik_2()
    # ---------------------------------------------------------------
    def binarik_2(self):
        a = self.lineEdit_2.text()

        def underdef(digit):
            length = len(digit)
            helpdig = 0
            for i in range(0, int(length)):
                helpdig = helpdig + int(digit[i]) * (2 ** (int(length) - i - 1))
            return helpdig

        self.label_3.setText(str(underdef(a)))

#####################################
# START
#####################################
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Bincalc()
    w.show()
    w.setWindowTitle('Бинарный калькулятор')
    w.setWindowIcon(QIcon('PLUS-ICON.ico'))
    sys.exit(app.exec_())
