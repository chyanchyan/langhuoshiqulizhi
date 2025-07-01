# 初始化数据库
# 使用 mysql sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from flask import current_app
from werkzeug.utils import secure_filename
from backend.models import Base




class DbManager:

    def __init__(self):
        self.db_url = current_app.config['SQLALCHEMY_DATABASE_URI']
        self.engine = create_engine(self.db_url)


    def init_db(self):
        Base.metadata.create_all(self.engine)
        

    def get_conn(self):
        return self.engine.connect()
    
    


