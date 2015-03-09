# encoding:utf8
'''
这是后台管理的页面
'''
from common_import import *
from common_func import *

@app.route('/admin/')
@requires_auth
def admin():
    data = {}
    data['username'] = session.get('name', 'anyone')
    return render_template('admin/index.html', data=data)

@app.route('/admin/logout')
def admin_logout ():
    session.clear()
    return redirect(url_for ('admin_login'))

@app.route(config.login_url, methods=['POST', 'GET'])
def admin_login ():
    if request.method == "GET":
        data = {}
        return render_template('admin/login.html', data=data)
    elif request.method == "POST":
        cond = get_parameter('username', 'password')
        if not cond.get('username') or not cond.get('password'):
            flash (u'用户名密码不能为空')
            return render_template('admin/login.html')
        cond['password'] = md5(cond['password'])
        user = db.session.query(db_Staff).filter(db_Staff.flag==1).filter_by(**cond).first()
        if not user:
            flash (u'用户名密码不正确')
            app.logger.info ('用户名密码不正确, 用户名:%s, 密码:%s' %  (cond.get('username'), cond.get('password')))
            return render_template('admin/login.html')
        elif user.role != 1:
            flash (u'该用户没有权限')
            return render_template('admin/login.html')
        else:
            app.logger.info ('user login successful, user:%s' % user)
            session['admin_login'] = True
            session['name'] = user.name
            return redirect(url_for ('admin'))