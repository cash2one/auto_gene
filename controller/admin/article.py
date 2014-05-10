#encoding:utf-8
import datetime

import web

from model.tables import article as m_article
from lib.utils import render, user_login, admin_login, next_page
from lib import utils
session = web.config._session

'''
文章管理
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
    return m_article.exists (** { 'id': xid, 'create_user': user_id} )

class article_list:
    
    @admin_login
    def GET(self):
        request = web.input()
        index  = request.get('__index',  '0').strip()
        length = request.get('__length', '10') .strip()
        assert (str(index).isdigit())
        assert (str(length).isdigit())
        index  = int(index)
        length = int(length)
        
        fields = [  'article_content',  'article_id',  'article_create_time',  'article_create_user',  'article_update_time',  'article_update_user',  'article_valid',  ]
        cond = {}
        data = {}
        data['filter'] = {}
        for field in fields :
            if request.get(field,'').strip():
                new_field = field.replace('article_','',1)
                data['filter'][new_field] = request.get(field).strip()
                cond[new_field] = request.get(field).strip()
        
        if request.get('__format','') == 'xls':
            data_list = m_article.get_many (0, 10000000000, 'id desc', **cond)
            filename = u'%s.xls' % '文章'
            fields   = {}
            fields['key'] = [  'content',  'id',  'create_time',  'create_user',  'update_time',  'update_user',  'valid',  ]
            fields['title'] = [ u'序号',  u'正文',  u'ID',  u'创建时间',  u'创建用户',  u'最后修改时间',  u'最后修改用户',  u'状态',  ]
            return utils.output_excel (filename, fields, data_list)
        
        data_list = m_article.get_many (index, length, 'id desc', **cond)
        data_len  = m_article.get_amount (**cond)
        
        data["records"]   = data_list
        data['next_page'] = next_page (index, length, data_len)
        return render ('admin/article_list.html', item=data)


class article_read:
    @admin_login
    def GET(self, xid):
        assert (str(xid).isdigit())
        if not check_right (xid):
            print 'try to read an unauthrithm data, %s record id:%s , user id:%s'  %  ('article',xid, get_user())
            raise web.notfound()
        record = m_article.get_one (**{"id": int(xid)})
        return render ('admin/article_read.html', data = {'record':record})
        

class article_edit:
    
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
            print 'try to edit unauthorization data, table:%s,  id:%s'  %   ( 'article', xid)
            return default_error ()
        
        data = {}
        if xid:
            data['record'] = m_article.get_one (**{"id": int(xid)})
            if not data:
                print 'Error, try to edit record but not found data, table:%s,  id:%s'   % ('article', xid)
                raise web.notfound()
        return render ('admin/article_edit.html', data = data)
        
    @admin_login
    def POST(self,xid):
        #xid = web.input(xid=0).get('xid')
        assert (str(xid).isdigit())
        xid  = int(xid)
        
        request = web.input()
        input_fields = [   'article_content',               ]
        nonul_fields = [   'article_content',               ]   #user input fileds, can not be emtpy
        
        #检查用户是否有权限
        if xid!=0 and not check_right (xid):
            print 'try to save an unauthrithm data, %s record id:%s , user id:%s'  %  ('article',xid, get_user())
            raise web.notfound()
        
        #检查是否存在 不能为空的字段 输入为空
        if not self.check_input (request, nonul_fields):
            print 'try to edit data, but found some not-null parameter null, table: %s'  % 'article'
            return default_error('some parameter empty')
        
        data = {}
        
        if xid==0:   #new record
            print 'add new record into database for table article'
            data["id"] = 0
            data['create_time'] = get_date(); data['create_user'] = get_user()
        else:
            print 'update record into database for table article'
            data = m_article.get_one ( ** {'id': xid})
            if not data:
                print 'try to update record into database, but fail'
                raise web.notfound()
            data['update_time'] = get_date(); data['update_user'] = get_user()
        for field in input_fields:
            new_field = field.replace('article_','',1)
            data[new_field] = request.get(field,'')
        
        #if xid=0 then add   ;  otherwise  update
        m_article.upsert ("id",**data)
        return web.seeother('/admin/article'+"_list")


class article_delete:

    @admin_login
    def GET(self, xid):
        assert (str(xid).isdigit())
        if not check_right (xid):
            print 'try to delete an unauthrithm data, %s record id:%s , user id:%s'  %  ('article',xid, get_user())
            raise web.notfound()
        m_article.delete (**{"id":xid})
        return web.seeother('/admin/article' + '_list')
        