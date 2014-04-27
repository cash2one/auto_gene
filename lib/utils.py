#encoding:utf-8
import os
import math
import urlparse

import web
from jinja2 import Environment,FileSystemLoader

session = web.config._session

def render(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')),
            extensions=extensions,
            )
    jinja_env.globals.update(globals)

    #jinja_env.update_template_context(context)
    return jinja_env.get_template(template_name).render(context)

def next_page (index, length, total):
    if index < 0:
        index = 0
    
    param = urlparse.urlparse( web.ctx.fullpath )
    url = param[2] + '?'
    for i in param[4].split('&'):
        if i.startswith('__index=') or i.startswith('__length='):
            continue
        url += i + '&'
        
    template = "&__index=%d&__length=%d"
    first = url + template % (0, length)
    pref  = url + template % (index-length, length)
    #curr  = url + template % (index, length)
    next  = url + template % (index+length, length)
    last  = url + template % (total - total%length, length)
    
    line = "<div style='margin-top:20px; margin-right:10px; float:right;' id='data_list_next' >"
    if index<=0:
        line += '<a class="button small disabled">首页</a>'
        line += '<a class="button small disabled">上一页</a>'
    else:
        line += '<a class="button small" href="%s" >首页</a>'    %  (first)
        line += '<a class="button small" href="%s" >上一页</a>'  %  (pref)
        
    line += '<a class="button small" >%d</a>'  %  (index/length+1)
    
    if index + length >= total:
        line += '<a class="button small disabled" >下一页</a>'
        line += '<a class="button small disabled" >尾页</a>'
    else:
        line += '<a class="button small" href="%s" >下一页</a>'  % (next)
        line += '<a class="button small" href="%s" >尾页</a>'    % (last)
    
    line += '<a style="color:#A87858;">共%d页</a>'  %  (int((total-1)/length) + 1)
    
    return line

def user_login(f, *args):
    def new_f(*args):
        if session.get('user_id') is None:
            raise web.seeother("/login/")
        else:
            return f(*args)
    return new_f

def admin_login(f, *args):
    def new_f(*args):
        if session.get('admin') is None:
            raise web.seeother("/admin/login")
        else:
            return f(*args)
    return new_f


def excel_to_list (filename, sheets=[], skip_header=1, header_as_key=False):
    '''
    读取excel文件，将其转换为list 返回
    读取excel文件，返回一个或多个列表（一个sheet对应一个列表），每个列表相当于一个table
    '''
    import xlrd
    def sheet_to_table (table):
        def value (r,c):
            return str(table.cell(r,c).value).strip()
        
        nrows = table.nrows
        ncols = table.ncols
        temp  = []
        for i in range(skip_header, nrows):
            line = None
            if not header_as_key :
                line = []
                for j in range(0, ncols):
                     line.append ( value(i,j) )
            else:
                line = {}
                for j in range(0, ncols):
                    line[value(0,j)] = value(i,j)
            temp.append (line)
        return temp
    
    data = xlrd.open_workbook(filename)
    result = None
    if not sheets:
        result = sheet_to_table (data.sheets()[0])    #取第一个sheet
    else:
        result = []
        for sheet in sheets:
             result.append ( sheet_to_table (data.sheet_by_name(sheet)) )
    return result

if __name__ == "__main__":
    temp = excel_to_list ('temp/schema.xlsx', ['admin','table','default_fields'], 1, True)
    
    print temp[0]