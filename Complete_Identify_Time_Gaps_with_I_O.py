#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################
# Author: F.Kurokawa
# Description:
# 休日と時間的不連続欠損を見つける
#########################

import string
import tkinter as tk
from tkinter import filedialog, messagebox
from dateutil.parser import parse
import pandas as pd
from datetime import timedelta
"""_summary_
class FileSelector: 入力ファイル選択ダイアログ表示。
class CSVLoader: CSVファイルの読み込み時、ヘッダーチェック。
class DiscontinuousTimeCheck: 休日や時間欠損データを見つける。
------DF------
self.data: 入力して、使えるようにしたDF。
self.holidays_df: 休日相当の日付のDF。
self.time_gaps_df: 時間的欠損が存在する日時のDF。
self.time_gaps_single_df: 時間的欠損がある日時の日付を取り出したもの(1列だけのDF)。

"""

# ☆入力ファイル選択ダイアログをGUIで表示し、CSVファイル名を選択するクラス
class FileSelector:
    """
    selecl_file(): 入力ファイル選択ダイアログボックスを出しす。（ファイル名のチェック）
    """
    def __init__(self, root):
        self.root = root

    def select_file(self, filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))):
        print("Execute select_file Method")
        file_path = filedialog.askopenfilename(filetypes=filetypes)
        self.file_path = file_path
        if not file_path:
            messagebox.showerror("WM_DELETE_WINDOW","ファイル名が存在しません")
            return
        return file_path
    
class CSVLoader:
    """
    check_for_column(): ヘッダーの有無のチェックから、以下のメソッドを使用して、DFとして送り返す。
    read_and_set_columuns(): CSVファイルの記述方式をチェックして、DFに読み込む。
    check_for_header(): 1列1行目を読み込んで、文字列か、数値かを判断して、ヘッダーの有り無しを決める。
    """
    def __init__(self, file_path, start_col=None, fixed_width=False):
        # CSV ファイルを DataFrame にロードします
        self.file_path = file_path
        self.start_col = start_col
        self.fixed_width = fixed_width
        self.data = self.check_for_column()  # ここで列のチェックを行う

    def check_for_column(self):
        # 列ヘッダーがあるかどうかを判断
        with open(self.file_path, 'r') as f:
            first_line = f.readline().strip()
        # 列ヘッダーの有無と対処をしてself.dataに読み込む
        self.has_header = self.check_for_header(first_line)
        return self.read_and_set_columuns()

    def read_and_set_columuns(self):
        has_header = self.has_header
        print(f"{has_header}")
        # 固定幅のファイルの読み込み（固定幅長は逐次変更が必要）
        if self.fixed_width:
            widths = [19, 6, 7, 6, 7, 6, 7, 6, 5, 4, 5, 20, 5]  # 各カラムの幅を指定
            names = ["Origin Time", "OTerr", "Lat", "LatErr", "Long", "LonErr", "Dep", "DepErr", "Mag", "Region", "Flag"]
            self.data = pd.read_fwf(self.file_path, widths=widths, names=names, skiprows=4)  # skiprows(行飛ばし)でヘッダー部分をスキップ
        else:
            # 既存のconmma_separate_valueの読み込み処理  
            if has_header:
                self.data = pd.read_csv(self.file_path)  # 仮に10000列までとしています", usecols=range(self.start_col, 10000)"←self.file_pathの後ろに入れる。
                print(self.data.head())
            else:
                self.data = pd.read_csv(self.file_path, header=None) # ", usecols=range(self.start_col, 10000)"←Noneの後に入れる。
                # カラム数によって列名を設定
                # ここで n_cols を設定
                n_cols = self.data.shape[1]

                if n_cols == 6:
                    self.data.columns = ['DateTime', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'TICK']
                elif n_cols == 7:
                    self.data.columns = ['DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'TICK']
                else:
                    # 最初の列を'DateTime'として、残りの列にはアルファベットを割り当てます。
                    alphabet = list(string.ascii_uppercase)
                    self.data.columns = ['DateTime'] + alphabet[:n_cols-1]  
        return self.data

        # 列ヘッダーがあるかどうかをチェック
    def check_for_header(self,first_line: str):
        try:
            # 1列目だけ取り出す
            first_column_value = first_line.split(',')[0]
            # Datetime型に変換を試みる
            parse(first_column_value)
            return False   #エラーが発生しなければ、これはヘッダーではない
        except ValueError:
            return True   #エラーが発生すれば、これはヘッダー  


class DiscontinuousTimeCheck:
    """
    read_csv(): DFから、日時を読み出して、連続性を検証。24時間以上の欠損は休日、短期の欠損は時間的欠損として振り分ける。
    self.holidays_df: 休日相当の日付を記録したDF
    self.time_gaps_df: 時間的連続性を欠いた日時を記録
    time_gaps_list: time_gaps_dfの日時から、日付だけを取り出したリスト
    time_gaps_single_df: df.to_csvを供用するために、時間欠損がある日付だけをDF化したもの。
    """
    def __init__(self,file_path):
        self.loader = CSVLoader(file_path)
        self.data = self.loader.data  # CSVLoaderのデータを取得

        self.holidays_df = None  # 明示的な初期化
        self.time_gaps_df = None

    def read_csv(self):    
        # 読み込んでおいたDataFrameを呼び出す    
        df = self.data
        print(df.head())
        # 「DateTime」列をpandasの日時オブジェクトに変換します。
        df['DateTime'] = pd.to_datetime(df['DateTime'])

        # 連続する行間の時間差を計算する
        df['TimeDifference'] = df['DateTime'].diff()

        # 比較を容易にするために DateTime から日付のみを抽出します
        df['Date'] = df['DateTime'].dt.date

        # 時差が 1 日以上ある休日を特定する
        holidays_df = df[df['TimeDifference'] >= timedelta(days=1)][['Date', 'TimeDifference']]
        self.holidays_df = holidays_df
        # 時差が 1 分を超える、同じ日内の時差を特定する
        time_gaps_df = df[(df['TimeDifference'] > timedelta(minutes=1)) & (df['Date'].diff() == timedelta(days=0))][['DateTime', 'Date', 'TimeDifference']]
        # 'Date' 列をリストに変換
        date_list = time_gaps_df['Date'].tolist()
        # リストをセットに変換して重複を排除
        unique_dates = set(date_list)
        time_gaps_list = sorted(list(unique_dates))
        time_gaps_single_df = pd.DataFrame(time_gaps_list, columns=['Date'])
        return holidays_df, time_gaps_single_df
    
################
#☆General Procedure☆
################
if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw() # メインのTkウィンドウを隠す
    file_selector = FileSelector(root)
    file_path = file_selector.select_file()
    print(f"Selected file: {file_path}")
    
    cal_check = DiscontinuousTimeCheck(file_path)
    holidays_df, time_gaps_single_df = cal_check.read_csv()
    
    #  DataFrame を CSV ファイルに保存する
    # ファイルダイアログを表示
    def save_file(file_name,df):
        savef_file_path = filedialog.asksaveasfilename(filetypes=(("CSV files", "*.csv"), ("All files", "*.*")), initialfile=f'{file_name}',)
        if savef_file_path:
            print(f"Chosen file path for saving: {savef_file_path}")
            try:
                # DataFrameをCSVファイルとして保存
                df.to_csv(savef_file_path,index=False)
                print("Data successfully saved.")
            except Exception as e:
                print(f"An error occurred while saving the file: {e}")

    file_name = "holidays.csv" # 休日相当日付のCSV
    df = holidays_df
    save_file(file_name=file_name,df=df)
    file_name = "time_gaps.csv" # 時間的欠損データの有る日付のCSV
    df = time_gaps_single_df
    save_file(file_name=file_name,df=df)

    messagebox.showinfo("情報","ファイル出力が終わりました。")

    # root.mainloop() ファイル選択ダイアログやメッセージボックスを表示するためだけにtkを使っている場合、無くても問題無い。