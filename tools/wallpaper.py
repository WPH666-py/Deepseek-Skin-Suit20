# -*- coding: utf-8 -*-
"""
DeepSeek 蓝色大肥鱼 · 皮肤套件20 —— 壁纸命令行
用法示例:
  python tools/wallpaper.py grid --set            # 生成并设置全屏铺满单图(默认, cover)
  python tools/wallpaper.py 1 --set               # 生成并设置卡片单图(模糊填充 + 圆角)
  python tools/wallpaper.py random --set          # 随机换一张
  python tools/wallpaper.py all --size 1920x1080  # 生成全部模式到 ~/.deepskin20/wallpapers
  python tools/wallpaper.py cycle 30              # 每 30 分钟自动随机换壁纸(Ctrl+C 停止)
"""
import argparse
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skin_core as sc  # noqa: E402

CLI_MODES = ["grid", "1", "2", "3", "4", "random", "all", "cycle"]


def parse_size(text):
    try:
        w, h = text.lower().split("x")
        return int(w), int(h)
    except ValueError:
        raise argparse.ArgumentTypeError("尺寸格式应为 1920x1080")


def mode_of(cli_mode):
    if cli_mode in ("1", "2", "3", "4"):
        return "single" + cli_mode
    return cli_mode


def apply(mode, size=None):
    out = sc.build(mode, size)
    sc.set_wallpaper(out)
    return out


def main():
    sc.prepare_console()
    sc.ensure_pillow()
    ap = argparse.ArgumentParser(description="DeepSeek 大肥鱼20 壁纸工具")
    ap.add_argument("mode", choices=CLI_MODES, help="grid | 1-4 | random | all | cycle")
    ap.add_argument("--set", action="store_true", help="同时设置为系统壁纸")
    ap.add_argument("--out", default=sc.WALLPAPER_DIR, help="输出目录(all 模式)")
    ap.add_argument("--size", type=parse_size, default=None, help="尺寸, 如 1920x1080 (默认取屏幕分辨率)")
    ap.add_argument("--minutes", type=int, default=30, help="cycle 模式的间隔分钟数")
    args = ap.parse_args()

    if args.mode in ("1", "2", "3", "4") and int(args.mode) > len(sc.IMAGE_FILES):
        print("[deepskin] 该套件只有 %d 张素材, 单图请用 1-%d。" % (len(sc.IMAGE_FILES), len(sc.IMAGE_FILES)))
        sys.exit(1)

    size = args.size or sc.screen_size()

    if args.mode == "all":
        sc.ensure_dirs()
        print("[deepskin] 生成全部壁纸到 %s (尺寸 %dx%d):" % (os.path.abspath(args.out), size[0], size[1]))
        for key, label in sc.MODES:
            img = sc.compose(key, size)
            path = os.path.join(os.path.abspath(args.out), "%s-%dx%d.jpg" % (key, size[0], size[1]))
            img.save(path, quality=92)
            print("  ✓ %-10s %s -> %s" % (key, label, path))
        return

    if args.mode == "cycle":
        print("[deepskin] 每 %d 分钟随机换壁纸, Ctrl+C 停止。" % args.minutes)
        while True:
            key = random.choice(["grid"] + ["single%d" % i for i in range(1, len(sc.IMAGE_FILES) + 1)])
            apply(key, size)
            time.sleep(args.minutes * 60)
        return

    if args.mode == "random":
        key = random.choice(["grid"] + ["single%d" % i for i in range(1, len(sc.IMAGE_FILES) + 1)])
        apply(key, size)
        return

    key = mode_of(args.mode)
    out = sc.build(key, size)
    print("[deepskin] 已生成: %s" % out)
    if args.set:
        sc.set_wallpaper(out)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
