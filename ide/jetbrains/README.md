# JetBrains(PyCharm / WebStorm / IntelliJ)背景图

JetBrains 系 IDE 自带背景图功能, 本套件生成图片后手动导入即可。

## 1. 生成图片

```bash
python tools/wallpaper.py all --out "$HOME/DeepSkin20"
```

会得到 2 张图:

```
grid-<宽>x<高>.jpg       全屏铺满单图(cover, 默认)
single1-<宽>x<高>.jpg    卡片单图(整张居中 + 模糊填充)
```

想指定尺寸加 `--size 2560x1440`。

## 2. 导入

`Settings / Preferences` → `Appearance & Behavior` → `Appearance` → **Background Image** →
`+` 选择上一步的图片 → `Opacity` 建议 8%–20% → `OK`。

同一对话框里可以分别给 `Editor and tools` / `Welcome screen` / `Menus and tool windows`
设置不同图片: 例如欢迎页用全屏图, 编辑器用卡片图。

## 3. 推荐搭配

- 编辑器: `single1-*.jpg`(整张居中, 背景不抢注意力), 不透明度 10% 左右。
- 欢迎页: `grid-*.jpg`(铺满), 不透明度可到 40%。
