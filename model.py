#coding=UTF-8

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

#############################基本表#############################
from passlib.apps import custom_app_context as pwd_context

#百度aksk
class Key(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    ak = Column(String(50), unique = True)
    sk = Column(String(50), unique = True)
    
    def __init__(self, ak, sk):
        self.ak = ak
        self.sk = sk
        
    def __repr__(self):
        return '<id: %r| ak: %r>'%(self.id, self.ak)
        
        
#教师
class Teacher(Base):
    __tablename__ = 'teacher'
    
    id = Column(Integer, primary_key = True)
    no = Column(String(20), unique = True)  #教师编号
    name = Column(String(50))
    password = Column(String(200))          #教师登录密码
    
    courses = relationship('Course')
    
    def __init__(self, no, name, password):
        self.no = no
        self.name = name
        self.password = pwd_context.encrypt(password)
        
    def __repr__(self):
        return '<No.%r| name: %r>'%(self.no, self.name)
        
    #验证密码
    def verify_password(self, password):
        return pwd_context.verify(password, self.password)
        
    #课程列表
    def course_list(self):
        result = []
        for course in self.courses:
            result.append(course.column_dict())
        return result
        
#课程
class Course(Base):
    __tablename__ = 'course'
    
    id = Column(Integer, primary_key = True)
    no = Column(String(20), unique = True)  #课程编号
    name = Column(String(50))
    classes_no_list = Column(String(200))   #班级编号列表
    
    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    
    def __init__(self, no, name, *classes_no_list):
        self.no = no
        self.name = name
        
        
    def __repr__(self):
        return '<No.%r| name: %r>'%(self.no, self.name)
        
    def class_list(self):
        result = []
        for classes_no in self.classes_no_list.split(' '):
            classes = Classes.query.filter(Classes.no == classes_no).first()
            result.append(classes)
        return result
        
        
#班级
class Classes(Base):
    __tablename__ = 'classes'
    
    id = Column(Integer, primary_key = True)
    no = Column(String(20), unique = True)  #班级编号
    name = Column(String(50), unique = True)
    
    students = relationship('Student')
    
    def __init__(self, no, name):
        self.no = no
        self.name = name
        
    def __repr__(self):
        return '<No.%r| name: %r>'%(self.no, self.name)
        
#学生
import time
class Student(Base):
    __tablename__ = 'student'
    
    id = Column(Integer, primary_key = True)
    no = Column(String(20), unique = True)  #学生编号
    name = Column(String(50))
    classes = Column(String(50))
    
    classes_id = Column(Integer, ForeignKey('classes.id'))
    
    sign_time = Column(Integer)             #签到时间
    
    def __init__(self, id, name, classes_id):
        self.id = id
        self.name = name
        self.classes_id = classes_id
        self.classes = Classes.query.get(classes_id).name
        
    def __repr__(self):
        return '<No.%r| name: %r>'%(self.no, self.name)
        
    @classmethod
    def sign(cls, no):
        student = Student.query.filter(Student.no == no).first()
        if student:
            student.sign_time = int(time.time())
            return True
        return False