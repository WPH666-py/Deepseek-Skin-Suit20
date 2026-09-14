@echo off
chcp 65001 >nul
echo ============================================
echo   DeepSeek 蓝色大肥鱼 · 皮肤套件20 安装
echo ============================================
where python >nul 2>nul
if errorlevel 1 (
  echo [x] 未找到 python, 请先安装 Python 3.9+:  winget install Python.Python.3.11
  pause
  exit /b 1
)
python "%~dp0tools\install.py"
pause
