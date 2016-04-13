#coding=UTF-8

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///GaoQiFaceSign.db', echo = False)
db_session = scoped_session(sessionmaker(autocommit = False, autoflush = False, bind = engine))

Base = declarative_base()
Base.query = db_session.query_property()

def column_dict(self):
    model_dict = dict(self.__dict__)
    del model_dict['_sa_instance_state']
    return model_dict
Base.column_dict = column_dict

def init_db():
    # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在
    # 元数据上。否则你就必须在调用 init_db() 之前导入它们。
    import model
    Base.metadata.create_all(bind=engine)