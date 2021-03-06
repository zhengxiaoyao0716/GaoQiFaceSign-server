#coding=UTF-8

from flask import Flask, request, jsonify, session, g, url_for

app = Flask(__name__)
app.secret_key = 'This is a secret key for GaoQiFaceSign, make in 2016/4/13'
app.debug = True


####################操作数据####################
#请求结束时或者应用关闭时删除数据库会话
from database import db_session

@app.teardown_appcontext
def shutdown_session(response_or_exc):
    try: 
        if response_or_exc is None:
            db_session.commit()
    finally:
        db_session.remove()
    return response_or_exc
    
    
####################工具方法####################
def pack_resp(success, content = None, message = None):
    return jsonify({'success': success, 'content': content, 'message': message})
    
    
####################Api模块####################
from model import *

#密匙验证
#@params ak accessKeyId
#@params authStringPrefix authStringPrefix
import hmac, hashlib
@app.route('/FaceSign/auth', methods = ['POST'])
def auth():
	sk = Key.query.filter(Key.ak == request.json['ak']).first().sk
	if sk:
		signingKey = hmac.new(sk.__str__(), request.json['authStringPrefix'], hashlib.sha256).hexdigest().__str__()
		return pack_resp(True, {'signingKey': signingKey})
	else:
		return pack_resp(False, None, 'Unexpected accessKeyId.')
        
#教师登录
@app.route('/FaceSign/login', methods = ['POST'])
def login():
    account = request.json['account']
    teacher = Teacher.query.filter(Teacher.no == account).first()
    if teacher:
        if teacher.verify_password(request.json['password']):
            session['teacher'] = teacher.id
            return pack_resp(True, {'no': teacher.no, 'name': teacher.name, 
                'courses': teacher.course_list()
            })
        return pack_resp(False, None, 'Miss password.')
    else:
        return pack_resp(False, None, 'No such teacher.')
        
#修改密码
@app.route('/FaceSign/change_pwd', methods = ['POST'])
def change_pwd():
    if not 'teacher' in session:
        return pack_resp(False, url_for('.login'), 'Please login before.')
    teacher = Teacher.query.get(session['teacher'])
    if not teacher:
        return pack_resp(False, url_for('.login'), 'Invalid session.')
    if not teacher.verify_password(request.json['old_pwd']):
        return pack_resp(False, None, 'Old password error.')
    teacher.set_password(request.json['new_pwd'])
    return pack_resp(True, 'Your password has already changed.')
    
        
#查询签到
@app.route('/FaceSign/records/<int:course>/<int:begin>')
def records(course, begin):
    if not 'teacher' in session:
        return pack_resp(False, url_for('.login'), 'Please login before.')
    teacher = Teacher.query.get(session['teacher'])
    if not teacher:
        return pack_resp(False, url_for('.login'), 'Invalid session.')
    course = Course.query.get(course)
    signs = []
    unsigns = []
    for classes in course.class_list():
        for student in classes.students:
            if student.sign_time > begin:
                signs.append(student.column_dict())
            else:
                unsigns.append(student.column_dict())
    return pack_resp(True, {'signs': signs, 'unsigns': unsigns})
    
#学生签到
@app.route('/FaceSign/sign', methods = ['POST'])
def sign():
    if Student.sign(request.json['no']):
        return pack_resp(True)
    else:
        return pack_resp(False, None, 'No such student.')
        
        
####################测试服务####################
if __name__ == '__main__':
	app.run(debug = True)