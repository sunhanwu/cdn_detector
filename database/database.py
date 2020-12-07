"""
Author: sunhanwu
Date: 2020-12-07
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship, backref, sessionmaker
from config import db_config

Base = declarative_base()

class CNAME(Base):
    """
    对应CNAME表结构
    """
    __tablename__ = 'CNAME'
    # id，主键，自增
    id = Column(Integer, autoincrement=True, primary_key=True)
    # dns 域名1，限制长度在65个字符之内
    dns1 = Column(String(65))
    # dns 域名2, 限制长度在65个字符内
    dns2 = Column(String(65))
    # 查询的递归服务器位置
    area = Column(Enum(""))
    # 插入数据的时间
    date = Column(Date)

class A(Base):
    """
    对应A表结构
    """
    __tablename__ = 'A'
    # id，主键，自增
    id = Column(Integer, autoincrement=True, primary_key=True)
    # dns 域名，限制长度在65个字符之内
    dns = Column(String(65))
    # 具体的ip
    ip = Column(String(20))
    # 查询的递归服务器位置
    area = Column(Enum(""))
    # ip前24位的值
    ip_24 = Column(String(20))
    # dns 递归链深度
    depth = Column(Integer)
    # 插入数据的时间
    date = Column(Date)

engine = create_engine('mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8'.format( db_config['user'], db_config['password'], db_config['host'], db_config['port'], db_config['database']))
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)


