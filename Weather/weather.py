# coding=utf-8
#######################################################
# 024_Программа Погода в мире (lesson23)
# python 3.x
# WebForMySelf - Андрей Кудлай, 2019
#######################################################
# Writing sgiman, 2025

#
# сборка приложения в виде одного файла (без консоли)
# pyinstaller -w weather.py
# python -m nuitka --windows-console-mode=disable
#


#
# Requests — простая, но элегантная HTTP-библиотека.
#------------------------------------------------------
# Weather service:
# https://openweathermap.org/api
# https://openweathermap.org/api/one-call-3
#
# SAMPLE:
# https://api.openweathermap.org/data/2.5/weather?appid=key&q=kiev,ua
# https://api.openweathermap.org/data/2.5/weather?appid=5e1ce895b1f7950c8267adecc8ce4989&q=kiev,ua
#
# API KEY:
# e17444a645a7bc7f9fc670fbd48d6a00
#
#------------------------------------------------------
# {
# "coord":{"lon":30.5167,"lat":50.4333},
# "weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}],
#
# "base":"stations",
#
# "main":{"temp":285.22,"feels_like":284.75,"temp_min":285.22,"temp_max":285.22,"pressure":1008,"humidity":87,"sea_level":1008,"grnd_level":992},
#
# "visibility":10000,
# "wind":{"speed":2.24,"deg":336,"gust":5.25},
# "clouds":{"all":100},
# "dt":1746418937,
#
# "sys":{"type":2,"id":2003742,"country":"UA","sunrise":1746411957,"sunset":1746465793},
#
# "timezone":10800,"id":703448,"name":"Kyiv","cod":200
# }
#------------------------------------------------------

#
# сборка приложения в виде одного файла (без консоли)
# pyinstaller -w weather.py
#

from tkinter import ttk         # расширение для виджетов и тем
from ttkthemes import ThemedTk  # доп. темы
import requests                 # простые url-запросы
from tkinter import messagebox  # сообщения
import time                     # время

# API_KEY = '5e1ce895b1f7950c8267adecc8ce4989'             # 2019 (lesson)
API_KEY = 'e17444a645a7bc7f9fc670fbd48d6a00'              # default (sgiman)
API_URL = 'https://api.openweathermap.org/data/2.5/weather'


#=======================================================
# WEATHER FUNCTIONS
#=======================================================

#-------------------------------
# ВЫВОД РЕЗУЛЬТАТА
#-------------------------------
def print_weather(weather):
    try:
        city = weather['name']
        country = weather['sys']['country']
        temp = weather['main']['temp']
        press = weather['main']['pressure']
        humidity = weather['main']['humidity']
        wind = weather['wind']['speed']
        desc = weather['weather'][0]['description']         # из списка - 1-й элемент (словарь)

        sunrise_ts = weather['sys']['sunrise']
        sunset_ts = weather['sys']['sunset']
        sunrise_struct_time = time.localtime(sunrise_ts)    # локальное время с часовыми поясами
        sunset_struct_time = time.localtime(sunset_ts)
        sunrise = time.strftime("%H:%M:%S", sunrise_struct_time)    # стандартное время (ru-format)
        sunset = time.strftime("%H:%M:%S", sunset_struct_time)

        current_dt = weather['dt']
        date_struct_time = time.localtime(current_dt)
        time_local = time.strftime("%H:%M:%S", date_struct_time)

        return (f"Местоположение: {city}, {country} \n"
                f"Температура: {temp} °C \n"
                f"Атм. давление: {press} гПа \n"
                f"Влажность: {humidity}% \n"
                f"Скорость ветра: {wind} м/с \n"
                f"Погодные условия: {desc} \n"
                f"Восход: {sunrise} \n"
                f"Закат: {sunset} \n"
                f"Время текущего прогноза: {time_local}")

    except:
        return "Ошибка получения данных..."


#-------------------------------
# Получить данные погоды
#-------------------------------
def get_weather(event=''):
    if not entry.get():
        messagebox.showwarning('Warning', 'Введите запрос в формате city,country_code')
    else:
        # Словарь параметров
        params = {
            "appid": API_KEY,   # ключ
            "q": entry.get(),   # город
            "units": "metric",  # метрическая система
            "lang": "ru"        # язык
        }
        r = requests.get(API_URL, params=params)    # запрос
        weather = r.json()                          # ответ (json)
        label['text'] = print_weather(weather)      # вывод результата
        # print(weather)  # test


#==================================================
#  INTERFACE UI/UX
#==================================================

#--------------------------------
# Окно
#--------------------------------
root = ThemedTk(theme="arc")        # тема ttk
root.geometry("500x400+700+300")    # геометрия (size+location)
root.resizable(0, 0)    # запретить изменение размера окна
root.title('Получение погоды (openweathermap.org)') # заголовок

# Стиль темы
s = ttk.Style()
s.configure("TLabel", padding=5, font=("Roboto Condensed", "11", 'normal'))   # only for "label"

#--------------------------------
# Фрейм для UI-элементов
#--------------------------------
top_frame = ttk.Frame(root)
top_frame.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.1, anchor='n')

# Поле ввода
entry = ttk.Entry(top_frame)            # создать
entry.place(relwidth=0.7, relheight=1)  # разместить
#entry.insert(1, "Название города (cyr, lat)")

# Кнопка
button = ttk.Button(top_frame, text="Запрос погоды", command=get_weather)
button.place(relx=0.7, relwidth=0.3, relheight=1)

#--------------------------------
# Фрейм для вывода результата
#--------------------------------
# Result
lower_frame = ttk.Frame(root)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.9, relheight=0.6, anchor='n')
label = ttk.Label(lower_frame, anchor="nw")
label.place(relwidth=1, relheight=1)

# Info
lower_frame2 = ttk.Frame(root)
lower_frame2.place(relx=0.5, rely=0.8, relwidth=0.9, relheight=2, anchor='n')
label_info = ttk.Label(lower_frame2, anchor="nw")
label_info.place(relwidth=1, relheight=0.5)
label_info['text'] = 'Введите название города (cyr, lat) и Enter.\nНапример: "Киев" или "Киев,ua"'

#-----------------------------------------------------------------------------------------------

# отслеживание событий (bind) для "Enter"
entry.bind("<Return>", get_weather)

# главный цикл
root.mainloop()
