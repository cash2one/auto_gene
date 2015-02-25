#encoding:utf8
import os
import sys
import hashlib
from datetime import datetime

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

sys.path.append (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from controller.common_import import app
except:
    app = Flask(__name__)

import etc
db_info = etc.db_info


#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@127.0.0.1/mydbname'
app.config['SQLALCHEMY_DATABASE_URI'] = '%s://%s:%s@%s:%s/%s' % (db_info['driver'], db_info['user'],  \
                                                                 db_info['pawd'], db_info['host'], \
                                                                 db_info['port'], db_info['name'])
app.config['SQLALCHEMY_ECHO'] = db_info['echo']
db = SQLAlchemy(app)


class User(db.Model):
    # 用户
    id       = db.Column(db.Integer, primary_key=True, info=u'*1-ID')
    username = db.Column(db.String(80), unique=True, info=u'2-用户名')
    password = db.Column(db.String(32), info=u'3-密码')
    name     = db.Column(db.String(100), info=u'4-姓名')
    role     = db.Column(db.Integer, info=u'5-权限')
    flag     = db.Column(db.Integer, info=u'10-是否有效')
    remark   = db.Column(db.String(1024), info=u'11-备注')
    created  = db.Column(db.DateTime, default=datetime.now(), info=u'12-创建时间')
    updated  = db.Column(db.DateTime, default=datetime.now(), info=u'13-修改时间')
    
    _url  = '/admin/user'
    _name = u'user'
    _title= '用户'
    _dbop = 'db_User'
    
    
class Book(db.Model):
    # 图书
    id       = db.Column(db.Integer, primary_key=True, info=u'*1-ID')
    title    = db.Column(db.String(100), info=u'2-标题')
    summary  = db.Column(db.String(1024), info=u'3-简介')
    author   = db.Column(db.String(100), info=u'4-作者')
    content  = db.Column(db.Text, info=u'5-内容')
    flag     = db.Column(db.Integer, info=u'10-是否有效')
    remark   = db.Column(db.String(1024), info=u'11-备注')
    created  = db.Column(db.DateTime, default=datetime.now(), info=u'12-创建时间')
    updated  = db.Column(db.DateTime, default=datetime.now(), info=u'13-修改时间')
    
    _url  = '/admin/book'
    _name = u'book'
    _title= '图书'
    _dbop = 'db_Book'
    
class Author(db.Model):
    # 作者
    id       = db.Column(db.Integer, primary_key=True, info=u'*1-ID')
    name     = db.Column(db.String(100), unique=True, info=u'2-姓名')
    summary  = db.Column(db.String(1024), info=u'3-简介')
    flag     = db.Column(db.Integer, info=u'10-是否有效')
    remark   = db.Column(db.String(1024), info=u'11-备注')
    created  = db.Column(db.DateTime, default=datetime.now(), info=u'12-创建时间')
    updated  = db.Column(db.DateTime, default=datetime.now(), info=u'13-修改时间')
    
    _url  = '/admin/author'
    _name = u'author'
    _title= '作者'
    _dbop = 'db_Author'

class Category (db.Model):
    # 分类
    id       = db.Column(db.Integer, primary_key=True, info=u'*1-ID')
    name     = db.Column(db.String(100), unique=True, info=u'2-姓名')
    summary  = db.Column(db.String(1024), info=u'3-简介')
    flag     = db.Column(db.Integer, info=u'10-是否有效')
    remark   = db.Column(db.String(1024), info=u'11-备注')
    created  = db.Column(db.DateTime, default=datetime.now(), info=u'12-创建时间')
    updated  = db.Column(db.DateTime, default=datetime.now(), info=u'13-修改时间')
    
    _url  = '/admin/category'
    _name = u'category'
    _title= '图书分类'
    _dbop = 'db_Category'
    
    