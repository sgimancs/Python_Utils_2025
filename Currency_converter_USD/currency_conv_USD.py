# coding=utf-8
#######################################################
# Программа Конвертер валют (USD)
# python 3.x
# WebForMySelf - Андрей Кудлай, 2019
#######################################################
# Writing sgiman, 2025

#
# сборка приложения в виде одного файла (без консоли)
# pyinstaller -w currency_conv_ua.py
# python -m nuitka --windows-console-mode=disable
#

#------------------------------------------------------
# Курсы валют PRIVATBANK
#------------------------------------------------------
# https://api.privatbank.ua/#p24/exchange
#
# PRIVAT API:
# Наличные
# https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5
# [{"ccy":"EUR","base_ccy":"UAH","buy":"46.70000","sale":"47.70000"},
# {"ccy":"USD","base_ccy":"UAH","buy":"41.25000","sale":"41.85000"}]
#
# Безнал (cards)
# https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=11
# [{"ccy":"EUR","base_ccy":"UAH","buy":"46.80000","sale":"47.84689"},
# {"ccy":"USD","base_ccy":"UAH","buy":"41.35000","sale":"41.84100"}]
#

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import urllib.request
import json


#================================
#  W I N D O W
#================================
root = Tk()
root.title('Privatbank (USD) - for Cards')
root.geometry("400x250+700+300")
root.resizable(False, False)    # изменяемый размер окна (запретить W & H)
root.iconbitmap('nt.ico')                   # иконка
START_AMOUNT = 100                          # SUMA (default)


#================================
#  F u n c t i o n s
#================================
def exchange():
    # очистить поля валют
    e_uah.delete(0, END)
    # Попытка конвертировать валюту
    try:
        e_uah.insert(0, round(float(e_usd.get()) * float(JSON_object[1]['sale']), 2))
    except:
        messagebox.showwarning('Warning', 'Проверьте введенную сумму')


# Попытка получить JSON (от API PRIVAT)
try:
    # html = urllib.request.urlopen('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5') # наличные
    html = urllib.request.urlopen('https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=11')        # безнал (cards)
    data = html.read()
    JSON_object = json.loads(data)  # текущие данные валют
except:
    messagebox.showerror("Error", 'Ошибка получения курсов валют.\nНет подключения к интернет.')
    # root.destroy()  # quit (exit)

#---------------------------------
# Header Frame
#---------------------------------
header_frame = Frame(root)
header_frame.pack(fill=X)

# Равномерное размещение колонок заголовков по весу (таблица)
header_frame.grid_columnconfigure(0, weight=1)
header_frame.grid_columnconfigure(1, weight=1)
header_frame.grid_columnconfigure(2, weight=1)

# Header (ряд 0) - чёрный
h_currency = Label(header_frame, text="Валюта", bg="#000", fg="#fff", font="Arial 12 bold")
h_currency.grid(row=0, column=0, sticky=EW)
h_buy = Label(header_frame, text="Покупка", bg="orange", fg="white", font="Arial 12 bold")
h_buy.grid(row=0, column=1, sticky=EW)
h_sale = Label(header_frame, text="Продажа", bg="blue", fg="white", font="Arial 12 bold")
h_sale.grid(row=0, column=2, sticky=EW)

# USD course (ряд 1)
usd_currency = Label(header_frame, text="USD", bg="#ccc", font="Arial 10")
usd_currency.grid(row=1, column=0, sticky=EW)
usd_buy = Label(header_frame, text=JSON_object[1]['buy'], bg="#ccc", font="Arial 10")
usd_buy.grid(row=1, column=1, sticky=EW)
usd_sale = Label(header_frame, text=JSON_object[1]['sale'], bg="#ccc", font="Arial 10")
usd_sale.grid(row=1, column=2, sticky=EW)

# EUR course (ряд 2) - серый
# eur_currency = Label(header_frame, text="EUR", font="Arial 10")
# eur_currency.grid(row=2, column=0, sticky=EW)
# eur_buy = Label(header_frame, text=JSON_object[0]['buy'],  font="Arial 10")
# eur_buy.grid(row=2, column=1, sticky=EW)
# eur_sale = Label(header_frame, text=JSON_object[0]['sale'], font="Arial 10")
# eur_sale.grid(row=2, column=2, sticky=EW)

# Calc Frame
calc_frame = Frame(root, bg="#fff")
calc_frame.pack(expand=1, fill=BOTH)                  # разместить и растянуть
calc_frame.grid_columnconfigure(1, weight=1)    # на всю ширину фрейма

# USD (вводимая сумма в USD)
l_usd = Label(calc_frame, text="USD:", bg="#fff", font="Arial 10 bold")
l_usd.grid(row=0, column=0, padx=10)
e_usd = ttk.Entry(calc_frame, justify=CENTER, font="Arial 10")
e_usd.grid(row=0, column=1, columnspan=2, pady=10, padx=10, sticky=EW)
e_usd.insert(0, START_AMOUNT)   # подставить сумму по умолчанию

#-----------------------
# Button ("Обмен")
#-----------------------
# btn_calc = ttk.Button(calc_frame, text="Обмен", command=exchange)   # ttk style
btn_calc = Button(calc_frame, text="Обмен", font=("Arial",'10','bold'), fg="white", bg="red", command=exchange)  # standard style
btn_calc.grid(row=1, column=1, columnspan=2, sticky=EW, padx=10)

#========================
#  R E S U L T (table)
#========================
# Result Frame
res_frame = Frame(root)
res_frame.pack(expand=1, fill=BOTH, pady=5)
res_frame.grid_columnconfigure(1, weight=1)

# UAH (entry)
l_uah = Label(res_frame, text="UAH:", font="Arial 10 bold")
l_uah.grid(row=2, column=0)
e_uah = ttk.Entry(res_frame, justify=CENTER, font="Arial 10")
e_uah.grid(row=2, column=1, columnspan=2, padx=10, sticky=EW)
e_uah.insert(0, round(START_AMOUNT * float(JSON_object[1]['sale']), 2))     # конвертация USD

# # EUR (entry)
# l_eur = Label(res_frame, text="EUR:", font="Arial 10 bold")
# l_eur.grid(row=3, column=0)
# e_eur = ttk.Entry(res_frame, justify=CENTER, font="Arial 10")
# e_eur.grid(row=3, column=1, columnspan=2, padx=10, sticky=EW)
# e_eur.insert(0, round(START_AMOUNT * float(JSON_object[1]['sale']), 2))     # конвертация EUR


root.mainloop()
