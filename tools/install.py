# -*- coding: utf-8 -*-
"""
DeepSeek 蓝色大肥鱼 · 皮肤套件20 —— 一键安装
用法: python tools/install.py
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skin_core as sc  # noqa: E402


def run(cmd):
    print("$ " + " ".join(cmd))
    subprocess.check_call(cmd)


def main():
    sc.prepare_console()
    print("=" * 56)
    print("  DeepSeek 蓝色大肥鱼 · 皮肤套件20 安装器")
    print("=" * 56)
    sc.ensure_pillow()
    sc.ensure_dirs()

    size = sc.screen_size()
    print("[1/3] 生成默认壁纸 (%dx%d) ..." % size)
    out = sc.build("grid", size, force=True)
    print("      -> %s" % out)

    print("[2/3] 设置为系统壁纸 ...")
    sc.set_wallpaper(out)

    print("[3/3] 完成! 后续玩法:")
    print("  • 皮肤切换器(可视化):  python tools/switcher.py")
    print("  • 桌面桌宠:             python tools/pet.py")
    print("  • 随机换壁纸(30 分钟): python tools/wallpaper.py cycle 30")
    print("  • 卡片单图:             python tools/wallpaper.py 1 --set")
    print("  • VSCode/Trae/CodeX:   vscode/ 目录扩展, 见 README.md")
    print("  • PyCharm 等:          ide/jetbrains/README.md。")
    print(" 素材与说明都在本仓库, 给任意 AI 发仓库链接即可重新安装。")


if __name__ == "__main__":
    main()
