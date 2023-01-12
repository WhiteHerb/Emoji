from os.path import exists
from time import sleep
from threading import Thread
from pyautogui import hotkey
from tkinter import Tk, Button, ttk, messagebox, Frame, StringVar, Entry
from win32api import GetKeyState
from pyperclip import copy


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
    with open("./Emojis.txt", "a", encoding="utf-8") as F:
        F.writelines("\n" + new_emoji.get())
        messagebox.showinfo("성공!", f"{new_emoji.get()}을 추가했습니다")
        Button(frame_e, text=new_emoji.get(), command=lambda: write_emoji(new_emoji.get()), height=1).pack(
            side="left")


def set_focus(i: bool):
    global is_focus
    is_focus = i


is_focus = True
if not exists("./Emojis.txt"):
    open("./Emojis.txt", 'a').close()
    messagebox.showinfo("에러!", "이모지 초기화! Emojis.txt 파일이 같은 위치에 없습니다")
window = Tk()
window.wm_attributes("-topmost", 1)
window.wm_attributes("-toolwindow", 1)
window.title("이모지")
window.bind("<FocusIn>", lambda x: set_focus(True))
window.bind("<FocusOut>", lambda x: set_focus(False))

frame_add = Frame(window)
new_emoji = StringVar()
Entry(frame_add, textvariable=new_emoji).pack(side="left")
Button(frame_add, text="이모지 추가 하기", command=add_emoji).pack(side="left")

frame_e = Frame(window)
style = ttk.Style()
style.configure("TButton", padding=3, borderwidth=4, font=('calibri', 20, 'bold'))
list(map(lambda i: Button(frame_e, text=i, command=lambda: write_emoji(i), height=1).pack(side="left"), open(
    './Emojis.txt', 'r', encoding="utf-8").readlines()))
frame_add.pack()
frame_e.pack(side="top")
window.mainloop()
