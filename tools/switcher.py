# -*- coding: utf-8 -*-
"""
DeepSeek 蓝色大肥鱼 · 皮肤套件 —— 可视化切换器
用法: python tools/switcher.py
支持: 预览 5 种壁纸样式、一键应用、每 30 分钟自动随机、一键启动桌宠
"""
import os
import random
import sys
import threading
import time
import subprocess
import tkinter as tk
from tkinter import ttk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skin_core as sc  # noqa: E402

PREVIEW_SIZE = (1280, 720)
AUTO_INTERVAL = 30 * 60  # 秒


def spawn_gui(script):
    """用 pythonw 启动 GUI 子脚本, 避免弹出黑色控制台窗口。"""
    exe = sys.executable
    if os.name == "nt":
        w = os.path.join(os.path.dirname(exe), "pythonw.exe")
        if os.path.exists(w):
            exe = w
    subprocess.Popen([exe, os.path.join(sc.TOOLS_DIR, script)], cwd=sc.TOOLS_DIR)


class App:
    def __init__(self, root):
        import PIL.Image
        import PIL.ImageTk
        self.PIL = PIL
        self.root = root
        root.title("DeepSeek 大肥鱼20 · 皮肤切换器")
        root.configure(bg="#f5f8fd")
        root.geometry("920x430")
        root.resizable(False, False)

        self.canvas = tk.Label(root, bg="#e9eff8", bd=1, relief="solid")
        self.canvas.pack(side="left", padx=14, pady=14)

        right = ttk.Frame(root)
        right.pack(side="left", fill="y", padx=(6, 14), pady=14)
        ttk.Label(right, text="选择壁纸样式").grid(row=0, column=0, sticky="w", pady=(0, 8))

        self.var = tk.StringVar(value="grid")
        for i, (key, label) in enumerate(sc.MODES):
            ttk.Radiobutton(
                right, text=label, value=key, variable=self.var, command=self.show_preview
            ).grid(row=1 + i, column=0, sticky="w", pady=2)

        row = 1 + len(sc.MODES)
        ttk.Button(right, text="应用到桌面", command=lambda: self.apply(self.var.get())).grid(
            row=row, column=0, sticky="ew", pady=(12, 4)
        )
        ttk.Button(
            right, text="随机来一张", command=lambda: self.apply(random.choice([m[0] for m in sc.MODES]))
        ).grid(row=row + 1, column=0, sticky="ew", pady=4)
        self.auto = tk.BooleanVar(value=False)
        ttk.Checkbutton(right, text="每 30 分钟自动随机", variable=self.auto).grid(
            row=row + 2, column=0, sticky="w", pady=4
        )
        ttk.Button(right, text="启动桌面桌宠", command=lambda: spawn_gui("pet.py")).grid(
            row=row + 3, column=0, sticky="ew", pady=(8, 0)
        )
        self.status = ttk.Label(right, text="就绪", foreground="#1c4e9c")
        self.status.grid(row=row + 4, column=0, sticky="w", pady=(12, 0))

        self.last_auto = time.time()
        self.root.after(60000, self._tick)
        self.show_preview()

    def _tick(self):
        if self.auto.get() and time.time() - self.last_auto >= AUTO_INTERVAL:
            self.last_auto = time.time()
            self.apply(random.choice([m[0] for m in sc.MODES]))
        self.root.after(60000, self._tick)

    def show_preview(self, *_):
        mode = self.var.get()
        try:
            img = sc.compose(mode, PREVIEW_SIZE)
            tmp = os.path.join(sc.APP_DIR, "preview.png")
            img.save(tmp)
            ph = self.PIL.ImageTk.PhotoImage(self.PIL.Image.open(tmp))
            self.canvas.configure(image=ph)
            self.canvas.image = ph  # 防 GC
        except Exception as e:
            self.status.configure(text="预览失败: %s" % e)

    def apply(self, mode):
        def work():
            try:
                out = sc.build(mode, force=True)
                sc.set_wallpaper(out)
                self.root.after(0, lambda: self.status.configure(text="已应用: %s" % mode))
            except Exception as e:
                self.root.after(0, lambda: self.status.configure(text="应用失败: %s" % e))

        threading.Thread(target=work, daemon=True).start()


def main():
    sc.prepare_console()
    sc.ensure_pillow()
    sc.ensure_dirs()
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
