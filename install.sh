#!/usr/bin/env bash
set -e
echo "============================================"
echo "  DeepSeek 蓝色大肥鱼 · 皮肤套件20 安装"
echo "============================================"
if command -v python3 >/dev/null 2>&1; then PY=python3; else PY=python; fi
"$PY" "$(dirname "$0")/tools/install.py"
