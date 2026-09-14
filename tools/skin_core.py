# -*- coding: utf-8 -*-
"""
DeepSeek 蓝色大肥鱼 · 皮肤套件20 —— 核心库
跨平台: Windows / macOS / Linux
功能: 素材定位、全屏单图(cover)、完整卡片单图(适合屏幕)、系统壁纸设置
"""
import os
import platform
import subprocess
import sys

APP_DIR = os.path.join(os.path.expanduser("~"), ".deepskin20")
WALLPAPER_DIR = os.path.join(APP_DIR, "wallpapers")
CACHE_DIR = os.path.join(APP_DIR, "cache")
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(os.path.dirname(TOOLS_DIR), "assets")

IMAGE_FILES = ["01-village.jpg"]
IMAGE_NAMES = [
    "苗寨灯火(16:9 宽幅)",
]
# 单张样式: 素材 1104x630 与屏幕同形, grid = cover 铺满(几乎不裁切),
# single1 = 卡片单图(模糊填充 + 圆角卡片)。
# 想改成整张不裁切的完整卡片: 把 GRID_FIT 改成 True。
GRID_COLS = 1
GRID_ROWS = 1
GRID_SINGLE = True
# 可切换的壁纸模式
GRID_FIT = False  # False: grid=全屏铺满(cover; 本套素材同形几乎不裁切)
MODES = [
    ("grid", "全屏铺满(默认, cover)"),
    ("single1", "卡片单图(模糊填充)"),
]


def ensure_dirs():
    for d in (APP_DIR, WALLPAPER_DIR, CACHE_DIR):
        os.makedirs(d, exist_ok=True)


def prepare_console():
    """Windows GBK 控制台避免 Unicode 打印崩溃。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def ensure_pillow():
    """确保 Pillow 可用; 缺失时自动 pip 安装。"""
    try:
        import PIL  # noqa: F401
        return
    except ImportError:
        pass
    print("[deepskin] 未检测到 Pillow, 正在自动安装 ...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "pillow"])
    import PIL  # noqa: F401


def asset_path(idx):
    """idx: 1..4"""
    return os.path.join(ASSETS_DIR, IMAGE_FILES[idx - 1])


def screen_size():
    """返回主屏幕尺寸 (W, H), 失败时回退 1920x1080。"""
    env = os.environ.get("DEEPSKIN_SIZE", "").strip()
    if env:
        try:
            w, h = env.lower().split("x")
            return int(w), int(h)
        except ValueError:
            pass
    try:
        if platform.system() == "Windows":
            import ctypes
            user32 = ctypes.windll.user32
            return int(user32.GetSystemMetrics(0)), int(user32.GetSystemMetrics(1))
    except Exception:
        pass
    return 1920, 1080


# ---------------------------------------------------------------- 图像合成

def _gradient(size, top=(250, 252, 255), bottom=(232, 242, 253)):
    """极浅蓝白渐变背景。"""
    from PIL import Image
    w, h = size
    g = Image.new("RGB", (1, max(h, 2)))
    for y in range(h):
        t = y / max(h - 1, 1)
        g.putpixel((0, y), tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))
    return g.resize((w, h))


def _paste_card(base, src, cell, margin_ratio=0.045, radius_ratio=0.05, shadow=True):
    """把 src 按 contain 方式贴进 cell, 圆角 + 柔和阴影。"""
    from PIL import Image, ImageDraw, ImageFilter

    x0, y0, cw, ch = cell
    margin = max(6, int(min(cw, ch) * margin_ratio))
    tw, th = cw - 2 * margin, ch - 2 * margin
    scale = min(tw / src.width, th / src.height)
    nw, nh = max(1, int(src.width * scale)), max(1, int(src.height * scale))
    tile = src.resize((nw, nh), Image.LANCZOS)
    x, y = x0 + (cw - nw) // 2, y0 + (ch - nh) // 2
    radius = max(6, int(min(cw, ch) * radius_ratio))

    mask = Image.new("L", (nw, nh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, nw - 1, nh - 1], radius=radius, fill=255)

    if shadow:
        pad = max(10, radius)
        sh = Image.new("RGBA", (nw + 2 * pad, nh + 2 * pad), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle(
            [pad, pad, pad + nw - 1, pad + nh - 1], radius=radius, fill=(24, 55, 110, 64)
        )
        sh = sh.filter(ImageFilter.GaussianBlur(max(8, radius // 2)))
        base.alpha_composite(sh, (x - pad, y - pad))
    base.paste(tile, (x, y), mask)


def _avg_source_aspect():
    """素材平均宽高比, 让格子形状贴合图片(竖图配竖格)。"""
    ensure_pillow()
    from PIL import Image

    s, n = 0.0, 0
    for f in IMAGE_FILES:
        try:
            with Image.open(os.path.join(ASSETS_DIR, f)) as im:
                s += im.width / max(im.height, 1)
                n += 1
        except OSError:
            pass
    return (s / n) if n else 1.0


def compose_grid(size=(3840, 2160), cols=None, rows=None, cell_aspect=None):
    """紧贴式拼贴壁纸: 卡片细缝相挨、整块居中(支持 1×2 / 2×2 …)。
    cols/rows/cell_aspect 缺省取自 GRID_COLS/GRID_ROWS 与素材平均比例。
    缝隙/外边距比例可用环境变量 DEEPSKIN_GRID_GAP 调整(百分比, 默认 1.5)。"""
    ensure_pillow()
    from PIL import Image

    if cols is None:
        cols = GRID_COLS
    if rows is None:
        rows = GRID_ROWS
    if cell_aspect is None:
        cell_aspect = _avg_source_aspect()
    if len(IMAGE_FILES) > cols * rows:
        raise ValueError("素材数量超过网格容量")
    W, H = size
    try:
        gap_pct = float(os.environ.get("DEEPSKIN_GRID_GAP", "1.5"))
    except ValueError:
        gap_pct = 1.5
    m = min(W, H)
    pad = max(6, int(m * 0.015))  # 外圈边距
    gap = max(4, int(m * gap_pct / 100.0))  # 卡片之间细缝
    th = (H - 2 * pad - (rows - 1) * gap) // rows  # 格子高(按整块高度填满)
    tw = int(th * cell_aspect)  # 格子宽(按素材比例)
    avail_w = (W - 2 * pad - (cols - 1) * gap) // cols
    if tw > avail_w:
        tw = avail_w
        th = max(1, int(tw / cell_aspect))
    tw, th = max(tw, 64), max(th, 64)
    total_w = cols * tw + (cols - 1) * gap
    total_h = rows * th + (rows - 1) * gap
    x0 = (W - total_w) // 2
    y0 = (H - total_h) // 2

    base = _gradient(size).convert("RGBA")
    for i, f in enumerate(IMAGE_FILES):
        src = Image.open(os.path.join(ASSETS_DIR, f)).convert("RGB")
        r, c = divmod(i, cols)
        cell = (x0 + c * (tw + gap), y0 + r * (th + gap), tw, th)
        _paste_card(base, src, cell, margin_ratio=0.018, radius_ratio=0.03, shadow=False)
    return base.convert("RGB")


def compose_single(idx, size=(1920, 1080)):
    """单图壁纸: 模糊填充背景 + 居中圆角卡片。"""
    ensure_pillow()
    from PIL import Image, ImageFilter

    src = Image.open(asset_path(idx)).convert("RGB")
    w, h = size
    # 模糊填充背景
    s = 96
    small = src.resize((s, max(1, int(s * src.height / src.width))), Image.BOX)
    bg = small.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(32))
    base = bg.convert("RGBA")
    _paste_card(base, src, (0, 0, w, h), margin_ratio=0.035, radius_ratio=0.035)
    return base.convert("RGB")


def compose_cover(size=(1920, 1080)):
    """全屏单图: 素材按 cover 方式裁剪铺满整屏(16:9 插画几乎无裁切)。"""
    ensure_pillow()
    from PIL import Image

    src = Image.open(asset_path(1)).convert("RGB")
    W, H = size
    scale = max(W / src.width, H / src.height)
    nw, nh = int(round(src.width * scale)), int(round(src.height * scale))
    img = src.resize((nw, nh), Image.LANCZOS)
    x, y = (nw - W) // 2, (nh - H) // 2
    return img.crop((x, y, x + W, y + H))


def _fit_gradient(size, top=(248, 251, 255), bottom=(226, 238, 252)):
    """极浅蓝白竖向渐变背景。"""
    from PIL import Image
    w, h = size
    col = Image.new("RGB", (1, h))
    for y in range(h):
        k = y / max(h - 1, 1)
        col.putpixel((0, y), tuple(int(a + (b - a) * k) for a, b in zip(top, bottom)))
    return col.resize((w, h))


def compose_fit(size=(1920, 1080)):
    """整张完整显示(contain)+ 渐变底 + 圆角阴影。

    方形/竖版素材在 16:9 屏幕上 cover 会裁掉约 22% 的高度, 大字会被切;
    这个模式保证整张素材都在画面内。
    """
    ensure_pillow()
    from PIL import Image, ImageDraw, ImageFilter

    src = Image.open(asset_path(1)).convert("RGB")
    w, h = size
    base = _fit_gradient(size).convert("RGBA")

    margin = max(18, int(min(w, h) * 0.045))
    tw, th = w - 2 * margin, h - 2 * margin
    scale = min(tw / src.width, th / src.height)
    nw, nh = max(1, int(src.width * scale)), max(1, int(src.height * scale))
    tile = src.resize((nw, nh), Image.LANCZOS)
    x, y = (w - nw) // 2, (h - nh) // 2
    radius = max(10, int(min(nw, nh) * 0.035))

    mask = Image.new("L", (nw, nh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, nw - 1, nh - 1], radius=radius, fill=255)

    pad = max(12, radius)
    sh = Image.new("RGBA", (nw + 2 * pad, nh + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle(
        [pad, pad, pad + nw - 1, pad + nh - 1], radius=radius, fill=(24, 55, 110, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(max(8, radius // 2)))
    base.alpha_composite(sh, (x - pad, y - pad))
    base.paste(tile, (x, y), mask)
    return base.convert("RGB")


def compose(mode, size=None):
    """按模式名合成壁纸: mode ∈ {grid, single1..}。
    本套件 GRID_SINGLE=True: grid 默认走 cover 铺满(GRID_FIT=True 时改为完整卡片);
    single1 = 全屏 cover。"""
    size = tuple(size) if size else screen_size()
    if mode == "grid":
        if GRID_SINGLE:
            return compose_fit(size) if GRID_FIT else compose_cover(size)
        return compose_grid(size)
    if mode.startswith("single"):
        # 单张素材套件: single1 走全屏 cover(GRID_FIT 时与 grid 区分开)
        if GRID_SINGLE and GRID_FIT:
            return compose_cover(size)
        return compose_single(int(mode[6:]), size)
    raise ValueError("未知模式: %s" % mode)


def wallpaper_path(mode, size):
    return os.path.join(WALLPAPER_DIR, "%s-%dx%d.jpg" % (mode, size[0], size[1]))


def _source_freshness():
    """素材与核心脚本的最新修改时间, 用于判断输出是否过期(实现热更新)。"""
    paths = [os.path.join(ASSETS_DIR, f) for f in IMAGE_FILES] + [os.path.abspath(__file__)]
    mt = 0.0
    for p in paths:
        try:
            mt = max(mt, os.path.getmtime(p))
        except OSError:
            pass
    return mt


def build(mode, size=None, force=False):
    """合成并保存, 返回文件路径。素材/脚本更新后会自动重新生成(热更新)。"""
    ensure_dirs()
    size = tuple(size) if size else screen_size()
    out = wallpaper_path(mode, size)
    stale = (
        force
        or not os.path.exists(out)
        or os.path.getmtime(out) < _source_freshness()
    )
    if not stale:
        return out
    img = compose(mode, size)
    img.save(out, quality=92)
    return out


# ---------------------------------------------------------------- 系统壁纸

def set_wallpaper(path):
    """跨平台设置系统壁纸。"""
    path = os.path.abspath(path)
    system = platform.system()
    if system == "Windows":
        import ctypes
        import time
        # 留出一点写盘时间, 避免 Explorer 读到旧缓存导致"壁纸没变化"
        time.sleep(0.4)
        # SPI_SETDESKWALLPAPER=20, SPIF_UPDATEINIFILE|SPIF_SENDWININICHANGE=3
        ok = ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
        if not ok:
            raise RuntimeError("Windows 设置壁纸失败")
    elif system == "Darwin":
        subprocess.run(
            [
                "osascript", "-e",
                'tell application "System Events" to set picture of every desktop '
                'to POSIX file "%s"' % path,
            ],
            check=True,
        )
    else:
        import pathlib
        uri = pathlib.Path(path).as_uri()
        ok = True
        try:
            subprocess.run(
                ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri],
                check=False,
            )
        except Exception:
            ok = False
        try:
            subprocess.run(
                ["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", uri],
                check=False,
            )
        except Exception:
            pass
        if not ok:
            subprocess.run(["feh", "--bg-fill", path], check=False)
    print("[deepskin] 壁纸已设置: %s" % path)


if __name__ == "__main__":
    from PIL import Image  # noqa: F401  (仅为检查)
