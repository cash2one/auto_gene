#encoding:utf8

#这个是系统初始化时（第一次安装）执行的脚本,
#用于创建系统所需要的数据库的表


import os
import sys
sys.path.append (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import etc as config

from model.model_crm import *
db.drop_all()  #drop all tables
db.create_all()   #create the tables in the database


tmp = User.query.filter_by(username='admin').first()
if not tmp:
    user = User('admin', '1234','小明', 'm@126.com', '12345214521', config.user_role['admin'])  #1:超级管理员
    db.session.add(user)
    db.session.commit()

print 'init db done'

