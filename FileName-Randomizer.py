import os
import random
import string
import tkinter as tk
import win32api
import win32con
import win32gui

# ウィンドウ設定
root = tk.Tk()
root.geometry("400x200")
root.title("FileName Randomizer")
root.attributes("-topmost", True)

# ウィンドウのスタイルを設定する
hwnd = root.winfo_id()
style = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
style |= win32con.WS_EX_ACCEPTFILES
win32api.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)

# WM_DROPFILES メッセージを処理する関数を定義する
def on_dropfiles(hdrop):
    num_files = win32api.DragQueryFile(hdrop)
    for i in range(num_files):
        file_path = win32api.DragQueryFile(hdrop, i)

        # 拡張子を取得
        file_extension = os.path.splitext(file_path)[1]

        # ファイル名をランダムな32文字の英数字に置き換える
        random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        new_file_path = os.path.join(os.path.dirname(file_path), random_name + file_extension)
        
        # リネーム
        os.rename(file_path, new_file_path)
    
    win32api.DragFinish(hdrop)

# WM_DROPFILES メッセージを受け取るためのウィンドウプロシージャを設定する
def wndproc(hwnd, msg, wParam, lParam):
    if msg == win32con.WM_DROPFILES:
        on_dropfiles(wParam)
    else:
        return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)
    return 0

# ウィンドウプロシージャを設定する
win32gui.SetWindowLong(hwnd, win32con.GWL_WNDPROC, wndproc)

# ラベルを作成する
label = tk.Label(root, text="ファイルをドラッグアンドドロップしてください", font=("Arial", 12, "bold"), fg="gray")
# ウィンドウの中央に配置する
label.place(relx=0.5, rely=0.5, anchor="center")


root.mainloop()
