#encoding:utf-8
import datetime

import web

from model.tables import user as m_user
from lib.utils import render, user_login, admin_login, next_page
from lib import utils
session = web.config._session

'''
用户信息表
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
    return m_user.exists (** { 'id': xid, 'create_user': user_id} )

class user_list:
    
    @admin_login
    def GET(self):
        request = web.input()
        index  = request.get('__index',  '0').strip()
        length = request.get('__length', '10') .strip()
        assert (str(index).isdigit())
        assert (str(length).isdigit())
        index  = int(index)
        length = int(length)
        
        fields = [  'user_memID',  'user_userID',  'user_userCode',  'user_userName',  'user_chainID',  'user_projectID',  'user_cityID',  'user_cityName',  'user_managerID',  'user_managerName',  'user_stationID',  'user_stationName',  'user_email',  'user_tel',  'user_mobile',  'user_joinDate',  'user_status',  'user_id',  'user_create_time',  'user_create_user',  'user_update_time',  'user_update_user',  'user_valid',  ]
        cond = {}
        data = {}
        data['filter'] = {}
        for field in fields :
            if request.get(field,'').strip():
                new_field = field.replace('user_','',1)
                data['filter'][new_field] = request.get(field).strip()
                cond[new_field] = request.get(field).strip()
        
        if request.get('__format','') == 'xls':
            data_list = m_user.get_many (0, 10000000000, 'id desc', **cond)
            filename = u'%s.xls' % '用户'
            fields   = {}
            fields['key'] = [  'memID',  'userID',  'userCode',  'userName',  'chainID',  'projectID',  'cityID',  'cityName',  'managerID',  'managerName',  'stationID',  'stationName',  'email',  'tel',  'mobile',  'joinDate',  'status',  'id',  'create_time',  'create_user',  'update_time',  'update_user',  'valid',  ]
            fields['title'] = [ u'序号',  u'用户会员编号',  u'用户ID',  u'用户编号',  u'用户姓名',  u'分店ID',  u'分店编号',  u'城市ID',  u'城市名称',  u'经理ID',  u'经理姓名',  u'职位ID',  u'职位名称',  u'Email邮件',  u'固定电话',  u'手机',  u'入职日期',  u'状态',  u'ID',  u'创建时间',  u'创建用户',  u'最后修改时间',  u'最后修改用户',  u'状态',  ]
            return utils.output_excel (filename, fields, data_list)
        
        data_list = m_user.get_many (index, length, 'id desc', **cond)
        data_len  = m_user.get_amount (**cond)
        
        data["records"]   = data_list
        data['next_page'] = next_page (index, length, data_len)
        return render ('admin/user_list.html', item=data)


class user_read:
    @admin_login
    def GET(self, xid):
        assert (str(xid).isdigit())
        if not check_right (xid):
            print 'try to read an unauthrithm data, %s record id:%s , user id:%s'  %  ('user',xid, get_user())
            raise web.notfound()
        record = m_user.get_one (**{"id": int(xid)})
        return render ('admin/user_read.html', data = {'record':record})
        

class user_edit:
    
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
            print 'try to edit unauthorization data, table:%s,  id:%s'  %   ( 'user', xid)
            return default_error ()
        
        data = {}
        if xid:
            data['record'] = m_user.get_one (**{"id": int(xid)})
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
        input_fields = [   'user_memID',    'user_userID',    'user_userCode',    'user_userName',    'user_chainID',    'user_projectID',    'user_cityID',    'user_cityName',    'user_managerID',    'user_managerName',    'user_stationID',    'user_stationName',    'user_email',    'user_tel',    'user_mobile',    'user_joinDate',    'user_status',               ]
        nonul_fields = [   'user_memID',    'user_userID',    'user_userCode',    'user_userName',                                         ]   #user input fileds, can not be emtpy
        
        #检查用户是否有权限
        if xid!=0 and not check_right (xid):
            print 'try to save an unauthrithm data, %s record id:%s , user id:%s'  %  ('user',xid, get_user())
            raise web.notfound()
        
        #检查是否存在 不能为空的字段 输入为空
        if not self.check_input (request, nonul_fields):
            print 'try to edit data, but found some not-null parameter null, table: %s'  % 'user'
            return default_error('some parameter empty')
        
        data = {}
        
        if xid==0:   #new record
            print 'add new record into database for table user'
            data["id"] = 0
            data['create_time'] = get_date(); data['create_user'] = get_user()
        else:
            print 'update record into database for table user'
            data = m_user.get_one ( ** {'id': xid})
            if not data:
                print 'try to update record into database, but fail'
                raise web.notfound()
            data['update_time'] = get_date(); data['update_user'] = get_user()
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
        