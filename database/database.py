from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class CNAME(Base):
    """
    对应CNAME表结构
    """
    __tablename__ = 'CNAME'
    # CNAME 记录id
    id = Column(Integer, autoincrement=True, primary_key=True)
    dns = Column(String(65))
    ip = Column(String(20))
    area = Column(Enum(""))