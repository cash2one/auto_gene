#encoding:utf-8
from common_import import *
from common_func import *

@app.route('/admin/staff')
@requires_auth
def admin_staff():
    length = request.args.get('length','10')
    index  = request.args.get('index', '1')
    length, index, offset = common.pagination_data (length, index, config.page['page_records'], config.page['page_records_max'])
    
    data = {}
    cond = {'flag':1}
    keyword = request.args.get('keyword','')
    if keyword:
        data['cur_keyword'] = keyword
        data['records'] = db.session.query(db_Staff).\
            filter(and_(db_Staff.flag==1, or_(db_Staff.tel==keyword, db_Staff.username==keyword, db_Staff.name==keyword)))
    else:
        data['records']  = db_Staff.query.filter_by(**cond).order_by('-id').limit(length).offset(offset)
    amount = db_Staff.query.filter_by(**cond).count()
    
    data['pgnation'] = common.pagination(index, amount, length, common_flask.pagination_url, common_flask.pagination_jump)
    return render_template('admin/staff_list.html', data=data)

@app.route('/admin/staff/edit/<int:xid>', methods=['POST', 'GET'])
@requires_auth
def admin_staff_edit(xid):
    if xid==0:
        record = {}
    else:
        record = db_Staff.query.filter_by(flag=1, id=xid).first()
        if not record:
            return default_error (u'该数据不存在')
        
    if request.method == "GET":
        data = {}
        data['position_list'] = db_Dept.query.all()
        data['dept_list'] = db_Position.query.all() 
        data['record'] = record
        return render_template('admin/staff_edit.html', data=data)
    elif request.method == "POST":
        temp = get_parameter(  'username', 'password', 'name', 'posi_id', 'stat_id', 'join', 'leave', 'mobile', 'email', 'line_mg', 'flag', 'remark',  )
        
        if xid == 0:
            #add
            record = db_Staff()
        for k,v in temp.iteritems():
            setattr(record, k, v)
        db.session.add (record)
        db.session.commit()
        if xid == 0:
            flash (u'添加成功')
            app.logger.info ("user(%s) add one record(%s) into database " % (get_user(), record))
        else:
            flash (u'修改成功')
            app.logger.info ("user(%s) edit one record(%s) in database " % (get_user(), record))
        return redirect(url_for('admin_staff'))

@app.route('/admin/staff/delete/<int:xid>', methods=['POST', 'GET'])
@requires_auth
def admin_staff_delete(xid):
    if request.method == "GET":
        record = db_Staff.query.filter_by(id=int(xid)).first()
        if not record:
            return default_error (u'该数据不存在')
        record.flag = 0 #修改用户的标识，相当于删除
        db.session.add(record)
        db.session.commit ()
        app.logger.info (u'user(%s) delete one record(%s)' % (get_user(), record))
        flash (u'成功删除一条数据')
        return redirect (url_for ('admin_staff'))
    else:
        #POST, 删除多行
        xids = request.form.get('xids')
        xids = [int(i) for i in xids.split(',') if i and i.isdigit() ]
        aa=db.session.query(db_Staff).filter(db_Staff.id.in_ (xids) ).update({'flag':0}, synchronize_session=False)
        db.session.commit ()
        app.logger.info ('user(%s) delete %d staff records, id list is %s' % (get_user(), aa, xids))
        return tojson({'msg':u'成功删除%d条数据' % aa})