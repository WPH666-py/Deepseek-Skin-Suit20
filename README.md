# 🐳 DeepSeek 蓝色大肥鱼 · 皮肤套件20 (Deepseek-Skin-Suit20)

DeepSeek 蓝色大肥鱼(鲸鱼娘)主题皮肤第二十弹: **单张样式**——一张夜景宽幅插画,
提供 **全屏铺满单图**(cover, 默认)与 **卡片单图**(模糊填充 + 圆角卡片)两种壁纸形态,
外加可视化切换器、桌面桌宠与多 IDE 皮肤。
画面: 鲸鱼娘着苗银盛装, 倚在吊脚楼栏杆边, 眺望山下万家灯火与夜色群山。
素材内置、离线可用; 跨平台 Windows / macOS / Linux。

![全屏单图预览](docs/single-preview.png)

## ✨ 功能

| 功能 | 说明 |
|---|---|
| 全屏铺满单图 | 素材按 cover 铺满整屏(默认; 1104x630 与屏幕同形, 几乎不裁切) |
| 卡片单图 | 整张素材居中 + 圆角卡片 + 模糊填充背景 |
| 可视化切换器 | `tools/switcher.py`: 左侧实时预览, 右侧点「应用到桌面」, 可开自动随机 |
| 命令行换壁纸 | `tools/wallpaper.py`: grid / 1 / random / all / cycle |
| 桌面桌宠 | `tools/pet.py`: 取人物区域, 透明置顶可拖动, 右键换/退出 |
| VSCode 系扩展 | 活动栏 🐳 图标 → 皮肤画廊, 卡片点选即换壁纸 |
| JetBrains 素材 | 生成全屏铺满图与卡片图, 供 PyCharm/WebStorm 背景图导入 |

> 素材是 1104x630(约 16:9), 与常见屏幕同形, 默认的「全屏铺满」上下各只裁约 1%;
> 想让整张原封不动显示, 用「卡片单图」。

## 🚀 一键安装

把本仓库地址交给任意 AI(DeepKing / Claude Code / Kimi Code / CodeX / Trae / Harness / Cursor …),
说一句「安装这个皮肤」即可, AI 会读 `AGENTS.md` 自动完成。手动安装:

```bash
git clone https://github.com/WPH666-py/Deepseek-Skin-Suit20.git "$HOME/DeepSkin-Suit20"
cd "$HOME/DeepSkin-Suit20"
python tools/install.py          # 装 Pillow → 生成全屏铺满 → 设为系统壁纸
```

## 🎛 切换壁纸

```bash
python tools/switcher.py                 # 图形切换器(推荐)
python tools/wallpaper.py 1 --set        # 卡片单图(模糊填充)
python tools/wallpaper.py grid --set     # 回到全屏铺满(cover)
python tools/wallpaper.py random --set   # 随机一张
python tools/wallpaper.py cycle 30       # 每 30 分钟自动随机
python tools/wallpaper.py all --out ~/DeepSkin20   # 导出全部(给 PyCharm 等用)
```

## 🐋 桌面桌宠

```bash
python tools/pet.py     # 透明置顶小鲸鱼; 左键拖动, 右键菜单, Esc 退出
```

## 🧩 IDE 集成

- **VSCode / Trae / CodeX**: `code --install-extension vscode/deepskin-suit20-0.1.0.vsix`
  → 活动栏 🐳「大肥鱼20」→ 皮肤画廊 → 「设为壁纸」。无网时把 `vscode/` 复制到
  `%USERPROFILE%\.vscode\extensions\wp666.deepskin-suit20-0.1.0\` 并重启。
- **PyCharm / WebStorm / IntelliJ**: `python tools/wallpaper.py all --out ~/DeepSkin20`,
  再在 Settings → Appearance → Background Image 里选图, 详见 `ide/jetbrains/README.md`。
- **DeepKing 本体**: 本仓库是独立皮肤套件, 与 DeepKing 本体互不影响;
  在 DeepKing 的 AI 对话里发本仓库链接即可自动安装。

## 📦 皮肤总目录 / pip 包

- 皮肤大全(30 套, 含 AI 全家桶系列): https://github.com/WPH666-py/Desktop-IDE-AI-Skin
- pip 包: `pip install deepskins` → `deepskins list` / `deepskins install deepseek-20`

## 📁 目录结构

```
assets/           1 张夜景宽幅插画(01-village.jpg, 1104x630)
tools/            install.py 一键安装 · wallpaper.py 命令行 · switcher.py 切换器 · pet.py 桌宠
vscode/           预打包 VSCode/Trae/CodeX 扩展(deepskin-suit20-0.1.0.vsix)
ide/jetbrains/    PyCharm 等背景图导入说明
docs/             预览图(由 tools/make_previews.py 生成)
```

## ⚠️ 说明

- 生成物写入 `~/.deepskin20/`(壁纸与缓存), 不改动仓库内容; 素材更新后自动重新合成。
- Windows 控制台若报 GBK 编码错误: `chcp 65001` 后重跑。
- 素材为 AI 生成的表情梗图, 仅供个人桌面娱乐使用; 请勿用于商业用途。
- License: MIT

---

其他套件: [皮肤大全](https://github.com/WPH666-py/Desktop-IDE-AI-Skin) ·
[DeepKing-Plugin](https://github.com/WPH666-py/DeepKing-Plugin)
