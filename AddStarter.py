import os
from win32com.client import Dispatch
import win32api

path = os.path.join(os.getenv("APPDATA"), r"Microsoft\Windows\Start Menu\Programs\Startup", "Mojiboard.lnk")
wDir = os.getcwd()
target = f"{os.getcwd()}\\Mojiboard.exe"

shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(path)
shortcut.Targetpath = target
shortcut.WorkingDirectory = wDir
shortcut.IconLocation = target
shortcut.save()
win32api.MessageBox(0, "시작프로그램으로 설정했습니다", "끝!", 0)
