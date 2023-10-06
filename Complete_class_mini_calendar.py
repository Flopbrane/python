#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################
# Author: F.Kurokawa
# Description:
# class MiniCalendar
# Output format: YYYY-MM-DD
#########################
import tkinter as tk
import calendar
from datetime import datetime

class MiniCalendar:
    def __init__(self, master):
        """_summary_
        ミニカレンダーのウインドの設定
        Args:
            master (_type_): _description_
            cal_frame:カレンダーフレーム
            year_var, month_var:実行日の月日
        """
        self.master = master
        self.master.title("Mini Calendar")
        self.master.geometry("360x240")
        self.cal_frame = tk.Frame(self.master)
        #self.cal_frame.pack(pady=2) # ここでpackすると、年入力、月選択が、一番下に来てしまう。

        self.now = datetime.now()
        self.year_var = tk.StringVar()
        self.year_var.set(str(self.now.year))
        self.month_var = tk.StringVar()
        self.month_var.set(str(self.now.month))
        self.month_var.trace_add("write", self.update_calendar)  # この行を追加

        self.setup_ui() # setup_uiメソッドを呼び出す

    def update_calendar(self, *args):  # このメソッドを追加
        # 月リストを変更したら、カレンダー自体も変更させるために呼び出し
        self.show_calendar()

    def setup_ui(self):
        """
        top_frame:カレンダーのウインド上端
        year_entry:年のテキストボックス
        month_list:1～12までの月リスト

        """
        top_frame = tk.Frame(self.master)
        top_frame.pack(side=tk.TOP, pady=10) # この行をここに移動

        year_entry = tk.Entry(top_frame, textvariable=self.year_var, width=5)
        year_entry.pack(side=tk.LEFT)
        year_label = tk.Label(top_frame, text="年")
        year_label.pack(side=tk.LEFT)

        month_list = [str(i) for i in range(1, 13)]  # 1から12までの月のリスト
        month_option = tk.OptionMenu(top_frame, self.month_var, *month_list)
        month_option.pack(side=tk.LEFT)
        month_label = tk.Label(top_frame, text="月")
        month_label.pack(side=tk.LEFT)
        # ボタンでカレンダーを変更する場合
        #show_cal_button = tk.Button(top_frame, text="Show Calendar", command=self.show_calendar)
        #show_cal_button.pack(side=tk.LEFT)
        self.cal_frame.pack(pady=2)
        self.show_calendar()

    def show_calendar(self):
        # ウインド表示の消去
        for widget in self.cal_frame.winfo_children():
            widget.destroy()

        year = int(self.year_var.get())
        month = int(self.month_var.get())
        
        # テキストカレンダーを使う場合
        # calendar.setfirstweekday(calendar.SUNDAY)
        # cal = calendar.TextCalendar()

        # 曜日を表示する
        days_of_week = ["日", "月", "火", "水", "木", "金", "土"]
        for i, day in enumerate(days_of_week):
            tk.Label(self.cal_frame, text=day).grid(row=2, column=i)
        
        # 日ごとのボタンを表示する
        self.clear_buttons(year, month)

    def get_date(self, date):
        year = self.year_var.get()
        month = self.month_var.get()
        self.formatted_date = f"{year}-{month}-{date}"
        print(f"Selected date is: {self.formatted_date}")

    def clear_buttons(self, year, month):
        first_day_of_month = (datetime(year, month, 1).weekday() + 1)% 7 # 日曜日を0として扱う
        buttons = []
        
        for i in range(6):
            row_buttons = []
            for j in range(7):
                btn = tk.Button(self.cal_frame, text="", width=5, command=lambda date="": self.get_date(date))
                btn.grid(row=i+3, column=j)
                row_buttons.append(btn)
            buttons.append(row_buttons)

        day = 1
        for i in range(6):
            for j in range(7):
                if i == 0 and j < first_day_of_month:
                    buttons[i][j].grid_remove()
                    continue
                if day > calendar.monthrange(year, month)[1]:
                    buttons[i][j].grid_remove()
                    continue
                buttons[i][j].config(text=str(day), command=lambda day=day: self.get_date(day))
                day += 1

if __name__ == '__main__':
    root = tk.Tk()
    app = MiniCalendar(root)
    root.mainloop()
