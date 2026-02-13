import time
import pyautogui
from pygetwindow import Window
from typing import Optional

def wait_window(title: str, timeout: int = 10) -> Window | None:
    """ 指定したウィンドウタイトルを持つウィンドウの表示を待つ
    
    :param title: ウィンドウのタイトル
    :type title: str
    :param timeout: タイムアウト秒数
    :type timeout: int
    """
    start = time.time()

    while time.time() - start < timeout:
        wins = pyautogui.getWindowsWithTitle(title)
        if wins:
            return wins[0]
        time.sleep(0.1)

    return None

def activate_window(title: str, timeout: int = 10):
    """ 指定したウィンドウをアクティブにする

    - ウィンドウが見つからないときはNoneを返す
    :param title: ウィンドウのタイトル
    :type title: str
    :param timeout: タイムアウト秒数
    :type timeout: int
    """
    win = wait_window(title, timeout)
    if win:
        win.activate()
        time.sleep(0.5)
        return win
    return None
