#encoding:utf-8
from common_func import *
from common_import import *


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
            return default_error (u'该数据不存在')
        
    if request.method == "GET":
        data = {}
        data['record'] = record
        return render_template('admin/user_edit.html', data=data)
    elif request.method == "POST":
        temp = get_parameter( '', '', '', '', '', '', '', '', '',)
        if not temp.get('username'):
            return default_error (u'参数不正确')
        
        if xid == 0:
            #add
            record = db_User()
        for k,v in temp.iteritems():
            setattr(record, k, v)
        db.session.add (record)
        db.session.commit()
        if xid == 0:
            flash (u'添加成功')
            app.logger.info ("user(%s) add one record(%s) into database " % (session['name'], record))
        else:
            flash (u'修改成功')
            app.logger.info ("user(%s) edit one record(%s) in database " % (session['name'], record))
        return redirect(url_for('admin_user'))

@app.route('/admin/user/delete/<int:xid>', methods=['POST', 'GET'])
@requires_auth
def admin_user_delete(xid):
    if request.method == "GET":
        record = db_User.query.filter_by(id=int(xid)).first()
        if not record:
            return default_error (u'该数据不存在')
        record.flag = 0 #修改用户的标识，相当于删除
        db.session.add(record)
        db.session.commit ()
        app.logger.info (u'admin(%s) delete one record(%s)' % (session['name'], record))
        flash (u'操作成功，已删除用户%s' % record.name)
        return redirect (url_for ('admin_user'))
    else:
        #POST, 删除多行
        xids = request.form.get('xids')
        xids = [int(i) for i in xids.split(',') if i and i.isdigit() ]
        aa=db.session.query(db_User).filter(db_User.id.in_ (xids) ).update({'flag':0}, synchronize_session=False)
        db.session.commit ()
        app.logger.info ('admin(%s) delete %d users, user id list is %s' % (session['name'], aa, xids))
        return tojson({'msg':u'删除成功'})