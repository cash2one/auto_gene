#encoding:utf8

import math

def list_to_dict (data, k, v):
    # convert a list to dict
    tmp = {}
    for item in data:
        kk = getattr(item, k)
        vv = getattr(item, v)
        tmp[kk] = vv
    return tmp

def pagination (cur_page, amount, length, make_url, make_jump):
    max_page = int(math.ceil(float(amount)/length))
    # 分页, 前端CSS用Bootstrap
    temp = """<div class="page"><ul>"""
    
    if cur_page == 1:
        temp += '<li><a  class="disabled">首页</a></li>'
        temp += '<li><a  class="disabled">前一页</a></li>'
    else:
        temp += '<li><a href="%s" >首页</a></li>' % (make_url(length,1))
        temp += '<li><a href="%s" >前一页</a></li>' % (make_url(length,cur_page-1))
        
    if cur_page == max_page:
        temp += '%s' + '<li><a class="disabled">后一页</a></li>'
        temp += '<li><a class="disabled">尾页</a></li>'
    else:
        temp += '%s' + '<li><a href="%s">后一页</a></li>' % (make_url(length, cur_page+1))
        temp += '<li><a href="%s">尾页</a></li>' % (make_url(length, max_page))
    temp += "</ul>%s</div>" % make_jump(length, cur_page, amount)
    
    if max_page < 10:
        start = 1
        end = max_page + 1
    else:
        start = cur_page - 3
        end = cur_page + 3 + 1
    tmp = ""
    for i in range(start, end):
        active = ''
        if i==cur_page:
            active = " class='active' "
        tmp += "<li %s ><a href='%s'>%s</a></li>" % (active, make_url(length,i),i) 
    return temp % tmp

def pagination_data (length, index, default_amount=None, max_amount=None):
    # 分页，控制取记录的数目，设置默认的数目和最大数目
    # 防止因为请求的数目太大而卡住系统
    if not str(default_amount).isdigit():
        default_amount = 10
    else:
        default_amount = int(default_amount)
        
    if not str(max_amount).isdigit():
        max_amount = 100
    else:
        max_amount = int(max_amount)
        
    if not length or not length.isdigit():
        length = default_amount
    length = int(length)
    
    if not index or not index.isdigit():
        index = 0
    index = int(index)
        
    if length ==0:
        length = default_amount
    elif length >= max_amount:
        length = max_amount
    offset = (index-1) * length
    
    return length, index, offset