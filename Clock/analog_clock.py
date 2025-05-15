#############################################################################
# clock_chatGPT.py
#
# Создать на python привлекательные по дизайну часы (графика)
# с круглым циферблатом и с тремя стрелками.
#
# Д о п о л н и т е л ь н о:
# добавить цифровую индикацию.
#-------------------------------------------------------------
# Пример графических аналоговых часов на Python
# с использованием библиотеки Tkinter и модуля math
# для расчета положения стрелок. Часы имеют круглый циферблат,
# три стрелки (часовая, минутная и секундная) и достаточно приятный дизайн.
#----------------------------------------------------------------------------
# В о з м о ж н о с т и:
#   Круглый циферблат.
#   Часовые деления.
#   Стрелки разного цвета и длины.
#   Авто-обновление каждую секунду.
#
# Д о б а в л е н о:
#   В нижней части окна (под циферблатом) отображается цифровое время в формате ЧЧ:ММ:СС.
#   Цифровое время обновляется синхронно со стрелками.
############################################################################

#
# сборка приложения в виде одного файла (без консоли)
# pyinstaller -w analog_clock.py
# python -m nuitka --windows-console-mode=disable
#

import tkinter as tk
import time
import math

########################################
# AnalogClock() - CLASS
########################################
class AnalogClock:
    #-----------------------------------
    # К О Н С Т Р У К Т О Р
    #-----------------------------------
    def __init__(self, win_main):
        self.root = win_main
        self.root.title("sgiman")
        self.root.resizable(False, False)

        self.canvas_size = 250                  # размер
        self.center = self.canvas_size // 2     # расстояние до центра
        self.clock_radius = self.center - 20    # радиус

        # Создать холст
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size + 40, bg='white')
        self.canvas.pack()

        # Аналоговые часы
        self.draw_clock_face() # Отрисовать циферблат

        # Цифровые часы
        self.digital_time_id = self.canvas.create_text(
            self.center, self.canvas_size + 20,  # Положение цифрового времени
            text='', font=('Helvetica', 32      , 'bold'), fill='black'
        )

        # Обновить время
        self.update_clock()

    #-----------------------------------
    # Ц И Ф Е Р Б Л А Т
    #-----------------------------------
    def draw_clock_face(self):
        self.canvas.create_oval(
            self.center - self.clock_radius, self.center - self.clock_radius,
            self.center + self.clock_radius, self.center + self.clock_radius,
            outline='black', width=4, fill='#f0f0f0'
        )

        # Часовые метки
        for hour in range(12):
            angle = math.radians((hour / 12) * 360)
            x_inner = self.center + (self.clock_radius - 30) * math.sin(angle)
            y_inner = self.center - (self.clock_radius - 30) * math.cos(angle)
            x_outer = self.center + self.clock_radius * math.sin(angle)
            y_outer = self.center - self.clock_radius * math.cos(angle)
            self.canvas.create_line(x_inner, y_inner, x_outer, y_outer, width=3)

        # Центр
        self.canvas.create_oval(
            self.center - 5, self.center - 5,
            self.center + 5, self.center + 5,
            fill='black'
        )

    #-----------------------------------
    # UPDATE CLOCK
    #-----------------------------------
    def update_clock(self):
        self.canvas.delete('hands')

        now = time.localtime()
        hours = now.tm_hour
        minutes = now.tm_min
        seconds = now.tm_sec

        # Углы стрелок
        hour_angle = math.radians(((hours % 12) + minutes / 60) * 30)
        minute_angle = math.radians((minutes + seconds / 60) * 6)
        second_angle = math.radians(seconds * 6)

        # Длина стрелок
        hour_len = self.clock_radius * 0.5
        minute_len = self.clock_radius * 0.7
        second_len = self.clock_radius * 0.85

        # Рисуем стрелки
        self.draw_hand(hour_angle, hour_len, 6, 'black')
        self.draw_hand(minute_angle, minute_len, 4, 'blue')
        self.draw_hand(second_angle, second_len, 2, 'red')

        # Обновляем цифровую индикацию
        digital_time = time.strftime("%H:%M:%S")
        self.canvas.itemconfigure(self.digital_time_id, text=digital_time)

        # self.root.after(1000, self.update_clock)    # "AFTER" - обновление через каждую секунду (запаздывает!!!)
        self.root.after(200, self.update_clock)       # синхронно с системным временем

    #-----------------------------------
    # DRAW HAND (отрисовка)
    #-----------------------------------
    def draw_hand(self, angle, length, width, color):
        x = self.center + length * math.sin(angle)
        y = self.center - length * math.cos(angle)
        self.canvas.create_line(self.center, self.center, x, y, width=width, fill=color, tags='hands')


#=======================================
# S T A R T
#=======================================
if __name__ == '__main__':
    root = tk.Tk()
    clock = AnalogClock(root)
    root.mainloop()
