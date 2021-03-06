#encoding:utf-8
import datetime

import web

from model.admin import insp_type as m_insp_type
from lib.utils import render, user_login, admin_login

session = web.config._session


'''
remark: 
name: insp_type
title: 巡查项目类型
url: /admin/insp_type
sub_title: 巡查项目类型
table_name: insp_type
----------database table-----
default: ;  	name: name;  	null: n;  	title: 名字;  	type: varchar(100);  
default: 1;  	name: ord;  	null: n;  	title: 顺序;  	type: tinyint;  
default: 1;  	name: valid;  	null: y;  	title: 是否显示;  	type: tinyint;  
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
    return m_insp_type.exists (** { 'id': xid, 'create_user_id': user_id} )

class insp_type_list:
    
    @admin_login
    def GET(self):
        request = web.input()
        index  = request.get('index',  '0').strip()
        length = request.get('length', '10') .strip()
        assert (str(index).isdigit())
        assert (str(length).isdigit())
        
        cond = {}
        cond['create_user_id'] = get_user()
        
        fields = ['name', 'ord', 'valid', 'id', 'create_user_id', 'update_user_id', 'create_date', 'update_date']
        
        for field in fields :
            if request.get(field,''):
                cond[field] = request.get(field).strip()
        
        data_list = m_insp_type.get_many (index, length, **cond)
        
        data = {}
        data["user_id"]   = session.user_id
        data["user_name"] = session.user_name
        data["records"]   = data_list
        
        return render ('admin/insp_type_list.html', data=data)


class insp_type_read:
    @admin_login
    def GET(self, xid):
        assert (str(xid).isdigit())
        if not check_right (xid):
            print 'try to read an unauthrithm data, %s record id:%s , user id:%s'  %  ('insp_type',xid, get_user())
            raise web.notfound()
        
        data = {}
        data['record'] = m_insp_type.get_one ({"id",int(xid)})
        return render ('admin/insp_type_read.html', data = data)
        

class insp_type_edit:

    def check_right (self, xid, user_id=get_user() ):
        #当前用户是否有权限
        return m_insp_type.exists (** { 'id': xid, 'create_user_id': user_id} )
    
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
            print 'try to edit unauthorization data, table:%s,  id:%s'  %   ( 'insp_type', xid)
            return default_error ()
        
        data = {}
        if xid:
            data = m_insp_type.get_one (**{"id": int(xid)})
            if not data:
                print 'Error, try to edit record but not found data, table:%s,  id:%s'   % ('insp_type', xid)
                raise web.notfound()
        return render ('admin/insp_type_edit.html', data = data)
        
    @admin_login
    def POST(self,xid):
        #xid = web.input(xid=0).get('xid')
        assert (str(xid).isdigit())
        xid  = int(xid)
        
        request = web.input()
        input_fields = [ 'insp_type_name',  'insp_type_ord',  'insp_type_valid', ]
        nonul_fields = [ 'insp_type_name',  'insp_type_ord', ]    #user input fileds, can not be emtpy
        
        #检查用户是否有权限
        if xid!=0 and not self.check_right (xid):
            print 'try to save an unauthrithm data, %s record id:%s , user id:%s'  %  ('insp_type',xid, get_user())
            raise web.notfound()
        
        #检查是否存在 不能为空的字段 输入为空
        if not self.check_input (request, nonul_fields):
            print 'try to edit data, but found some not-null parameter null'
            return default_error('some parameter empty')
        
        data = {}
        if xid==0:   #new record
            print 'add new record into database for table insp_type'
            data["id"] = 0
            data['create_date']    = get_date()
            data['create_user_id'] = get_user()
        else:
            print 'update record into database for table insp_type'
            data = m_insp_type.get_one ( ** {'id': xid})
            if not data:
                print 'try to update record into database, but fail'
                raise web.notfound()
            data['update_date']    = get_date()
            data['update_user_id'] = get_user()
        for field in input_fields:
            new_field = field.replace('insp_type_','',1)
            data[new_field] = request.get(field,'')
        
        #if xid=0 then add   ;  otherwise  update
        m_insp_type.upsert ("id",**data)
        return web.seeother('/admin/insp_type'+"_list")


class insp_type_delete:

    @admin_login
    def GET(self, xid):
        assert (str(xid).isdigit())
        if not check_right (xid):
            print 'try to delete an unauthrithm data, %s record id:%s , user id:%s'  %  ('insp_type',xid, get_user())
            raise web.notfound()
        m_insp_type.delete (**{"id":xid})
        return web.seeother('/admin/insp_type' + '_list')
        