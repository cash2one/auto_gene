#encoding:utf-8
import datetime

import web

from model.admin import {{{{name}}}} as m_{{{{name}}}}
from lib.utils import render, user_login, admin_login

session = web.config._session


'''
{{{{schema}}}}
'''

def get_user ():
    return session.get('user_id')

def get_date():
    return datetime.datetime.now()

def default_error (msg=''):
    raise web.notfound()

def check_right (xid, user_id=get_user() ):
    #当前用户是否有权限
    return m_{{{{name}}}}.exists (** { 'id': xid, 'create_user_id': user_id} )

class {{{{name}}}}_list:
    
    @admin_login
    def GET(self):
        request = web.input()
        index  = request.get('index',  '0').strip()
        length = request.get('length', '10') .strip()
        assert (str(index).isdigit())
        assert (str(length).isdigit())
        
        cond = {}
        cond['create_user_id'] = get_user()
        
        fields = [{{{{input_fields}}}}]
        
        for field in fields :
            if request.get(field,''):
                cond[field] = request.get(field).strip()
        
        data_list = m_{{{{name}}}}.get_many (index, length, 'id desc', **cond)
        
        data = {}
        data["records"]   = data_list
        
        return render ('admin/{{{{name}}}}_list.html', data=data)


class {{{{name}}}}_read:
    @admin_login
    def GET(self, xid):
        assert (str(xid).isdigit())
        if not check_right (xid):
            print 'try to read an unauthrithm data, %s record id:%s , user id:%s'  %  ('{{{{name}}}}',xid, get_user())
            raise web.notfound()
        
        data = m_{{{{name}}}}.get_one ({"id": int(xid)})
        return render ('admin/{{{{name}}}}_read.html', data = data)
        

class {{{{name}}}}_edit:

    def check_right (self, xid, user_id=get_user() ):
        #当前用户是否有权限
        return m_{{{{name}}}}.exists (** { 'id': xid, 'create_user_id': user_id} )
    
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
            print 'try to edit unauthorization data, table:%s,  id:%s'  %   ( '{{{{name}}}}', xid)
            return default_error ()
        
        data = {}
        if xid:
            data = m_{{{{name}}}}.get_one (**{"id": int(xid)})
            if not data:
                print 'Error, try to edit record but not found data, table:%s,  id:%s'   % ('{{{{name}}}}', xid)
                raise web.notfound()
        return render ('admin/{{{{name}}}}_edit.html', data = data)
        
    @admin_login
    def POST(self,xid):
        #xid = web.input(xid=0).get('xid')
        assert (str(xid).isdigit())
        xid  = int(xid)
        
        request = web.input()
        input_fields = [{{{{input_fields}}}}]
        nonul_fields = [{{{{fields_not_null}}}}]    #user input fileds, can not be emtpy
        
        #检查用户是否有权限
        if xid!=0 and not self.check_right (xid):
            print 'try to save an unauthrithm data, %s record id:%s , user id:%s'  %  ('{{{{name}}}}',xid, get_user())
            raise web.notfound()
        
        #检查是否存在 不能为空的字段 输入为空
        if not self.check_input (request, nonul_fields):
            print 'try to edit data, but found some not-null parameter null'
            return default_error('some parameter empty')
        
        data = {}
        if xid==0:   #new record
            print 'add new record into database for table {{{{name}}}}'
            data["id"] = 0
            data['create_date']    = get_date()
            data['create_user_id'] = get_user()
        else:
            print 'update record into database for table {{{{name}}}}'
            data = m_{{{{name}}}}.get_one ( ** {'id': xid})
            if not data:
                print 'try to update record into database, but fail'
                raise web.notfound()
            data['update_date']    = get_date()
            data['update_user_id'] = get_user()
        for field in input_fields:
            new_field = field.replace('{{{{name}}}}_','',1)
            data[new_field] = request.get(field,'')
        
        #if xid=0 then add   ;  otherwise  update
        m_{{{{name}}}}.upsert ("id",**data)
        return web.seeother('{{{{url}}}}'+"_list")


class {{{{name}}}}_delete:

    @admin_login
    def GET(self, xid):
        assert (str(xid).isdigit())
        if not check_right (xid):
            print 'try to delete an unauthrithm data, %s record id:%s , user id:%s'  %  ('{{{{name}}}}',xid, get_user())
            raise web.notfound()
        m_{{{{name}}}}.delete (**{"id":xid})
        return web.seeother('{{{{url}}}}' + '_list')
        