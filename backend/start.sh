#!/bin/bash

# 设置字符编码
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

echo ""
echo "========================================"
echo "  狼火石器立志 - 后端服务启动器"
echo "========================================"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python 3.7+"
    echo "💡 Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "💡 CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "💡 macOS: brew install python3"
    exit 1
fi

echo "✅ Python3已安装"

# 检查是否在正确的目录
if [ ! -f "app.py" ]; then
    echo "❌ 请在backend目录下运行此脚本"
    echo "💡 当前目录: $(pwd)"
    exit 1
fi

echo "✅ 当前目录正确"

# 检查虚拟环境
if [ -f "venv/bin/activate" ]; then
    echo "🔧 激活虚拟环境..."
    source venv/bin/activate
    echo "✅ 虚拟环境已激活"
else
    echo "⚠️  未找到虚拟环境，使用系统Python"
fi

# 检查依赖
echo ""
echo "🔍 检查Python依赖..."
python3 -c "import flask, flask_cors, sqlalchemy, pymysql" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 缺少必要的Python依赖"
    echo "💡 正在安装依赖..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
    echo "✅ 依赖安装完成"
else
    echo "✅ 依赖检查通过"
fi

# 检查MySQL服务
echo ""
echo "🔍 检查MySQL服务..."
if command -v systemctl &> /dev/null; then
    # Linux系统
    if systemctl is-active --quiet mysql; then
        echo "✅ MySQL服务正在运行"
    else
        echo "⚠️  MySQL服务未运行，尝试启动..."
        sudo systemctl start mysql
        if [ $? -eq 0 ]; then
            echo "✅ MySQL服务启动成功"
        else
            echo "❌ MySQL服务启动失败"
            echo "💡 请手动启动: sudo systemctl start mysql"
        fi
    fi
elif command -v brew &> /dev/null; then
    # macOS系统
    if brew services list | grep -q "mysql.*started"; then
        echo "✅ MySQL服务正在运行"
    else
        echo "⚠️  MySQL服务未运行，尝试启动..."
        brew services start mysql
        if [ $? -eq 0 ]; then
            echo "✅ MySQL服务启动成功"
        else
            echo "❌ MySQL服务启动失败"
            echo "💡 请手动启动: brew services start mysql"
        fi
    fi
else
    echo "⚠️  无法检测MySQL服务状态，请确保MySQL已启动"
fi

# 启动应用
echo ""
echo "🚀 启动应用..."
echo "========================================"
python3 start_with_mysql.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 应用启动失败"
    echo "💡 请检查错误信息并解决问题"
    exit 1
fi

echo ""
echo "👋 应用已停止" 