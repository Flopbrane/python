#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################
# Author: F.Kurokawa
# Description:
# World Market Clock
#########################
import tkinter as tk
import time
import pytz
from datetime import datetime
import holidays

def create_holidays_list():

    # 空の辞書を作成
    holidays_by_region = {}
    year_val = datetime.now().year
    # 地域のキーを追加
    holidays_by_region[("JP","")] = []
    holidays_by_region[("DE","RP")] = []
    holidays_by_region[("UK","ENG")] = []
    holidays_by_region[("US","NY")] = []
    holidays_by_region[("AU","NSW")] = []
    holidays_by_region[("NZ","AUK")] = []
    for key in holidays_by_region:
        country, city = key
        holidays_by_region[key] = holidays.CountryHoliday(country, subdiv=city, years=year_val)

    # ここで各地域の祝祭日リストを表示または処理
    # holidays_by_region.items() で辞書の各要素（キーと祝日リストの組み合わせ）にアクセスします。
    #for key, holidays_list in holidays_by_region.items(): 
    # 外側の for ループ (for key, holidays_list in holidays_by_region.items()) は、辞書の各要素を一つずつ取り出します。
    # key は国と都市の組み合わせ（例えば、("japan", "tokyo")）、holidays_list はその地域の祝日のリストです。
        #print(f"{key}:") #print(f"{key}:") で、国と都市の組み合わせを表示します。
         #内側の for ループ (for date, name in sorted(holidays_list.items())) は、祝日のリストを一つずつ取り出します。
        #for date, name in sorted(holidays_list.items()):
            #print(f"  {date}: {name}")

  

    return holidays_by_region

def update_time(holidays_by_region, year_flag):
    year_val = datetime.now().year
    if year_flag != year_val:
        year_flag = year_val
        holidays_by_region = create_holidays_list()
    # 東京の時間
    tokyo_datetime = datetime.now(pytz.timezone('Asia/Tokyo'))
    tokyo_time = tokyo_datetime.strftime('%H:%M:%S')
    tokyo_stats = 'Lording...'
    time_label_tokyo.config(text=tokyo_time)
    stats_label_tokyo.config(text=tokyo_stats)
    tokyo_day_of_week = tokyo_datetime.weekday()
    Tokyo_day = tokyo_datetime.strftime('%m/%d')
    tokyo_holiday = holidays_by_region[("JP","")]
    if tokyo_day_of_week in [5, 6] or tokyo_datetime in tokyo_holiday:
        # 週末の場合の色設定
        time_label_tokyo.config(fg='blue',bg='white')
        stats_label_tokyo.config(text='Holiday',font=('Helvetica', 11), fg='red', bg='white')
        day_label_tokyo.config(text=Tokyo_day, fg='red', bg='white')
    else:
         # 東京市場の開場時間をチェック（例：9時から17時）
        if 9 <= tokyo_datetime.hour < 17:
            time_label_tokyo.config(fg='green', bg='white')
            stats_label_tokyo.config(text='Open', font=('Helvetica', 11, 'bold'),fg='green', bg='white')
            day_label_tokyo.config(text=Tokyo_day, fg='black', bg='white')
        else:
            time_label_tokyo.config(fg='blue', bg='white')
            stats_label_tokyo.config(text='Close', font=('Helvetica', 11),fg='blue', bg='white')
            day_label_tokyo.config(text=Tokyo_day, fg='black', bg='white')            
        
    # 現在のドイツ（EU）の日時取得(Europe/Frankfurtの代わりにEurope/Berlinを使用)
    eu_datetime = datetime.now(pytz.timezone('Europe/Berlin'))
    eu_time = eu_datetime.strftime('%H:%M')
    time_label_eu.config(text=eu_time)
    stats_label_eu.config(text=eu_stats)    
    eu_day_of_week = eu_datetime.weekday()
    Eu_day = eu_datetime.strftime('%m/%d')
    eu_holiday = holidays_by_region[("DE","RP")]
    # 曜日と祝日のチェック
    if eu_day_of_week in [5, 6] or eu_datetime in eu_holiday:
        time_label_eu.config(fg='blue', bg='white')
        stats_label_eu.config(text='Holiday', font=('Helvetica', 11), fg='red', bg='white')
        day_label_eu.config(text=Eu_day, fg='red', bg='white') 
    else:
        # 市場開閉時間のチェック
        if (9, 0) <= (eu_datetime.hour, eu_datetime.minute) < (17, 30):
            time_label_eu.config(fg='green', bg='white')
            stats_label_eu.config(text='Open', font=('Helvetica', 11, 'bold'), fg='blue', bg='white')
            day_label_eu.config(text=Eu_day, fg='black', bg='white') 
        else:
            time_label_eu.config(fg='blue', bg='white')
            stats_label_eu.config(text='Close', font=('Helvetica', 11), fg='blue', bg='white')
            day_label_eu.config(text=Eu_day, fg='black', bg='white') 

    # イギリスの時間
    uk_datetime = datetime.now(pytz.timezone('Europe/London'))
    uk_time = uk_datetime.strftime('%H:%M')
    time_label_uk.config(text=uk_time)
    stats_label_uk.config(text=uk_stats)    
    uk_day_of_week = uk_datetime.weekday()
    Uk_day = uk_datetime.strftime('%m/%d')
    uk_holiday = holidays_by_region[("UK","ENG")]
    if uk_day_of_week in [5, 6] or uk_datetime in uk_holiday:
        time_label_uk.config(fg='blue', bg='white')
        stats_label_uk.config(text='Holiday', font=('Helvetica', 11), fg='red', bg='white')
        day_label_uk.config(text=Uk_day, font=('Helvetica', 11), fg='red', bg='white') 
    else:    
        if (5, 5) <= (uk_datetime.hour, uk_datetime.minute) < (7, 50):
            # プリマーケットの色設定
            time_label_uk.config(fg='orange', bg='white')
            stats_label_uk.config(text='Pre-Market', font=('Helvetica', 11, 'bold'), fg='orenge', bg='white')
            day_label_uk.config(text=Uk_day, font=('Helvetica', 11), fg='black', bg='white')
        elif (8, 0) <= (uk_datetime.hour, uk_datetime.minute) < (16, 30):
            # 通常市場の色設定
            time_label_uk.config(fg='green', bg='white')
            stats_label_uk.config(text='Open', font=('Helvetica', 11, 'bold'), fg='green', bg='white')
            day_label_uk.config(text=Uk_day, font=('Helvetica', 11), fg='black', bg='white') 
        elif (16, 40) <= (uk_datetime.hour, uk_datetime.minute) < (17, 15):
            # ポストマーケットの色設定
            time_label_uk.config(fg='purple', bg='white')
            stats_label_uk.config(text='Post-Market', font=('Helvetica', 11, 'bold'), fg='purple', bg='white')
            day_label_uk.config(text=Uk_day, font=('Helvetica', 11), fg='black', bg='white') 
        else:
            # 市場が閉まっている時間の色設定
            time_label_uk.config(fg='blue', bg='white')
            stats_label_uk.config(text='Close', font=('Helvetica', 11), fg='blue', bg='white')
            day_label_uk.config(text=Uk_day, font=('Helvetica', 11), fg='black', bg='white') 
        
    # ニューヨーク（北米）の時間
    ny_datetime = datetime.now(pytz.timezone('America/New_York'))
    ny_time = ny_datetime.strftime('%H:%M')
    time_label_ny.config(text=ny_time)    
    ny_day_of_week = ny_datetime.weekday()
    Ny_day = ny_datetime.strftime('%m/%d')   
    ny_holiday = holidays_by_region[("US","NY")]
    if ny_day_of_week in [5, 6] or ny_datetime in ny_holiday:
        time_label_ny.config(fg='blue', bg='white')
        stats_label_ny.config(text='Holiday', font=('Helvetica', 11), fg='red', bg='white')
        day_label_ny.config(text=Ny_day, font=('Helvetica', 11), fg='red', bg='white') 
    else:     
        if (4, 0) <= (ny_datetime.hour, ny_datetime.minute) < (9, 30):
            # プリマーケットの色設定
            time_label_ny.config(fg='orange', bg='white')
            stats_label_ny.config(text='Pre-Market', font=('Helvetica', 11, 'bold'), fg='orange', bg='white')
            day_label_ny.config(text=Ny_day, font=('Helvetica', 11), fg='black', bg='white') 
        elif (9, 30) <= (ny_datetime.hour, ny_datetime.minute) < (16, 0):
            # 通常市場の色設定
            time_label_ny.config(fg='green', bg='white')
            stats_label_ny.config(text='Open', font=('Helvetica', 11, 'bold'), fg='green', bg='white')
            day_label_ny.config(text=Ny_day, font=('Helvetica', 11), fg='black', bg='white') 
        elif (16, 0) <= (ny_datetime.hour, ny_datetime.minute) < (20, 0):
            # ポストマーケットの色設定
            time_label_ny.config(fg='purple', bg='white')
            stats_label_ny.config(text='Post-Market', font=('Helvetica', 11, 'bold'), fg='purple', bg='white')
            day_label_ny.config(text=Ny_day, font=('Helvetica', 11), fg='black', bg='white') 
        else:
            # 市場が閉まっている時間の色設定
            time_label_ny.config(fg='blue', bg='white')
            stats_label_ny.config(text='Close', font=('Helvetica', 11), fg='blue', bg='white')
            day_label_ny.config(text=Ny_day, font=('Helvetica', 11), fg='black', bg='white') 

    # オーストラリアの時間
    au_datetime = datetime.now(pytz.timezone('Australia/Sydney'))
    au_time = au_datetime.strftime('%H:%M')
    time_label_au.config(text=au_time)    
    au_day_of_week = au_datetime.weekday()
    Ny_day = au_datetime.strftime('%m/%d')   
    au_holiday = holidays_by_region[("AU","NSW")]
    if au_day_of_week in [5, 6] or au_datetime in au_holiday:
        time_label_au.config(fg='blue', bg='white')
        stats_label_au.config(text='Holiday', font=('Helvetica', 11), fg='red', bg='white')
        day_label_au.config(text=Ny_day, font=('Helvetica', 11), fg='red', bg='white') 
    else:     
        if (7, 0) <= (au_datetime.hour, au_datetime.minute) < (10, 0):
            # プリマーケットの色設定
            time_label_au.config(fg='orange', bg='white')
            stats_label_au.config(text='Pre-Market', font=('Helvetica', 11, 'bold'), fg='orange', bg='white')
            day_label_au.config(text=Ny_day, font=('Helvetica', 11), fg='black', bg='white') 
        elif (10, 0) <= (au_datetime.hour, au_datetime.minute) < (16, 0):
            # 通常市場の色設定
            time_label_au.config(fg='green', bg='white')
            stats_label_au.config(text='Open', font=('Helvetica', 11, 'bold'), fg='green', bg='white')
            day_label_au.config(text=Ny_day, font=('Helvetica', 11), fg='black', bg='white') 
        elif (16, 10) <= (au_datetime.hour, au_datetime.minute) < (16, 12):
            # ポストマーケットの色設定
            time_label_au.config(fg='purple', bg='white')
            stats_label_au.config(text='Post-Market', font=('Helvetica', 11, 'bold'), fg='purple', bg='white')
            day_label_au.config(text=Ny_day, font=('Helvetica', 11), fg='black', bg='white') 
        else:
            # 市場が閉まっている時間の色設定
            time_label_au.config(fg='blue', bg='white')
            stats_label_au.config(text='Close', font=('Helvetica', 11), fg='blue', bg='white')
            day_label_au.config(text=Ny_day, font=('Helvetica', 11), fg='black', bg='white') 
            
    # ニュージーランドの時間
    nz_datetime = datetime.now(pytz.timezone('Pacific/Auckland'))
    nz_time = nz_datetime.strftime('%H:%M')
    time_label_nz.config(text=nz_time)    
    nz_day_of_week = nz_datetime.weekday()
    Nz_day = nz_datetime.strftime('%m/%d')   
    nz_holiday = holidays_by_region[("NZ","AUK")]
    if nz_day_of_week in [5, 6] or nz_datetime in nz_holiday:
        time_label_nz.config(fg='blue', bg='white')
        stats_label_nz.config(text='Holiday', font=('Helvetica', 11), fg='red', bg='white')
        day_label_nz.config(text=Nz_day, font=('Helvetica', 11), fg='red', bg='white') 
    else:     
        if (10, 0) <= (nz_datetime.hour, nz_datetime.minute) < (16, 30):
            # 通常市場の色設定
            time_label_nz.config(fg='green', bg='white')
            stats_label_nz.config(text='Open', font=('Helvetica', 11, 'bold'), fg='green', bg='white')
            day_label_nz.config(text=Nz_day, font=('Helvetica', 11), fg='black', bg='white') 
        elif (16, 45) <= (nz_datetime.hour, nz_datetime.minute) < (17, 0):
            # ポストマーケットの色設定
            time_label_nz.config(fg='purple', bg='white')
            stats_label_nz.config(text='Post-Market', font=('Helvetica', 11, 'bold'), fg='purple', bg='white')
            day_label_nz.config(text=Nz_day, font=('Helvetica', 11), fg='black', bg='white') 
        else:
            # 市場が閉まっている時間の色設定
            time_label_nz.config(fg='blue', bg='white')
            stats_label_nz.config(text='Close', font=('Helvetica', 11), fg='blue', bg='white')
            day_label_nz.config(text=Nz_day, font=('Helvetica', 11), fg='black', bg='white') 
        

    
def create_label(frame, location, day='lording...', stats='Lording...', i=0):
    day_label = tk.Label(frame, text=day, font=('Helvetica', 11), fg='blue', bg='white')
    day_label.grid(row=i, column=0)
    location_label = tk.Label(frame, text=location, font=('Helvetica', 15, 'bold'), fg='blue', bg='white')
    location_label.grid(row=i, column=1)
    stats_label = tk.Label(frame, text=stats, font=('Helvetica', 11), fg='blue', bg='white')
    stats_label.grid(row=i, column=2)
    label = tk.Label(frame, font=('Helvetica', 24, 'bold'), bg='white')
    label.grid(row=i+1, column=0, columnspan=3) # このラベルは2列にまたがる
    return label, stats_label, day_label

def schedule_update():
    update_time(holidays_by_region, year_flag)
    window.after(1000, schedule_update)  # 1000ミリ秒（1秒）後に再度実行

##############################
# main
##############################

window = tk.Tk()
window.title("市場時計")
window.geometry("300x450")

main_frame = tk.Frame(window, bg='white')
main_frame.pack()  # main_frameをウィンドウに配置
# ラベルの初期化
day_label_tokyo = tk.Label(main_frame, text='Lording...', font=('Helvetica', 14), fg='blue')
day_label_eu = tk.Label(main_frame, text='Lording...', font=('Helvetica', 14), fg='blue')
day_label_uk = tk.Label(main_frame, text='Lording...', font=('Helvetica', 14), fg='blue')
day_label_ny = tk.Label(main_frame, text='Lording...', font=('Helvetica', 14), fg='blue')
day_label_au = tk.Label(main_frame, text='Lording...', font=('Helvetica', 14), fg='blue')
day_label_nz = tk.Label(main_frame, text='Lording...', font=('Helvetica', 14), fg='blue')
time_label_tokyo = tk.Label(main_frame, text='Lording...', font=('Helvetica', 14, 'bold'), fg='blue')
time_label_eu = tk.Label(main_frame, text='Lording...', font=('Helvetica', 14, 'bold'), fg='blue')
time_label_uk = tk.Label(main_frame, text='Lording...', font=('Helvetica', 14, 'bold'), fg='blue')
time_label_ny = tk.Label(main_frame, text='Lording...', font=('Helvetica', 14, 'bold'), fg='blue')
time_label_au = tk.Label(main_frame, text='Lording...', font=('Helvetica', 14, 'bold'), fg='blue')
time_label_nz = tk.Label(main_frame, text='Lording...', font=('Helvetica', 14, 'bold'), fg='blue')
stats_label_tokyo = tk.Label(main_frame, text='Lording...', font=('Helvetica', 11), fg='blue')
stats_label_eu = tk.Label(main_frame, text='Lording...', font=('Helvetica', 11), fg='blue')
stats_label_uk = tk.Label(main_frame, text='Lording...', font=('Helvetica', 11), fg='blue')
stats_label_ny = tk.Label(main_frame, text='Lording...', font=('Helvetica', 11), fg='blue')
stats_label_au = tk.Label(main_frame, text='Lording...', font=('Helvetica', 11), fg='blue')
stats_label_nz = tk.Label(main_frame, text='Lording...', font=('Helvetica', 11), fg='blue')
tokyo_stats = 'Lording...'
eu_stats = 'Lording...'
uk_stats = 'Lording...'
ny_stats = 'Lording...'
au_stats = 'Lording...'
nz_stats = 'Lording...'
day = 'Lording...'
holidays_by_region = create_holidays_list()
year_flag = datetime.now().year
# 東京
time_label_tokyo, stats_label_tokyo, day_label_tokyo = create_label(main_frame, '東京', day, tokyo_stats, 0)
# ベルギー
time_label_eu, stats_label_eu, day_label_eu = create_label(main_frame, 'ドイツ(EU)', day, eu_stats, 2)
# イギリス
time_label_uk, stats_label_uk, day_label_uk = create_label(main_frame, 'イギリス', day,  uk_stats, 4)
# ニューヨーク
time_label_ny, stats_label_ny, day_label_ny = create_label(main_frame, 'ニューヨーク', day, ny_stats, 6)
# オーストラリア
time_label_au, stats_label_au, day_label_au = create_label(main_frame, 'オーストラリア', day,  au_stats, 8)
# ニュージーランド
time_label_nz, stats_label_nz, day_label_nz = create_label(main_frame, 'ニュージーランド', day, nz_stats, 10)


window.after(1000, schedule_update)
update_time(holidays_by_region, year_flag)

window.mainloop()

