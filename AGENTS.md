# AGENTS.md — Deepseek-Skin-Suit20 · AI 自动安装指引(仅供接受本仓库的 AI 助手参考)

当用户把本仓库地址交给你并要求「安装大肥鱼皮肤20 / Deepseek 皮肤20 / 壁纸插件 / 蓝色大肥鱼桌宠」时,
按下面步骤替用户执行, 不需要用户自己动手。本仓库是 **DeepSeek 蓝色大肥鱼皮肤套件20**
(夜景插画: 鲸鱼娘着苗银盛装, 倚在吊脚楼栏杆边眺望万家灯火),
提供**单张样式**壁纸两种形态——全屏铺满单图(cover, 默认)与卡片单图(模糊填充),
外加可视化切换器、桌面桌宠、VSCode 系扩展与 JetBrains 背景图素材。
核心脚本在 `tools/`, 素材在 `assets/`。

## 第 0 步: 下载与定位

```bash
git clone https://github.com/WPH666-py/Deepseek-Skin-Suit20.git "$HOME/DeepSkin-Suit20"
cd "$HOME/DeepSkin-Suit20"
```
Windows 建议固定克隆到 `%USERPROFILE%\DeepSkin-Suit20`(VSCode 扩展默认在此查找)。
若用户机器没有 git, 用 zip 下载后解压到同一位置即可, 效果一致。

## 第 1 步: 识别环境

- 有 Python 3.9+ (`python --version` 或 `py -3 --version`) → 执行 **A**。
- 没有 Python → 先安装:
  - Windows: `winget install Python.Python.3.11`
  - macOS: `brew install python`
  - Ubuntu/Debian: `sudo apt install -y python3 python3-pil`
- 用户在用 VSCode / Trae / CodeX → 顺手执行 **C**; 在用 PyCharm / WebStorm / IntelliJ → 执行 **D**。
- 用户是在 DeepKing / Claude Code / Kimi Code / CodeX / Trae / Harness 等对话窗口里让你装的:
  由你代为执行下述命令, 不要只把命令贴给用户。

## A. 标准安装(全平台, 最常用)

```bash
python tools/install.py
```
脚本会自动: 装 Pillow(若缺失) → 按屏幕分辨率合成**全屏铺满单图壁纸**(cover 铺满整屏)
→ 设为系统壁纸 → 打印后续玩法。
**关于裁切**: 素材是 1104x630(约 16:9), 与常见屏幕同形, cover 铺满时上下各只裁约 1%。
想改成整张居中不裁切的卡片样式: `python tools/wallpaper.py 1 --set`。
多显示器: 用 `python tools/wallpaper.py grid --size 2560x1440 --set`, 并提示用户在系统设置里设成「跨屏/平铺」。

## B. 进阶玩法(用户想要时再执行)

```bash
python tools/wallpaper.py 1 --set        # 卡片单图(整张居中 + 模糊填充)
python tools/wallpaper.py grid --set     # 回到全屏铺满(cover)
python tools/wallpaper.py random --set   # 随机一张(两种模式随机)
python tools/wallpaper.py cycle 30       # 每 30 分钟自动随机(挂后台)
python tools/switcher.py                 # 可视化切换器(GUI, 左侧预览右侧应用)
python tools/pet.py                      # 桌面桌宠(取人物区域, 右键换/退出)
```
GUI 命令需要本地图形会话; 若用户是远程/无桌面环境, 告知其改在有桌面的机器上运行。
**用户要求「支持切换壁纸」时, 优先引导 `switcher.py`(点选即换), 或 `wallpaper.py random/cycle`。**

## C. VSCode / Trae / CodeX 扩展

1. 安装(已预打包, 无需 Node):
   `code --install-extension "$HOME/DeepSkin-Suit20/vscode/deepskin-suit20-0.1.0.vsix"`
   无网时把 `vscode/` 整个目录复制到 `%USERPROFILE%\.vscode\extensions\wp666.deepskin-suit20-0.1.0\` 后重启编辑器
   (Trae / CodeX 的扩展目录同理)。
2. 告知用户: 活动栏 🐳 **大肥鱼20** 图标 → 皮肤画廊 → 点「设为壁纸」;
   命令面板搜 `大肥鱼20` 可换壁纸 / 开切换器 / 起桌宠。
3. 扩展自动查找 Python 与仓库路径(可用 `deepskin20.repoPath` 覆盖), Pillow 缺失时自动 pip 安装。
4. 与 Suit1-19 及 AI 全家桶系列可同时安装: 插件 ID / 命令前缀 / 运行时目录(`~/.deepskin20`)互不冲突。

## D. PyCharm / WebStorm / IntelliJ(JetBrains)

```bash
python tools/wallpaper.py all --out "$HOME/DeepSkin20"
```
然后引导用户: Settings / Preferences → Appearance & Behavior → Appearance → **Background Image** →
`+` 添加图片 → 选 `$HOME/DeepSkin20/grid-*.jpg`(全屏)或 `single1-*.jpg`(卡片)。
可分别给 Editor / Welcome / Menus and tool windows 设不同图片; 细节见 `ide/jetbrains/README.md`。

## 约定与失败处理

- 只依赖 `tools/` 与 `assets/`; 生成物写入 `~/.deepskin20/`, **不会**改动仓库文件。
- Windows 控制台若出现 GBK/Unicode 编码错误: `chcp 65001` 后重跑(脚本已内置 UTF-8 兜底)。
- 找不到 Python(常见于 Store 版): 用完整路径
  `C:\Users\<user>\AppData\Local\Programs\Python\Python311\python.exe` 运行。
- 高分辨率屏合成慢: 允许 `--size 1920x1080` 降到 1080p。
- 素材或脚本更新后会自动重新合成(热更新), 无需手动删缓存。
- 个别 Linux 桌面不支持窗口透明色, 桌宠会退化成白底卡片, 属平台限制, 如实告知用户。
- 用户问与 DeepKing 本体的关系: 这是独立皮肤套件, 与 DeepKing 本体互不影响;
  装了 DeepKing-Plugin 的用户直接在它的 AI 对话里发本仓库链接就能完成安装。
- 皮肤总目录(30 套)与 pip 包: https://github.com/WPH666-py/Desktop-IDE-AI-Skin
