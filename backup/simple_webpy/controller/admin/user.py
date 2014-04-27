#encoding:utf-8
import datetime

import web

from model.admin import user as m_user
from lib.utils import render, user_login, admin_login

session = web.config._session


'''
remark: 集团内部的用户不会外开放使用,员工帐号
name: user
title: 用户
url: /admin/user
sub_title: 用户
table_name: user
----------database table-----
default: ;  	name: uid;  	null: n;  	title: 用户ID;  	type: varchar(20);  
default: ;  	name: code;  	null: n;  	title: 编号;  	type: varchar(20);  
default: ;  	name: name;  	null: n;  	title: 姓名;  	type: varchar(20);  
default: ;  	name: role;  	null: n;  	title: 角色;  	type: tinyint;  
default: ;  	name: dept;  	null: y;  	title: 部门;  	type: tinyint;  
default: ;  	display: n;  	name: id;  	null: n;  	title: 主键;  	type: int primary key auto_increment;  
default: ;  	display: n;  	name: create_user_id;  	null: y;  	title: 创建用户;  	type: int;  
default: ;  	display: n;  	name: update_user_id;  	null: y;  	title: 修改用户;  	type: int;  
default: ;  	display: n;  	name: create_date;  	null: y;  	title: 创建时间;  	type: date;  
default: ;  	display: n;  	name: update_date;  	null: y;  	title: 修改时间;  	type: date;  

'''

def get_user ():
    return session.get('user_id')

def get_date():
    return datetime.datetime.now()

def default_error (msg=''):
    raise web.notfound()

def check_right (xid, user_id=get_user() ):
    #当前用户是否有权限
    return m_user.exists (** { 'id': xid, 'create_user_id': user_id} )

class user_list:
    
    @admin_login
    def GET(self):
        request = web.input()
        index  = request.get('index',  '0').strip()
        length = request.get('length', '10') .strip()
        assert (str(index).isdigit())
        assert (str(length).isdigit())
        
        cond = {}
        cond['create_user_id'] = get_user()
        
        fields = ['uid', 'code', 'name', 'role', 'dept', 'id', 'create_user_id', 'update_user_id', 'create_date', 'update_date']
        
        for field in fields :
            if request.get(field,''):
                cond[field] = request.get(field).strip()
        
        data_list = m_user.get_many (index, length, **cond)
        
        data = {}
        data["user_id"]   = session.user_id
        data["user_name"] = session.user_name
        data["records"]   = data_list
        
        return render ('admin/user_list.html', data=data)


class user_read:
    @admin_login
    def GET(self, xid):
        assert (str(xid).isdigit())
        if not check_right (xid):
            print 'try to read an unauthrithm data, %s record id:%s , user id:%s'  %  ('user',xid, get_user())
            raise web.notfound()
        
        data = m_user.get_one (**{"id": int(xid)})
        return render ('admin/user_read.html', data = data)
        

class user_edit:

    def check_right (self, xid, user_id=get_user() ):
        #当前用户是否有权限
        return m_user.exists (** { 'id': xid, 'create_user_id': user_id} )
    
    def check_input (self, request, not_null_fields):
        #输入的字段 是否合法
        for item in not_null_fields:
            if request.get(item,None)  is None:
                return False    #Error
        return True  # OK
    
    @admin_login
    def GET(self,xid):
        assert (str(xid).isdigit())
        xid  = int(xid)
        
        if xid and not self.check_right (xid):
            print 'try to edit unauthorization data, table:%s,  id:%s'  %   ( 'user', xid)
            return default_error ()
        
        data = {}
        if xid:
            data = m_user.get_one (**{"id": int(xid)})
            if not data:
                print 'Error, try to edit record but not found data, table:%s,  id:%s'   % ('user', xid)
                raise web.notfound()
        return render ('admin/user_edit.html', data = data)
        
    @admin_login
    def POST(self,xid):
        #xid = web.input(xid=0).get('xid')
        assert (str(xid).isdigit())
        xid  = int(xid)
        
        request = web.input()
        input_fields = [ 'user_uid',  'user_code',  'user_name',  'user_role',  'user_dept', ]
        nonul_fields = [ 'user_uid',  'user_code',  'user_name',  'user_role', ]    #user input fileds, can not be emtpy
        
        #检查用户是否有权限
        if xid!=0 and not self.check_right (xid):
            print 'try to save an unauthrithm data, %s record id:%s , user id:%s'  %  ('user',xid, get_user())
            raise web.notfound()
        
        #检查是否存在 不能为空的字段 输入为空
        if not self.check_input (request, nonul_fields):
            print 'try to edit data, but found some not-null parameter null'
            return default_error('some parameter empty')
        
        data = {}
        if xid==0:   #new record
            print 'add new record into database for table user'
            data["id"] = 0
            data['create_date']    = get_date()
            data['create_user_id'] = get_user()
        else:
            print 'update record into database for table user'
            data = m_user.get_one ( ** {'id': xid})
            if not data:
                print 'try to update record into database, but fail'
                raise web.notfound()
            data['update_date']    = get_date()
            data['update_user_id'] = get_user()
        for field in input_fields:
            new_field = field.replace('user_','',1)
            data[new_field] = request.get(field,'')
        
        #if xid=0 then add   ;  otherwise  update
        m_user.upsert ("id",**data)
        return web.seeother('/admin/user'+"_list")


class user_delete:

    @admin_login
    def GET(self, xid):
        assert (str(xid).isdigit())
        if not check_right (xid):
            print 'try to delete an unauthrithm data, %s record id:%s , user id:%s'  %  ('user',xid, get_user())
            raise web.notfound()
        m_user.delete (**{"id":xid})
        return web.seeother('/admin/user' + '_list')
        