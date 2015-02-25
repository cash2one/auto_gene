#encoding:utf8
import os
import sys
import time
import shutil
import datetime

from jinja2 import Template

'''
这是基于Flask 自动生成的后台管理模板的项目
输入自定义 model, 生成其他的 controller和view
生成的代码放到output目录
'''

def write_file (filename, content):
    #生成文件
    dirname = os.path.split(filename)[0]
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    
    content = content.encode('utf8')
    w = open(filename, 'w')
    w.write(content)
    w.close()
    
def output_folder (path='output'):
    created = (datetime.datetime.now()).strftime("%Y%m%d%H%M%S")
    return os.path.join(path, created)
    
    
def extract_info (module):
    result = {}
    result['name'] = getattr(module,'_name','')
    result['url']  = getattr(module,'_url','')
    result['title']= getattr(module,'_title','')
    result['dbNa'] = getattr(module,'_dbop''')
    
    model_info = []
    table = module
    for j in dir(table):
        if str(j).startswith('_'):
            continue
        field = getattr(table, j)
        field_type = getattr(getattr(table, j), 'type', None)
        if field_type:
            remark = getattr(getattr(table, j), 'info', '')
            is_pk  = False
            if remark.startswith('*'):
                is_pk = True
                remark = remark[1:]
            if '-' in remark:
                order, desc = remark.split('-',1)
                #model_info.append ( [j,field_type, remark, int(order), desc, is_pk] )
                model_info.append ({'name':j, 'type':field_type, 'title': desc, 'remark':remark, 'order':int(order), 'primary':is_pk})
                       
    #result['fields'] = sorted (model_info, key=lambda x:x[3])
    result['fields'] = sorted (model_info, key=lambda x:x['order'])
    return result
    
def gene_html (obj, tpl_list, tpl_edit) :
    #生成template中的html文件
    def gene_edit ():
        data = obj
        content = Template (file(tpl_edit).read()).render(data = data)
        file_path = os.path.join(dir_path, 'templates/admin', '%s_edit.html' % obj['name'])
        write_file (file_path, content)
    
    def gene_list ():
        data = obj
        content = Template (file(tpl_list).read()).render(data=data)
        file_path = os.path.join(dir_path, 'templates/admin', '%s_list.html' % obj['name'])
        write_file (file_path, content)
        
    
    gene_list ()
    gene_edit()

def gene_py(obj, tpl_py):
    #生成 controller python文件
    content = Template(file(tpl_py).read()).render(data=obj)
    file_path = os.path.join(dir_path, 'controller', 'admin_%s.py' % obj['name'])
    write_file (file_path, content)

def gene_menu (project_name, objs, tpl):
    #后台管理的菜单页
    data = {}
    data['project_name'] = project_name
    data['menus'] = []
    admin_import = ''
    common_import = ''
    for obj in objs:
        obj_name = str(obj).split('.')[-1].split("'")[0]
        data['menus'].append ([obj._title, obj._url, obj._name])
        admin_import += 'from admin_%s import *\n' % obj._name
        common_import += 'from model.model_cms import %s as db_%s\n' % (obj_name, obj_name)
    content = Template (file(tpl).read()).render(data=data)
    file_path = os.path.join(dir_path, tpl.replace('input/',''))
    write_file (file_path, content)
    
    w = open(os.path.join(dir_path, 'controller', 'common_import.py'), 'a')
    w.write('\n' + admin_import + '\n' + common_import + '\n')
    w.close()

def gene_static ():
    
    dirs = [
            {'input_path':'input/etc', 'output_path': 'etc'},
            {'input_path':'input/scripts', 'output_path': 'scripts'},
            {'input_path':'input/tools', 'output_path': 'tools'},
            {'input_path':'input/model', 'output_path': 'model'},
            {'input_path':'input/templates', 'output_path': 'templates'},
            {'input_path':'input/static', 'output_path': 'static'},
            {'input_path':'input/controller', 'output_path':'controller'}
            ]
    for i in dirs:
        shutil.copytree(i['input_path'], os.path.join(dir_path, i['output_path']))
    
    files = [
            {'input_path':'input/myapp.py', 'output_path':'myapp.py'},
            {'input_path':'input/controller/admin.py', 'output_path':'controller/admin.py'},
            {'input_path':'input/controller/__init__.py', 'output_path':'controller/__init__.py'},
            ]
    
    for i in files:
        content = file(i['input_path']).read()
        file_path = os.path.join(dir_path, i['output_path'])
        write_file (file_path, content)

if __name__ == "__main__":
    dir_path = output_folder()
    gene_static ()
    from input.model.model_cms import User, Book , Author, Category
    db_models = (User, Book , Author, Category)
    for tmp in db_models:
        temp = extract_info(tmp)
        gene_html(temp, 'input/view/user_list.html', 'input/view/user_edit.html')
        gene_py  (temp, 'input/controller/user.py')
    
    gene_menu (u'图书管理系统', db_models, 'input/templates/admin/index.html')
    
    print "Done"
