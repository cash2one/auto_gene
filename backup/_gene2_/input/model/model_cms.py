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
    id       = db.Column(db.Integer, primary_key=True, info=u'*1-ID')
    username = db.Column(db.String(80), unique=True, info=u'2-用户名')
    password = db.Column(db.String(32), info=u'3-密码')
    flag     = db.Column(db.Integer, info=u'4-是否有效')
    remark   = db.Column(db.String(1024), info=u'5-备注')
    created  = db.Column(db.DateTime, default=datetime.now(), info=u'6-创建时间')
    updated  = db.Column(db.DateTime, default=datetime.now(), info=u'7-修改时间')
    
    _url  = '/admin/user'
    _name = u'user'
    _title= '用户'
    