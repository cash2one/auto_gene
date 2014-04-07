#encoding:utf-8
import os
import math

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

def next_page (index, length, total, url):
    start_page = 0
    end_page = math.ceil (float(total) / length)
    
    first, prev, curr , next, last = [False,] * 5
    if index-length >=0:
        first = True
        prev  = True
        
    if index + length < total:
        next  = True
        last  = True
    
    line = '''
                    <div style='margin-top:20px; margin-right:10px; float:right;'>
                    <a class="button small disabled">首页</a>
                    <a href="" class="button small">上一页</a>
                    <a >3</a>
                    <a href="" class="button small">下一页</a>
                    <a href="" class="button small">尾页</a>
                    <a style="color:#A87858;">共14页</a>
                </div>
            '''
        
    
    pass


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