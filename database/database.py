"""
Author: sunhanwu
Date: 2020-12-07
"""
# sys.path.append('../')
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import sessionmaker
import datetime
from utils.config import db_config

Base = declarative_base()

class CNAME(Base):
    """
    对应CNAME表结构
    """
    __tablename__ = 'CNAME'
    # dns 域名1，限制长度在65个字符之内, 主键1
    dns1 = Column(String(65), primary_key=True)
    # dns 域名2, 限制长度在65个字符内, 主键2
    dns2 = Column(String(65), primary_key=True)
    # 查询的递归服务器位置
    # area = Column(Enum("GD", "BJ"), default='BJ')   # 修改为字符串，记录查询的递归服务器IP
    area = Column(String(15))   # TODO 修改为字符串，记录查询的递归服务器IP
    # 插入数据的时间
    date = Column(DateTime, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # 插入标志
    flag = Column(Enum("0", "1", "2"), default="0")

    def __repr__(self):
        return '<%s %s %s %s %s>' % (self.dns1, self.dns2,self.area,self.date,self.flag)


class A(Base):
    """
    对应A表结构
    """
    __tablename__ = 'A'
    # dns 域名，限制长度在65个字符之内, 主键1
    dns = Column(String(65), primary_key=True)
    # 具体的ip, 主键2
    ip = Column(String(20), primary_key=True)
    # 查询的递归服务器位置
    # area = Column(Enum("BJ"), default="BJ")     # 同上，改为IP地址
    area = Column(String(15))     # 同上，改为IP地址
    # ip前24位的值
    # ip_24 = Column(String(20))
    # dns 递归链深度
    depth = Column(Integer)
    # 插入数据的时间
    date = Column(DateTime, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # 插入标志
    flag = Column(Enum("0", "1", "2"), default="0")

    def __repr__(self):
        return '<%s %s %s %s %s %s>' % (self.dns, self.ip, self.area, self.depth, self.date, self.flag)

engine = create_engine('mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8'.format( db_config['user'], db_config['password'], db_config['host'], db_config['port'], db_config['database']))
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


