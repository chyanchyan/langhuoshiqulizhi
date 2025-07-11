#!/usr/bin/env python3
"""
带MySQL服务检查的启动脚本
自动检查并启动MySQL服务，然后启动Flask应用
"""

import sys
import os
import time
import subprocess
from pathlib import Path

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def check_python_dependencies():
    """检查Python依赖是否已安装"""
    required_packages = [
        'flask', 'flask_cors', 'sqlalchemy', 'pymysql', 
        'python_dotenv', 'werkzeug'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ 缺少以下Python依赖包:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 请运行以下命令安装依赖:")
        print(f"   pip install -r {current_dir}/requirements.txt")
        return False
    
    print("✅ Python依赖检查通过")
    return True

def check_env_file():
    """检查环境变量文件是否存在"""
    env_file = current_dir / '.env'
    if not env_file.exists():
        print("⚠️  未找到.env文件，将使用默认配置")
        print("💡 建议创建.env文件并配置数据库连接信息")
        return False
    
    print("✅ 找到.env配置文件")
    return True

def main():
    """主函数"""
    print("🚀 启动系统检查...")
    print("=" * 50)
    
    # 检查Python依赖
    if not check_python_dependencies():
        return 1
    
    # 检查环境文件
    check_env_file()
    
    print("\n🔍 检查MySQL服务...")
    
    try:
        # 导入MySQL服务管理器
        from services.mysql_service import MySQLServiceManager
        from services.db_manager import DbManager
        
        # 创建服务管理器
        mysql_manager = MySQLServiceManager()
        
        # 检查MySQL服务状态
        if not mysql_manager.check_mysql_service():
            print("🔴 MySQL服务未运行，尝试启动...")
            success, message = mysql_manager.start_mysql_service()
            if success:
                print(f"✅ {message}")
                # 等待服务就绪
                if mysql_manager.wait_for_mysql_ready(timeout=60):
                    print("✅ MySQL服务已就绪")
                else:
                    print("❌ MySQL服务启动超时")
                    return 1
            else:
                print(f"❌ MySQL服务启动失败: {message}")
                print("\n💡 请手动启动MySQL服务:")
                if mysql_manager.is_windows:
                    print("   1. 以管理员身份打开命令提示符")
                    print("   2. 运行: net start MySQL80")
                elif mysql_manager.is_linux:
                    print("   1. 运行: sudo systemctl start mysql")
                elif mysql_manager.is_macos:
                    print("   1. 运行: brew services start mysql")
                return 1
        else:
            print("✅ MySQL服务正在运行")
        
        print("\n📦 初始化数据库...")
        
        # 创建Flask应用实例（仅用于数据库初始化）
        from flask import Flask
        app = Flask(__name__)
        
        # 初始化数据库管理器
        db_manager = DbManager(app)
        
        # 检查数据库连接
        if not db_manager.test_connection():
            print("❌ 数据库连接失败")
            print("💡 请检查:")
            print("   1. MySQL服务是否正常运行")
            print("   2. 数据库配置是否正确")
            print("   3. 数据库用户权限是否足够")
            return 1
        
        print("✅ 数据库连接正常")
        
        # 初始化数据库表
        db_manager.init_db()
        print("✅ 数据库初始化完成")
        
    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        print("💡 请确保所有依赖已正确安装")
        return 1
    except Exception as e:
        print(f"❌ 系统检查失败: {e}")
        return 1
    
    print("\n🚀 启动Flask应用...")
    print("=" * 50)
    
    # 启动Flask应用
    try:
        from app import app
        app.run(
            host=os.getenv('HOST', '0.0.0.0'),
            port=int(os.getenv('PORT', 5000)),
            debug=os.getenv('DEBUG', 'True').lower() == 'true'
        )
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
        return 0
    except Exception as e:
        print(f"❌ 应用启动失败: {e}")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code) 