import ctypes.wintypes
import os.path
import subprocess
from os.path import exists
from threading import Thread
from time import sleep
from tkinter import Tk, Button, ttk, messagebox, Frame, StringVar, Entry

from pyautogui import hotkey
from pyperclip import copy
from win32api import GetKeyState


class Hook(Thread):
    def __init__(self, emoji):
        super(Hook, self).__init__()
        self.daemon = True
        self.emoji = emoji

    def run(self):
        while True:
            if GetKeyState(0x01) and not is_focus:
                copy(self.emoji)
                sleep(0.1)
                hotkey("ctrl", "v")
                break


def write_emoji(emoji):
    h = Hook(emoji)
    h.start()


def add_emoji():
    if new_emoji.get() == "":
        return
    with open(path, "r", encoding="utf-8") as F:
        if new_emoji.get() in F.read():
            messagebox.showinfo("중복!", f"{new_emoji.get()}가 이미 존재합니다")
            return
    with open(path, "a", encoding="utf-8") as F:
        F.writelines("\n" + new_emoji.get())
        messagebox.showinfo("성공!", f"{new_emoji.get()}을 추가했습니다")
        Button(frame_e, text=new_emoji.get(), command=lambda: write_emoji(new_emoji.get()), height=1).pack(
            side="left")
        new_emoji.set("")


def set_focus(i: bool):
    global is_focus
    is_focus = i


def openfile():
    subprocess.Popen(f'explorer /select,"{path}"')


buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf)

path = os.path.join(buf.value, "Emojis.txt")
is_focus = True
if not exists(path):
    open(path, 'a').close()
    messagebox.showinfo("에러!", f"이모지 초기화! Emojis.txt 파일이 같은 위치에 없습니다 {path} 위치에 재생성합니다")
window = Tk()
window.wm_attributes("-topmost", 1)
window.wm_attributes("-toolwindow", 1)
window.title("이모지")
window.bind("<FocusIn>", lambda x: set_focus(True))
window.bind("<FocusOut>", lambda x: set_focus(False))
window.bind("<Return>", lambda x: add_emoji())

window.geometry("-0-40")

frame_add = Frame(window)
new_emoji = StringVar()
Button(frame_add, text="새로고침", command=lambda: list(
    map(lambda i: Button(frame_e, text=i, command=lambda: write_emoji(i), height=1).pack(side="left"),
        open(path, 'r', encoding="utf-8").readlines()))).pack(side="left")
Entry(frame_add, textvariable=new_emoji).pack(side="left")
Button(frame_add, text="이모지 추가하기", command=add_emoji).pack(side="left")
Button(frame_add, text="이모지 파일 열기", command=openfile).pack(side="left")

frame_e = Frame(window)
style = ttk.Style()
style.configure("TButton", padding=3, borderwidth=4, font=('calibri', 20, 'bold'))
list(map(lambda i: Button(frame_e, text=i, command=lambda: write_emoji(i), height=1).pack(side="left"), open(
    path, 'r', encoding="utf-8").readlines()))
frame_add.pack()
frame_e.pack(side="top")
window.mainloop()
