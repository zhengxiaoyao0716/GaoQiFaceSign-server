#coding=UTF-8

import os
def init_test_data():
    if os.path.exists('GaoQiFaceSign.db'):
        os.remove('GaoQiFaceSign.db')
    from database import init_db
    init_db()
    from database import db_session
    from model import *
    db_session.add(Key('', ''))
    db_session.commit()
init_test_data()