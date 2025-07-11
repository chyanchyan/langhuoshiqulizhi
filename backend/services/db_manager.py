# 初始化数据库
# 使用 mysql sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, text   
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime
from flask import current_app
from werkzeug.utils import secure_filename
from models import Base
import os
import logging
from dotenv import load_dotenv
from .mysql_service import MySQLServiceManager

# 加载环境变量
load_dotenv()

# 配置日志
logger = logging.getLogger(__name__)

class DbManager:
    def __init__(self, app=None):
        self.mysql_manager = MySQLServiceManager()
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """初始化数据库连接"""
        # 从环境变量或配置文件获取数据库配置
        self.db_url = self._get_database_url()
        self.db_url_without_db = self._get_database_url(with_db=False)
        
        # 创建引擎，包含连接池配置
        self.engine = create_engine(
            self.db_url,
            pool_size=int(os.getenv('DB_POOL_SIZE', 10)),
            max_overflow=int(os.getenv('DB_MAX_OVERFLOW', 20)),
            pool_timeout=int(os.getenv('DB_POOL_TIMEOUT', 30)),
            pool_recycle=int(os.getenv('DB_POOL_RECYCLE', 3600)),
            echo=os.getenv('DB_ECHO', 'false').lower() == 'true'
        )
        self.engine_without_db = create_engine(
            self.db_url_without_db,
            pool_size=int(os.getenv('DB_POOL_SIZE', 10)),
            max_overflow=int(os.getenv('DB_MAX_OVERFLOW', 20)),
            pool_timeout=int(os.getenv('DB_POOL_TIMEOUT', 30)),
            pool_recycle=int(os.getenv('DB_POOL_RECYCLE', 3600)),
            echo=os.getenv('DB_ECHO', 'false').lower() == 'true'
        )
        
        # 创建会话工厂
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)
    
    def _get_database_url(self, with_db=True):
        """获取数据库连接URL"""
        # 优先使用环境变量
        if os.getenv('DATABASE_URL'):
            return os.getenv('DATABASE_URL')
        
        # 从环境变量构建
        host = os.getenv('DB_HOST', 'localhost')
        port = os.getenv('DB_PORT', '3306')
        username = os.getenv('DB_USERNAME', 'root')
        password = os.getenv('DB_PASSWORD', '123456')
        charset = os.getenv('DB_CHARSET', 'utf8mb4')

        database = os.getenv('DB_SCHEMA', 'langhuo_db')

        if with_db:
            return f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset={charset}"
        else:
            return f"mysql+pymysql://{username}:{password}@{host}:{port}?charset={charset}"

    def init_db(self):
        """初始化数据库表"""
        try:
            # 获取数据库名称
            database = os.getenv('DATABASE_NAME', 'langhuo_db')
            
            # 创建数据库
            with self.engine_without_db.connect() as conn:
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {database}"))
                conn.commit()

            # 创建表
            Base.metadata.create_all(self.engine)
            print("数据库表初始化完成")
        except Exception as e:
            logger.error(f"初始化数据库失败: {e}")
            raise

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
                result = conn.execute(text("SELECT 1"))
                return True, None
        except Exception as e:
            logger.error(f"数据库连接测试失败: {e}")
            return False, e

    def ensure_mysql_service_running(self) -> bool:
        """确保MySQL服务正在运行"""
        logger.info("检查MySQL服务状态...") 
        
        # 检查MySQL服务是否正在运行
        if self.mysql_manager.check_mysql_service():
            logger.info("MySQL服务正在运行")
            return True
        
        logger.warning("MySQL服务未运行，尝试启动...")
        
        # 尝试启动MySQL服务
        success, message = self.mysql_manager.start_mysql_service()
        if success:
            logger.info(f"MySQL服务启动成功: {message}")
            
            # 等待服务就绪
            if self.mysql_manager.wait_for_mysql_ready(timeout=60):
                logger.info("MySQL服务已就绪")
                return True
            else:
                logger.error("MySQL服务启动超时")
                return False
        else:
            logger.error(f"MySQL服务启动失败: {message}")
            return False
    
    def check_and_start_mysql(self) -> bool:
        """检查并启动MySQL服务（如果未运行）"""
        
        # 首先尝试直接连接数据库
        success, message = self.test_connection()
        if success:
            logger.info("数据库连接正常")
            return True

        if '2003' in str(message):
            logger.info(f"MySQL服务未运行: {message}")
            logger.info(f"尝试启动MySQL服务...")
            success, message = self.ensure_mysql_service_running()
            if success:
                logger.info(f"MySQL服务启动成功: {message}")
                return self.check_and_start_mysql()
            else:
                logger.error(f"MySQL服务启动失败: {message}")
                return False
        
        if '1049' in str(message):
            logger.info("数据库不存在，创建数据库")
            self.init_db()
            return self.check_and_start_mysql()
        
