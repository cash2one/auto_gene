#encoding:utf8
import hashlib
from datetime import datetime

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

#import etc
#db_info = etc.db_info

app = Flask(__name__)

'''
if __name__ == "__main__":
    app = Flask(__name__)
else:
    from myapp import app
'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@127.0.0.1/mydbname'
#app.config['SQLALCHEMY_DATABASE_URI'] = '%s://%s:%s@%s:%s/%s' % (db_info['driver'], db_info['user'],  \
#                                                                 db_info['pawd'], db_info['host'], \
#                                                                 db_info['port'], db_info['name'])
#app.config['SQLALCHEMY_ECHO'] = db_info['echo']
db = SQLAlchemy(app)


class User(db.Model):
    # 用户，包含普通用户和管理员
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32) )
    sex      = db.Column(db.String(1))
    name     = db.Column(db.String(100), nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    tel      = db.Column(db.String(20), unique=True, nullable=False)
    role     = db.Column(db.Integer)
    flag     = db.Column(db.Integer)   #状态，1：有效；   0:无效（被删除)
    remark   = db.Column(db.String(1024))
    created  = db.Column(db.DateTime, default=datetime.now())   #用户注册时间
    updated  = db.Column(db.DateTime, default=datetime.now())   #用户信息最后修改时间（不包含捐赠信息)
    
    def __init__(self, username='', password='', name='', email='', tel='', role=''):
        self.username = username
        self.password = hashlib.md5(password).hexdigest()
        self.name     = name
        self.email    = email
        self.tel      = tel
        self.role     = role
        self.flag     = 1

    def __repr__(self):
        return '<User %r>' % self.username
    
    def login (self, username, password):
        return self.query.filter_by(flag=1, username=username, password=hashlib.md5(password).hexdigest()).first()

class Item(db.Model):
    # 慈善项目
    id       = db.Column(db.Integer, primary_key=True)
    title    = db.Column(db.String(80))
    summary  = db.Column(db.String(1024))
    image    = db.Column(db.String(1024))
    body     = db.Column(db.Text)
    remark   = db.Column(db.String(1024))
    flag     = db.Column(db.Integer, default=1)  #状态, 1有效; 0无效（下线)
    author_id= db.Column(db.Integer, db.ForeignKey('user.id'))   #作者或最后编辑的用户
    created  = db.Column(db.DateTime, default=datetime.now())
    updated  = db.Column(db.DateTime, default=datetime.now())
    author   = db.relationship('User', backref=db.backref('item', lazy='dynamic'))

    def __init__(self, title='', summary='', image='', body=''):
        self.title   = title
        self.summary = summary
        self.image   = image
        self.body    = body

    def __repr__(self):
        return '<Item %r>' % self.title

class Transaction (db.Model):
    #每一笔交易 （捐赠)
    id       = db.Column(db.Integer, primary_key=True)
    user_id  = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id  = db.Column(db.Integer, db.ForeignKey('item.id'))
    money    = db.Column(db.Integer)
    status   = db.Column(db.Integer)
    remark   = db.Column(db.String(1024))
    created  = db.Column(db.DateTime, default=datetime.now())  #创建这笔交易的时间
    updated  = db.Column(db.DateTime, default=datetime.now())  #完成这笔交易的时间
    

