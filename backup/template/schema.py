#encoding:utf-8

test_item = {
    'name'   :   'user',
    'title'  :  u'用户',
    'sub_title':u'用户',
    'url': '/admin/user',
    'remark':u'集团内部的用户不会外开放使用,员工帐号',
    'table_name': 'user',
    'fields':[
        {'name':'uid',  'null':'n', 'title':u'用户ID',  'type':'varchar(20)',   'default':''},
        {'name':'code', 'null':'n', 'title':u'编号',    'type':'varchar(20)',   'default':''},
        {'name':'name', 'null':'n', 'title':u'姓名',    'type':'varchar(20)',   'default':''},
        {'name':'role', 'null':'n', 'title':u'角色',    'type':'tinyint',       'default':''},
        {'name':'dept', 'null':'y', 'title':u'部门',    'type':'tinyint',       'default':''},   
    ],
}

insp_type = {
    'name'   :   'insp_type',
    'title'  :  u'巡查项目类型',
    'sub_title':u'巡查项目类型',
    'url': '/admin/insp_type',
    'remark':u'',
    'table_name': 'insp_type',
    'fields':[
        {'name':'name', 'null':'n', 'title':u'名字',    'type':'varchar(100)',   'default':''},
        {'name':'ord',  'null':'n', 'title':u'顺序',    'type':'tinyint',        'default':1},
        {'name':'valid','null':'y', 'title':u'是否显示', 'type':'tinyint',       'default':1},   
    ],
}

insp_item = {
    'name'   :   'insp_item',
    'title'  :  u'巡查项目',
    'sub_title':u'巡查项目',
    'url': '/admin/insp_item',
    'remark':u'',
    'table_name': 'insp_item',
    'fields':[
        {'name':'insp_type',    'null':'n', 'title':u'巡查类型',       'type':'int',            'default':''    },
        {'name':'title',        'null':'n', 'title':u'标题',          'type':'varchar(1000)',   'default':''   },
        {'name':'ord',          'null':'n', 'title':u'顺序',          'type':'tinyint',         'default':1    },
        {'name':'valid',        'null':'y', 'title':u'是否显示',      'type':'tinyint',         'default':1     },   
    ],
}

insp_plan = {
    'name'   :   'insp_plan',
    'title'  :  u'巡查计划',
    'sub_title':u'巡查计划',
    'url': '/admin/insp_plan',
    'remark':u'',
    'table_name': 'insp_plan',
    'fields':[
        {'name':'user_id',      'null':'n', 'title':u'巡查员',        'type':'int',             'default':''   },
        {'name':'insp_date',    'null':'n', 'title':u'标题',          'type':'varchar(1000)',   'default':''   },
        {'name':'dept_id',      'null':'n', 'title':u'部门',          'type':'tinyint',         'default':''   },
        {'name':'chain_id',     'null':'n', 'title':u'分店',          'type':'int',             'default':''   },
    ],
}

insp_value = {
    'name'   :   'insp_value',
    'title'  :  u'巡查值',
    'sub_title':u'巡查值',
    'url': '/admin/insp_value',
    'remark':u'',
    'table_name': 'insp_value',
    'fields':[
        {'name':'insp_plan_id',    'null':'n', 'title':u'巡查计划',       'type':'int',             'default':''    },
        {'name':'insp_item_id',    'null':'n', 'title':u'巡查项目',       'type':'int',             'default':''   },
        {'name':'value',           'null':'n', 'title':u'巡查值（是否）',  'type':'tinyint',         'default':''   },
        {'name':'remark',          'null':'n', 'title':u'巡查异常记录',    'type':'varchar(1000)',   'default':''    },
    ],
}

data = [test_item, insp_type, insp_item, insp_plan, insp_value]