#encoding:utf-8
import web
from lib.utils import render, user_login, admin_login

session = web.config._session

def default_error ():
    raise web.notfound()


class index:
    @admin_login
    def GET(self):
        data = {}
        data['userid']   = session.get('userid')
        data['username'] = session.get('username')
        return render ("admin/admin.html", data = data)
    
class login:
    def GET(self):
        data = {}
        return render ("admin/login.html", data = data)
    
    def POST (self):
        request = web.input()
        user_id = request.get('user_id', '').strip()
        user_pw = request.get('user_pw', '').strip()
        
        msg = ''
        if not user_id or not user_pw:
            msg = u'用户，密码不能为空'
            
        elif user_id != 'admin' or user_pw !='admin':
            msg = u'用户名或密码不正确'
            
        if msg:
            data = {}
            data['error_msg'] = msg
            return render ("admin/login.html", data = data)
        
        if user_id == 'admin' and user_pw == 'admin':
            session.user_name = u'小明'
            session.user_code = user_id
            session.user_id = 1234
            session.admin   = True
            web.seeother("/admin/")
            
class logout:
    def GET(self):
        session.kill()
        web.seeother ("/admin/login")