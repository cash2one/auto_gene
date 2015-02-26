#encoding:utf8

login_url = '/admin/login'

#用户权限说明
user_role = {
    'admin':1, #系统管理员
    'user': 2, #普通用户，只可以在前台使用
}
    
#交易状态
tran_status = {
    'finish': 1,  #交易完成
    'unpay':  2,  #等待支付
    'paying': 3,  #正在支付
}

#分页的设置，限制最大的查询记录数
page = {
    'page_records':10,        #默认查询一次的记录数
    'page_records_max':100,   #默认查询一次的最大记录数
}

#禁止使用的密码
deny_password = "******"