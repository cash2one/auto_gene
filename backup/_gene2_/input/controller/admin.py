# encoding:utf8
'''
这是后台管理的页面
'''
import json
import hashlib

from flask import Flask
from flask import flash
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import make_response
from flask import render_template
from flask import get_flashed_messages

from werkzeug import secure_filename
from functools import wraps

from sqlalchemy import or_, and_

from model.model_crm import db, User as db_User, Item as db_Item, Transaction as db_Tran
import etc as config
import tools.common as common
import tools.common_flask as common_flask

if __name__ == "__main__":
    app = Flask(__name__)
else:
    from myapp import app

def get_parameter (*p):
    result = {}
    for i in p:
        result[i] = request.form.get(i,'')
    return result

def get_site_info ():
    site_info = {}
    return site_info

site = get_site_info()

def default_error (msg):
    return render_template ('admin/default_error.html', msg=msg)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_login' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/admin/login', methods=['POST', 'GET'])
def admin_login():
    msg  = ""
    if 'admin_login' in session:
        return redirect(url_for('admin'))
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','').strip()
        
        user = db_User().login (username, password)
        if not user:
            msg = u"用户不存在或用户名密码不正确"
            app.logger.info("User %s login fail, user not exists or password error" % username)
        elif user.role != config.user_role['admin']:
            msg = u"该用户没有权限登录后台"
            app.logger.info("User %s do not has the role to login admin page" % username)
        else:
            #登录成功
            app.logger.info("User %s login successful" % username)
            session['admin_login'] = True
            session['userid']      = user.id
            session['username']    = user.username
            session['userrole']    = user.role
            session['name']        = user.name
            return redirect(url_for('admin'))
    if msg:
        flash (msg)
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout ():
    session.clear()
    return redirect(url_for ('admin_login'))

@app.route('/admin/')
@requires_auth
def admin():
    data = {}
    data['username'] = session['name']
    return render_template('admin/index.html', data=data)

@app.route('/admin/user')
@requires_auth
def admin_user():
    length = request.args.get('length','10')
    index  = request.args.get('index', '1')
    length, index, offset = common.pagination_data (length, index, config.page['page_records'], config.page['page_records_max'])
    
    data = {}
    cond = {'flag':1}
    keyword = request.args.get('keyword','')
    if keyword:
        data['cur_keyword'] = keyword
        data['records'] = db.session.query(db_User).\
            filter(and_(db_User.flag==1, or_(db_User.tel==keyword, db_User.username==keyword, db_User.name==keyword)))
    else:
        data['records']  = db_User.query.filter_by(**cond).order_by('-id').limit(length).offset(offset)
    amount = db_User.query.filter_by(**cond).count()
    
    data['pgnation'] = common.pagination(index, amount, length, common_flask.pagination_url, common_flask.pagination_jump)
    return render_template('admin/user_list.html', data=data)

@app.route('/admin/user/edit/<int:xid>', methods=['POST', 'GET'])
@requires_auth
def admin_user_edit(xid):
    if xid==0:
        record = {}
    else:
        record = db_User.query.filter_by(flag=1, id=xid).first()
        if not record:
            return default_error (u'用户不存在')
        
    if request.method == "GET":
        data = {}
        data['deny_password'] = config.deny_password
        data['record'] = record
        return render_template('admin/user_edit.html', data=data)
    else:
        temp = get_parameter('sex', 'username', 'password1','password2', 'name', 'email', 'tel', 'remark')
        if temp['sex'] not in ['f','m'] or not temp['username'] or not temp['password1'] or not temp['password2'] \
            or temp['password1'] != temp['password2'] or not temp['name'] or not temp['email'] or not temp['tel']:
            return default_error (u'参数不正确')
        if xid == 0 and temp['password1'] == config.deny_password:
            return default_error (u'不能使用%s作为密码' % config.deny_password)
            
        temp.pop('password2')
        password = temp.pop('password1')
        if xid != 0 and password == config.deny_password:
            #没有修改密码
            temp['password'] = record.password
        else:
            #需要修改密码
            temp['password'] = hashlib.md5(password).hexdigest()
        
        if xid == 0:
            #add
            record = db_User()
        for k,v in temp.iteritems():
            setattr(record, k, v)
        setattr(record, 'role', config.user_role['user'])
        db.session.add (record)
        db.session.commit()
        if xid == 0:
            flash (u'操作成功，已添加用户%s' % temp['name'])
            app.logger.info ("admin(%s) add  user(%s)'s infomation" % (session['name'], record.name))
        else:
            flash (u'操作成功,已修改用户%s的信息' % temp['name'])
            app.logger.info ("admin(%s) edit user(%s)'s infomation" % (session['name'], record.name))
        return redirect(url_for('admin_user'))

@app.route('/admin/user/delete/<int:xid>', methods=['POST', 'GET'])
@requires_auth
def admin_user_delete(xid):
    if request.method == "GET":
        record = db_User.query.filter_by(id=int(xid)).first()
        if not record:
            return default_error (u'该用户不存在')
        record.flag = 0 #修改用户的标识，相当于删除
        db.session.add(record)
        db.session.commit ()
        app.logger.info (u'admin(%s) delete one user(%s)' % (session['name'], record.name))
        flash (u'操作成功，已删除用户%s' % record.name)
        return redirect (url_for ('admin_user'))
    else:
        #POST, 删除多行
        xids = request.form.get('xids')
        xids = [int(i) for i in xids.split(',') if i and i.isdigit() ]
        aa=db.session.query(db_User).filter(db_User.id.in_ (xids) ).update({'flag':0}, synchronize_session=False)
        db.session.commit ()
        app.logger.info ('admin(%s) delete %d users, user id list is %s' % (session['name'], aa, xids))
        return json.dumps ({'msg':u'删除成功'})


@app.route('/admin/project')
@requires_auth
def admin_project():
    length = request.args.get('length','10')
    index  = request.args.get('index', '1')
    length, index, offset = common.pagination_data (length, index, config.page['page_records'], config.page['page_records_max'])
    
    data = {}
    cond = {'flag':1}
    keyword = request.args.get('keyword','')
    if keyword:
        data['cur_keyword'] = keyword
        data['records'] = db.session.query(db_Item).\
            filter(and_(db_Item.flag==1, or_(db_Item.title.like('%'+keyword+'%'), db_Item.summary.like('%'+keyword+'%'))))
    else:
        data['records']  = db_Item.query.filter_by(**cond).order_by('-id').limit(length).offset(offset)
    amount = db_Item.query.filter_by(**cond).count()
    
    data['pgnation'] = common.pagination(index, amount, length, common_flask.pagination_url, common_flask.pagination_jump)
    return render_template('admin/project_list.html', data=data)


@app.route('/admin/project/edit/<int:xid>', methods=['POST', 'GET'])
@requires_auth
def admin_project_edit(xid):
    if xid==0:
        record = {}
    else:
        record = db_Item.query.filter_by(flag=1, id=xid).first()
        if not record:
            return default_error (u'该项目不存在')
        
    if request.method == "GET":
        data = {}
        data['record'] = record
        return render_template('admin/project_edit.html', data=data)
    else:
        temp = get_parameter('title', 'summary', 'remark', 'body')
        if not temp['title']:
            return default_error (u'参数不正确')
        
        if xid == 0:
            #add
            record = db_Item()
        for k,v in temp.iteritems():
            setattr(record, k, v)
        record.author_id = session['userid']
        db.session.add (record)
        db.session.commit()
        if xid == 0:
            flash (u'操作成功，已添加项目%s' % temp['title'])
            app.logger.info ("admin(%s) add  project(%s)'s infomation" % (session['name'], temp.get('title')))
        else:
            flash (u'操作成功,已修改项目%s的信息' % temp['title'])
            app.logger.info ("admin(%s) edit project(%s)'s infomation" % (session['name'], temp.get('title')))
        return redirect(url_for('admin_project'))


@app.route('/admin/project/delete/<int:xid>', methods=['POST', 'GET'])
@requires_auth
def admin_project_delete(xid):
    if request.method == "GET":
        record = db_Item.query.filter_by(id=int(xid)).first()
        if not record:
            return default_error (u'该用户不存在')
        record.flag = 0 #修改用户的标识，相当于删除
        db.session.add(record)
        db.session.commit ()
        app.logger.info (u'admin(%s) delete one project(%s)' % (session['name'], record.title))
        flash (u'操作成功，已删除用户%s' % record.title)
        return redirect (url_for ('admin_project'))
    else:
        #POST, 删除多行
        xids = request.form.get('xids')
        xids = [int(i) for i in xids.split(',') if i and i.isdigit() ]
        aa=db.session.query(db_Item).filter(db_Item.id.in_ (xids) ).update({'flag':0}, synchronize_session=False)
        db.session.commit ()
        app.logger.info ('admin(%s) delete %d project, project id list is %s' % (session['name'], aa, xids))
        return json.dumps ({'msg':u'删除成功'})
    
    


@app.route('/admin/operator')
@requires_auth
def admin_operator():
    length = request.args.get('length','10')
    index  = request.args.get('index', '1')
    length, index, offset = common.pagination_data (length, index, config.page['page_records'], config.page['page_records_max'])
    
    data = {}
    cond = {'flag':1, 'role':1}
    keyword = request.args.get('keyword','')
    if keyword:
        data['cur_keyword'] = keyword
        data['records'] = db.session.query(db_User).\
            filter(and_(db_User.flag==1, db_User.role==1, or_(db_User.tel==keyword, db_User.username==keyword, db_User.name==keyword)))
    else:
        data['records']  = db_User.query.filter_by(**cond).order_by('-id').limit(length).offset(offset)
    amount = db_User.query.filter_by(**cond).count()
    
    data['pgnation'] = common.pagination(index, amount, length, common_flask.pagination_url, common_flask.pagination_jump)
    return render_template('admin/operator_list.html', data=data)

@app.route('/admin/user/become_operator/<int:xid>', methods=['POST', 'GET'])
@requires_auth
def admin_operator_from_user(xid):
    if request.method == "GET":
        record = db_User.query.filter_by(id=int(xid)).first()
        if not record:
            return default_error (u'该用户不存在')
        record.role = 1
        db.session.add(record)
        db.session.commit ()
        app.logger.info (u'admin(%s) set user(%s) to operator' % (session['name'], record.name))
        flash (u'操作成功，已将用户%s设置为系统管理员' % record.name)
        return redirect (url_for ('admin_operator'))
    else:
        #POST, 操作多行
        xids = request.form.get('xids')
        xids = [int(i) for i in xids.split(',') if i and i.isdigit() ]
        aa=db.session.query(db_User).filter(db_User.id.in_ (xids) ).update({'role':1}, synchronize_session=False)
        db.session.commit ()
        app.logger.info ('admin(%s) set %s users to operator, user id list is %s' % (session['name'], aa, xids))
        return json.dumps ({'msg':u'操作成功'})

@app.route('/admin/user/become_user/<int:xid>', methods=['POST', 'GET'])
@requires_auth
def admin_operator_to_user(xid):
    if request.method == "GET":
        record = db_User.query.filter_by(id=int(xid)).first()
        if not record:
            return default_error (u'该用户不存在')
        record.role = 2
        db.session.add(record)
        db.session.commit ()
        app.logger.info (u'admin(%s) set user(%s) to operator' % (session['name'], record.name))
        flash (u'操作成功，已将用户%s设置为普通员工' % record.name)
        return redirect (url_for ('admin_operator'))
    else:
        #POST, 操作多行
        xids = request.form.get('xids')
        xids = [int(i) for i in xids.split(',') if i and i.isdigit() ]
        aa=db.session.query(db_User).filter(db_User.id.in_ (xids) ).update({'role':2}, synchronize_session=False)
        db.session.commit ()
        app.logger.info ('admin(%s) set %s users to user, user id list is %s' % (session['name'], aa, xids))
        return json.dumps ({'msg':u'操作成功'})

if __name__ == "__main__":
    app.debug = config.debug_mode    
    app.secret_key = config.session_key       
    app.run() 