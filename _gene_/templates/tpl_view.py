#encoding:utf-8
import datetime

import web

from model.tables import {{item.table_name}} as m_{{item.name}}
from lib.utils import render, user_login, admin_login, next_page

session = web.config._session

'''
{{item.remark}}
'''

def get_user ():
    return session.get('user_id')

def get_date():
    return datetime.datetime.now()

def default_error (msg=''):
    raise web.notfound()

def check_right (xid, user_id=get_user() ):
    return True
    #当前用户是否有权限
    return m_{{item.name}}.exists (** { 'id': xid, 'create_user': user_id} )

class {{item.name}}_list:
    
    @admin_login
    def GET(self):
        request = web.input()
        index  = request.get('__index',  '0').strip()
        length = request.get('__length', '10') .strip()
        assert (str(index).isdigit())
        assert (str(length).isdigit())
        index  = int(index)
        length = int(length)
        
        fields = [ {% for line in item.table.fields %} '{{ item.name }}_{{ line.field }}', {% endfor %} ]
        cond = {}
        data = {}
        data['filter'] = {}
        for field in fields :
            if request.get(field,'').strip():
                new_field = field.replace('{{item.name}}_','',1)
                data['filter'][new_field] = request.get(field).strip()
                cond[new_field] = request.get(field).strip()
        
        data_list = m_{{item.name}}.get_many (index, length, 'id desc', **cond)
        data_len  = m_{{item.name}}.get_amount (**cond)
        
        data["records"]   = data_list
        data['next_page'] = next_page (index, length, data_len)
        
        return render ('admin/{{item.name}}_list.html', item=data)


class {{item.name}}_read:
    @admin_login
    def GET(self, xid):
        assert (str(xid).isdigit())
        if not check_right (xid):
            print 'try to read an unauthrithm data, %s record id:%s , user id:%s'  %  ('{{item.name}}',xid, get_user())
            raise web.notfound()
        record = m_{{item.name}}.get_one (**{"id": int(xid)})
        return render ('admin/{{item.name}}_read.html', data = {'record':record})
        

class {{item.name}}_edit:
    
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
        
        if xid and not check_right (xid):
            print 'try to edit unauthorization data, table:%s,  id:%s'  %   ( '{{item.name}}', xid)
            return default_error ()
        
        data = {}
        if xid:
            data['record'] = m_{{item.name}}.get_one (**{"id": int(xid)})
            if not data:
                print 'Error, try to edit record but not found data, table:%s,  id:%s'   % ('{{item.name}}', xid)
                raise web.notfound()
        return render ('admin/{{item.name}}_edit.html', data = data)
        
    @admin_login
    def POST(self,xid):
        #xid = web.input(xid=0).get('xid')
        assert (str(xid).isdigit())
        xid  = int(xid)
        
        request = web.input()
        input_fields = [ {% for line in item.table.fields %} '{{item.name}}_{{line.field}}', {% endfor %} ]
        nonul_fields = [ {% for line in item.table.fields %} {% if line.null=='n' %} '{{item.name}}_{{line.field}}', {% endif %} {% endfor %} ]   #user input fileds, can not be emtpy
        
        #检查用户是否有权限
        if xid!=0 and not check_right (xid):
            print 'try to save an unauthrithm data, %s record id:%s , user id:%s'  %  ('{{item.name}}',xid, get_user())
            raise web.notfound()
        
        #检查是否存在 不能为空的字段 输入为空
        if not self.check_input (request, nonul_fields):
            print 'try to edit data, but found some not-null parameter null'
            return default_error('some parameter empty')
        
        data = {}
        if xid==0:   #new record
            print 'add new record into database for table {{item.name}}'
            data["id"] = 0
            data['create_time'] = get_date()
            data['create_user'] = get_user()
        else:
            print 'update record into database for table {{item.name}}'
            data = m_{{item.name}}.get_one ( ** {'id': xid})
            if not data:
                print 'try to update record into database, but fail'
                raise web.notfound()
            data['update_time'] = get_date()
            data['update_user'] = get_user()
        for field in input_fields:
            new_field = field.replace('{{item.name}}_','',1)
            data[new_field] = request.get(field,'')
        
        #if xid=0 then add   ;  otherwise  update
        m_{{item.name}}.upsert ("id",**data)
        return web.seeother('{{item.url}}'+"_list")


class {{item.name}}_delete:

    @admin_login
    def GET(self, xid):
        assert (str(xid).isdigit())
        if not check_right (xid):
            print 'try to delete an unauthrithm data, %s record id:%s , user id:%s'  %  ('{{item.name}}',xid, get_user())
            raise web.notfound()
        m_{{item.name}}.delete (**{"id":xid})
        return web.seeother('{{item.url}}' + '_list')
        