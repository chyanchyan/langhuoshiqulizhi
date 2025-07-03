# 初始化数据库
# 使用 mysql sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime
from flask import current_app
from werkzeug.utils import secure_filename
from backend.models import Base
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class DbManager:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """初始化数据库连接"""
        # 从环境变量或配置文件获取数据库配置
        self.db_url = self._get_database_url()
        
        # 创建引擎，包含连接池配置
        self.engine = create_engine(
            self.db_url,
            pool_size=int(os.getenv('DB_POOL_SIZE', 10)),
            max_overflow=int(os.getenv('DB_MAX_OVERFLOW', 20)),
            pool_timeout=int(os.getenv('DB_POOL_TIMEOUT', 30)),
            pool_recycle=int(os.getenv('DB_POOL_RECYCLE', 3600)),
            echo=os.getenv('DB_ECHO', 'false').lower() == 'true'
        )
        
        # 创建会话工厂
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)
    
    def _get_database_url(self):
        """获取数据库连接URL"""
        # 优先使用环境变量
        if os.getenv('DATABASE_URL'):
            return os.getenv('DATABASE_URL')
        
        # 从环境变量构建
        host = os.getenv('DATABASE_HOST', 'localhost')
        port = os.getenv('DATABASE_PORT', '3306')
        database = os.getenv('DATABASE_NAME', 'langhuo_db')
        username = os.getenv('DATABASE_USER', 'root')
        password = os.getenv('DATABASE_PASSWORD', '123456')
        charset = os.getenv('DATABASE_CHARSET', 'utf8mb4')
        
        return f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset={charset}"

    def init_db(self):
        """初始化数据库表"""
        Base.metadata.create_all(self.engine)
        print("数据库表初始化完成")

    def get_session(self):
        """获取数据库会话"""
        return self.Session()

    def close_session(self):
        """关闭数据库会话"""
        self.Session.remove()

    def get_conn(self):
        """获取数据库连接"""
        return self.engine.connect()
    
    def test_connection(self):
        """测试数据库连接"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute("SELECT 1")
                return True
        except Exception as e:
            print(f"数据库连接测试失败: {e}")
            return False
    
    


