#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################
# Author: F.Kurokawa
# Description:
#  二画面のテキストエディタ(wxPythonモジュール使用)
#########################

import sys
import wx
import wx.stc as stc

# ☆入力ファイル選択ダイアログをGUIで表示し、CSVファイル名を選択するクラス
class FileSelector:
    def __init__(self, parent):
        self.parent = parent
        self.file_path = ""

    def select_file(self, filetypes="Text files (*.txt)|*.txt|All files (*.*)|*.*"):
        print("Execute select_file Method")
        file_dialog = wx.FileDialog(self.parent, "ファイルを選択してください", wildcard=filetypes, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if file_dialog.ShowModal() == wx.ID_OK:
            self.file_path = file_dialog.GetPath()
        else:
            wx.MessageBox("ファイルが選択されませんでした。", "エラー", wx.ICON_ERROR)
            sys.exit(1)
        file_dialog.Destroy() # ダイアログリソースを解放
        return self.file_path

class ReadFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = ""
    def read_file(self):
        print("Execute read_file Method")
        with open(self.file_path, mode='r', encoding='utf-8') as f:
            self.text = f.read()
            print(type(self.text))
            
            if self.text != "":
                print("ファイルを読み込みました。")
                return self.text
            else:
                wx.MessageBox("ファイルが空です。")
                return ""

class SaveFileDialog:
    def __init__(self, parent):
        self.parent = parent
        self.file_path = ""
    def save_file(self, filetypes="Text files (*.txt)|*.txt|All files (*.*)|*.*"):
        with wx.FileDialog(self, "ファイルを保存", wildcard="テキストファイル (*.txt)|*.txt",
                        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return  # ユーザーがキャンセルした場合
            self.file_path = file_dialog.GetPath()  # ファイルパスを取得
        # with ブロックを抜けると自動的に Destroy が呼び出される
        return self.file_path
    
class WriteFile:
    def __init__(self, file_path):
        self.file_path = file_path
    def write_file(self, text):
        with open(self.file_path, mode='w', encoding='utf-8') as f:
            f.write(text)
            print("ファイルを書き込みました。")
    
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(1000, 800)) # MyFrameがMainFrameに該当
        self.parent = parent
        self.title = title
        self.size = (1000, 800)
        self.create_menu() # メニューの作成
        #self.CreateStatusBar() # ステータスバーの作成
        self.sw = 0
        self.panel = wx.Panel(self)# 親パネル
        self.splitter = wx.SplitterWindow(self.panel) # 子パネルに相当
        # パネル1とパネル2の作成
        self.panel1 = wx.Panel(self.splitter, style=wx.SUNKEN_BORDER) # 孫パネルに相当
        self.panel2 = wx.Panel(self.splitter, style=wx.SUNKEN_BORDER) # 孫パネルに相当
        self.control_panel = wx.Panel(self.panel, style=wx.SUNKEN_BORDER) # 孫パネルに相当
        self.splitter.SplitVertically(self.panel1, self.panel2)
        # パネル1とパネル2にテキストボックスを追加
        self.text_ctrl1 = stc.StyledTextCtrl(self.panel1, style=wx.TE_MULTILINE)# (親パネル, スタイル)
        self.text_ctrl2 = stc.StyledTextCtrl(self.panel2, style=wx.TE_MULTILINE)# (親パネル, スタイル)
         # 行番号を表示
        self.text_ctrl1.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.text_ctrl2.SetMarginType(1, stc.STC_MARGIN_NUMBER)
         # 行番号の幅を設定
        self.text_ctrl1.SetMarginWidth(1, 20)
        self.text_ctrl2.SetMarginWidth(1, 20)
        #self.text_ctrl1.SetValue(text)
        self.checkbox_twin = wx.CheckBox(self.control_panel, label="二画面化")
        self.scroll_lock_checkbox = wx.CheckBox(self.control_panel, label="スクロールバー・ロック")
        # 各パネルのレイアウト設定
        self.panel1_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel1_sizer.Add(self.text_ctrl1, 1, wx.EXPAND | wx.ALL, 5) # (オブジェクト, 比率, フラグ, 余白)
        self.panel1.SetSizer(self.panel1_sizer)
        self.panel2_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel2_sizer.Add(self.text_ctrl2, 1, wx.EXPAND | wx.ALL, 5)
        self.panel2.SetSizer(self.panel2_sizer)
        self.control_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)  
        self.control_panel_sizer.Add(self.checkbox_twin, 0, wx.ALL | wx.CENTER, 5)
        self.control_panel_sizer.Add(self.scroll_lock_checkbox, 0, wx.ALL | wx.CENTER, 5)
        self.control_panel.SetSizer(self.control_panel_sizer)
        #self.splitter.SplitVertically(self.panel1, self.panel2,sashPosition = 500)
        #self.splitter.SetMinimumPaneSize(500)
        #self.splitter.Unsplit()  # 初期状態では画面を分割しない
        # 初期状態で二画面化のチェックボックスがオフの場合、Unsplitを呼び出す
        # 二画面化のチェックボックスを追加
        self.checkbox_twin.Bind(wx.EVT_CHECKBOX, self.on_checkbox_twin) #(イベント, メソッド)
        self.checkbox_twin.SetValue(False) # デフォルトではオフにする
        self.on_checkbox_twin(None) # Unsplitを呼び出して初期状態を設定する
        
        # スクロールバーロックのチェックボックスを追加
        self.scroll_lock_checkbox.Bind(wx.EVT_CHECKBOX, self.on_scroll_lock_changed)
        # スクロールイベントのバインド
        self.text_ctrl1.Bind(stc.EVT_STC_UPDATEUI, self.on_scroll_text1)
        self.text_ctrl2.Bind(stc.EVT_STC_UPDATEUI, self.on_scroll_text2)

        sizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.Add(self.checkbox, 0, wx.ALL | wx.EXPAND, 5) # (オブジェクト, 比率, フラグ, 余白)
        sizer.Add(self.splitter, 1, wx.EXPAND) # (オブジェクト, 比率, フラグ, 余白)
        # メインサイザーにコントロールパネルを追加
        sizer.Add(self.control_panel, 0, wx.EXPAND | wx.ALL, 5)
        self.panel.SetSizer(sizer)
        self.panel.Layout()
        self.Layout()

    def create_menu(self):
        #ファイルメニュー
        f_menu = wx.Menu()
        clear = f_menu.Append(-1, "消去", "テキスト消去")
        input_file = f_menu.Append(-1, "ファイル読込\tCtrl-O", "ファイル読込")
        write_file = f_menu.Append(-1, "ファイル保存\tCtrl-S", "ファイル保存")
        exit = f_menu.Append(-1, "終了\tCtrl-E", "終了します")
        #選択メニュー
        s_menu = wx.Menu()
        tex1 = s_menu.Append(-1, "画面1\tF1", "画面1を選択します")
        tex2 = s_menu.Append(-1, "画面2\tF2", "画面2を選択します")
        #メニューバーの基本設定
        m_bar = wx.MenuBar()
        m_bar.Append(f_menu, "ファイル(&F)")
        m_bar.Append(s_menu, "選択(&S)")
        self.SetMenuBar(m_bar)
        #イベント設定
        self.Bind(wx.EVT_MENU, self.ClearText, clear)
        self.Bind(wx.EVT_MENU, self.OpenFile, input_file)
        self.Bind(wx.EVT_MENU, self.SaveFile, write_file)
        self.Bind(wx.EVT_MENU, self.OnClose, exit)
        self.Bind(wx.EVT_MENU, self.OnSelect1, tex1)
        self.Bind(wx.EVT_MENU, self.OnSelect2, tex2)

    def sync_scroll(self, scrolled_text, target_text):
        first_visible_line = scrolled_text.GetFirstVisibleLine()
        target_text.ScrollToLine(first_visible_line)

    def on_scroll_text1(self, event):
        if self.scroll_lock_checkbox.IsChecked():
            self.sync_scroll(self.text_ctrl1, self.text_ctrl2)
        event.Skip()  # 重要：スクロールイベントをスキップしてデフォルトの処理を続行する

    def on_scroll_text2(self, event):
        if self.scroll_lock_checkbox.IsChecked():
            self.sync_scroll(self.text_ctrl2, self.text_ctrl1)
        event.Skip()  # 重要：スクロールイベントをスキップしてデフォルトの処理を続行する

    def on_scroll_lock_changed(self, event):
        # スクロールバーロックの状態が変更されたときの処理（必要に応じて）
        pass

    def on_checkbox_twin(self, event):
        twin_flag = self.checkbox_twin.IsChecked()
        if self.checkbox_twin.IsChecked():
            # スプリット状態を確保
            if not self.splitter.IsSplit():
                self.splitter.SplitVertically(self.panel1, self.panel2)
                self.panel2_sizer.Show(self.text_ctrl2) # text_ctrl2を再表示
                self.text_ctrl2.SetValue(self.text_ctrl1.GetValue())
                self.panel2.Layout() # サイズイベントを送信
        else:
            # スプリット状態を解除
            self.splitter.Unsplit()
            self.panel2_sizer.Hide(self.text_ctrl2)
        self.panel.Layout()

    def OnSelect1(self, event):
        self.sw = 0
        self.text_ctrl1.SetFocus()
        
    def OnSelect2(self, event):
        if self.sw == 0:
            self.sw = 1
            self.checkbox_twin.SetValue(True)
            self.on_checkbox_twin(None)
        else:            
            self.sw = 1
            self.text_ctrl2.SetFocus()

    def ClearText(self, event):
        if self.sw == 0:
            self.text_ctrl1.Clear()
        else:
            self.text_ctrl2.Clear()

    def OpenFile(self, event):
        file_selector = FileSelector(self)
        file_path = file_selector.select_file()
        read_file = ReadFile(file_path)
        text = read_file.read_file()
        if self.sw == 0:
            self.text_ctrl1.SetValue(text)
        elif self.sw == 1:
            self.text_ctrl2.SetValue(text)
        else:
            wx.MessageBox("どちらかの画面を選択してください。")
            return
    def SaveFile(self, event):
        if self.sw == 0:
            text = self.text_ctrl1.GetValue()
        elif self.sw == 1:
            text = self.text_ctrl2.GetValue()
        else:
            wx.MessageBox("どちらかの画面を選択してください。")
            return        
        file_selector = SaveFileDialog(self)
        file_path = file_selector.save_file()
        write_file = WriteFile(file_path)
        write_file.write_file(text)

    def on_check_focus(self, event):
        focused_window = wx.Window.FindFocus()
        if focused_window == self.text_ctrl1:
            self.sw = 0
            print("フォーカスは text_ctrl1 にあります。")
        elif focused_window == self.text_ctrl2:
            self.sw = 1
            print("フォーカスは text_ctrl2 にあります。")
        else:
            self.sw = 2
            print("フォーカスは他のウィジェットにあります。")

    def OnClose(self, event):
        self.Close()
        


###############################
# main
###############################

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None, "SplitterWindow")
    frame.Show()
    app.MainLoop()
