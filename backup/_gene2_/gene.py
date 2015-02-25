#encoding:utf8
import os
import sys
import time
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
                model_info.append ( [j,field_type, remark, int(order), desc, is_pk] )
                       
    result['fields'] = sorted (model_info, key=lambda x:x[3])
    return result
    
def gene_html (obj, tpl_list, tpl_edit) :
    #生成template中的html文件
    def gene_edit ():
        data = obj
        content = Template (file(tpl_edit).read()).render(data = data)
        file_path = os.path.join(dir_path, 'templates', '%s_edit.html' % obj['name'])
        write_file (file_path, content)
    
    def gene_list ():
        data = obj
        content = Template (file(tpl_list).read()).render(data=data)
        file_path = os.path.join(dir_path, 'templates', '%s_list.html' % obj['name'])
        write_file (file_path, content)
        
    
    gene_list ()
    gene_edit()

def gene_py(obj, tpl_py):
    #生成 controller python文件
    content = Template(file(tpl_py).read()).render(data=obj)
    file_path = os.path.join(dir_path, 'controller', 'admin_%s.py' % obj['name'])
    write_file (file_path, content)

def gene_static ():
    files = [
            {'input_path':'input/model/user.py', 'output_path':'model/user.py'},
            {'input_path':'input/model/user.py', 'output_path':'model/user.py'},
            ]
    
    for i in files:
        content = file(i['input_path']).read()
        file_path = os.path.join(dir_path, i['output_path'])
        write_file (file_path, content)

if __name__ == "__main__":
    from input.model.model_cms import User
    user = extract_info(User)
    dir_path = output_folder()
    gene_html(user, 'input/view/user_list.html', 'input/view/user_edit.html')
    gene_py  (user, 'input/controller/user.py')
    
    gene_static ()
    print "Done"
