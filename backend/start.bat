@echo off
chcp 65001 >nul
title 狼火石器立志 - 后端服务启动器

echo.
echo ========================================
echo   狼火石器立志 - 后端服务启动器
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.7+
    echo 💡 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python已安装

:: 检查是否在正确的目录
if not exist "app.py" (
    echo ❌ 请在backend目录下运行此脚本
    echo 💡 当前目录: %CD%
    pause
    exit /b 1
)

echo ✅ 当前目录正确

:: 检查虚拟环境
if exist "venv\Scripts\activate.bat" (
    echo 🔧 激活虚拟环境...
    call venv\Scripts\activate.bat
    echo ✅ 虚拟环境已激活
) else (
    echo ⚠️  未找到虚拟环境，使用系统Python
)

:: 检查依赖
echo.
echo 🔍 检查Python依赖...
python -c "import flask, flask_cors, sqlalchemy, pymysql" >nul 2>&1
if errorlevel 1 (
    echo ❌ 缺少必要的Python依赖
    echo 💡 正在安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
    echo ✅ 依赖安装完成
) else (
    echo ✅ 依赖检查通过
)

:: 启动应用
echo.
echo 🚀 启动应用...
echo ========================================
python start_with_mysql.py

if errorlevel 1 (
    echo.
    echo ❌ 应用启动失败
    echo 💡 请检查错误信息并解决问题
    pause
    exit /b 1
)

echo.
echo 👋 应用已停止
pause 