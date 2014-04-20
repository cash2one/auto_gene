#encoding:utf-8
import datetime

import web

from model.admin import insp_value as m_insp_value
from lib.utils import render, user_login, admin_login

session = web.config._session


'''
remark: 
name: insp_value
title: 巡查值
url: /admin/insp_value
sub_title: 巡查值
table_name: insp_value
----------database table-----
default: ;  	name: insp_plan_id;  	null: n;  	title: 巡查计划;  	type: int;  
default: ;  	name: insp_item_id;  	null: n;  	title: 巡查项目;  	type: int;  
default: ;  	name: value;  	null: n;  	title: 巡查值（是否）;  	type: tinyint;  
default: ;  	name: remark;  	null: n;  	title: 巡查异常记录;  	type: varchar(1000);  
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
    return m_insp_value.exists (** { 'id': xid, 'create_user_id': user_id} )

class insp_value_list:
    
    @admin_login
    def GET(self):
        request = web.input()
        index  = request.get('index',  '0').strip()
        length = request.get('length', '10') .strip()
        assert (str(index).isdigit())
        assert (str(length).isdigit())
        
        cond = {}
        cond['create_user_id'] = get_user()
        
        fields = ['insp_plan_id', 'insp_item_id', 'value', 'remark', 'id', 'create_user_id', 'update_user_id', 'create_date', 'update_date']
        
        for field in fields :
            if request.get(field,''):
                cond[field] = request.get(field).strip()
        
        data_list = m_insp_value.get_many (index, length, **cond)
        
        data = {}
        data["user_id"]   = session.user_id
        data["user_name"] = session.user_name
        data["records"]   = data_list
        
        return render ('admin/insp_value_list.html', data=data)


class insp_value_read:
    @admin_login
    def GET(self, xid):
        assert (str(xid).isdigit())
        if not check_right (xid):
            print 'try to read an unauthrithm data, %s record id:%s , user id:%s'  %  ('insp_value',xid, get_user())
            raise web.notfound()
        
        data = {}
        data['record'] = m_insp_value.get_one ({"id",int(xid)})
        return render ('admin/insp_value_read.html', data = data)
        

class insp_value_edit:

    def check_right (self, xid, user_id=get_user() ):
        #当前用户是否有权限
        return m_insp_value.exists (** { 'id': xid, 'create_user_id': user_id} )
    
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
            print 'try to edit unauthorization data, table:%s,  id:%s'  %   ( 'insp_value', xid)
            return default_error ()
        
        data = {}
        if xid:
            data = m_insp_value.get_one (**{"id": int(xid)})
            if not data:
                print 'Error, try to edit record but not found data, table:%s,  id:%s'   % ('insp_value', xid)
                raise web.notfound()
        return render ('admin/insp_value_edit.html', data = data)
        
    @admin_login
    def POST(self,xid):
        #xid = web.input(xid=0).get('xid')
        assert (str(xid).isdigit())
        xid  = int(xid)
        
        request = web.input()
        input_fields = [ 'insp_value_insp_plan_id',  'insp_value_insp_item_id',  'insp_value_value',  'insp_value_remark', ]
        nonul_fields = [ 'insp_value_insp_plan_id',  'insp_value_insp_item_id',  'insp_value_value',  'insp_value_remark', ]    #user input fileds, can not be emtpy
        
        #检查用户是否有权限
        if xid!=0 and not self.check_right (xid):
            print 'try to save an unauthrithm data, %s record id:%s , user id:%s'  %  ('insp_value',xid, get_user())
            raise web.notfound()
        
        #检查是否存在 不能为空的字段 输入为空
        if not self.check_input (request, nonul_fields):
            print 'try to edit data, but found some not-null parameter null'
            return default_error('some parameter empty')
        
        data = {}
        if xid==0:   #new record
            print 'add new record into database for table insp_value'
            data["id"] = 0
            data['create_date']    = get_date()
            data['create_user_id'] = get_user()
        else:
            print 'update record into database for table insp_value'
            data = m_insp_value.get_one ( ** {'id': xid})
            if not data:
                print 'try to update record into database, but fail'
                raise web.notfound()
            data['update_date']    = get_date()
            data['update_user_id'] = get_user()
        for field in input_fields:
            new_field = field.replace('insp_value_','',1)
            data[new_field] = request.get(field,'')
        
        #if xid=0 then add   ;  otherwise  update
        m_insp_value.upsert ("id",**data)
        return web.seeother('/admin/insp_value'+"_list")


class insp_value_delete:

    @admin_login
    def GET(self, xid):
        assert (str(xid).isdigit())
        if not check_right (xid):
            print 'try to delete an unauthrithm data, %s record id:%s , user id:%s'  %  ('insp_value',xid, get_user())
            raise web.notfound()
        m_insp_value.delete (**{"id":xid})
        return web.seeother('/admin/insp_value' + '_list')
        