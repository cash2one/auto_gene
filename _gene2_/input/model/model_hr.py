#encoding:utf8
import os
import sys
import hashlib
from datetime import datetime

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

sys.path.append (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controller.common_app_db import app

import etc
db_info = etc.db_info


#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@127.0.0.1/mydbname'
app.config['SQLALCHEMY_DATABASE_URI'] = '%s://%s:%s@%s:%s/%s' % (db_info['driver'], db_info['user'],  \
                                                                 db_info['pawd'], db_info['host'], \
                                                                 db_info['port'], db_info['name'])
app.config['SQLALCHEMY_ECHO'] = db_info['echo']
db = SQLAlchemy(app)

class Staff(db.Model):
    id       = db.Column(db.Integer, primary_key=True, info=u'*1-ID')
    username = db.Column(db.String(80), unique=True, info=u'2-用户名')
    password = db.Column(db.String(32), info=u'3-密码')
    name     = db.Column(db.String(100), info=u'4-姓名')
    posi_id  = db.Column(db.Integer, info=u'5-职位')
    stat_id  = db.Column(db.Integer, info=u'6-部门')
    join     = db.Column(db.Date, info=u'd7-入职日期')
    leave    = db.Column(db.Date, info=u'd8-离职日期')
    mobile   = db.Column(db.String(20), info=u'9-手机号码')
    email    = db.Column(db.String(100), info=u'10-邮箱')
    line_mg  = db.Column(db.Integer, info=u'11-直线上司')
    flag     = db.Column(db.Integer, info=u'b21-是否有效')
    remark   = db.Column(db.String(1024), info=u'22-备注')
    created  = db.Column(db.DateTime, default=datetime.now(), info=u'-23-创建时间')
    updated  = db.Column(db.DateTime, default=datetime.now(), info=u'-24-修改时间')
    
    _url  = '/admin/staff'
    _name = u'staff'
    _title= '员工'
    _dbop = 'db_Staff'
    
    
class Department(db.Model):
    id       = db.Column(db.Integer, primary_key=True, info=u'*1-ID')
    name     = db.Column(db.String(100), info=u'2-部门名称')
    flag     = db.Column(db.Integer, info=u'10-是否有效')
    remark   = db.Column(db.String(1024), info=u'11-备注')
    created  = db.Column(db.DateTime, default=datetime.now(), info=u'-12-创建时间')
    updated  = db.Column(db.DateTime, default=datetime.now(), info=u'-13-修改时间')
    
    _url  = '/admin/dept'
    _name = u'dept'
    _title= '部门'
    _dbop = 'db_Dept'
    
class Position(db.Model):
    id       = db.Column(db.Integer, primary_key=True, info=u'*1-ID')
    name     = db.Column(db.String(100), unique=True, info=u'2-职位名称')
    flag     = db.Column(db.Integer, info=u'10-是否有效')
    remark   = db.Column(db.String(1024), info=u'11-备注')
    created  = db.Column(db.DateTime, default=datetime.now(), info=u'-12-创建时间')
    updated  = db.Column(db.DateTime, default=datetime.now(), info=u'-13-修改时间')
    
    _url  = '/admin/position'
    _name = u'position'
    _title= '职位'
    _dbop = 'db_Position'

class Salary (db.Model):
    id       = db.Column(db.Integer, primary_key=True, info=u'*1-ID')
    staff    = db.Column(db.Integer, info=u'2-员工')
    level    = db.Column(db.Integer, info=u'5-等级')
    money    = db.Column(db.Integer, info=u'6-每月薪水')
    flag     = db.Column(db.Integer, info=u'10-是否有效')
    remark   = db.Column(db.String(1024), info=u'11-备注')
    created  = db.Column(db.DateTime, default=datetime.now(), info=u'-12-创建时间')
    updated  = db.Column(db.DateTime, default=datetime.now(), info=u'-13-修改时间')
    
    _url  = '/admin/salary'
    _name = u'salary'
    _title= '薪酬'
    _dbop = 'db_Salary'
    
    