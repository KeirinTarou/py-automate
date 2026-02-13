import time
import subprocess   # 外部アプリ起動用
import pyautogui

from functions.utils import activate_window

# メモ帳を起動
subprocess.Popen("C:/Program Files (x86)/TeraPad/TeraPad.exe")
time.sleep(1)

# メモ帳ウィンドウをアクティブ化
activate_window("無題 - TeraPad")

# テキストを入力
pyautogui.write("Hello from Python automation!", interval=0.05)
pyautogui.press("enter")
pyautogui.write("This replaces AutoHotkey.")