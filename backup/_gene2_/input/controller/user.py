@app.route('{{data.url}}')
@requires_auth
def admin_{{data.name}}():
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

@app.route('{{data.url}}/edit/<int:xid>', methods=['POST', 'GET'])
@requires_auth
def admin_{{data.name}}_edit(xid):
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

@app.route('{{data.url}}/delete/<int:xid>', methods=['POST', 'GET'])
@requires_auth
def admin_{{data.name}}_delete(xid):
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