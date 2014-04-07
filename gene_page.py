    #encoding:utf-8

'''  database 
table primary key : id int primary key auto_increment
each record add a field  user_id to tag which user to create it
'''
import os

def replace_template (content, data):
    content = content.decode('utf8')
    for k,v in data.iteritems():

        content = content.replace(  '{{{{'+k+'}}}}',  v )

    return content


def write_file (filename, content):
    dirname = os.path.split(filename)[0]
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    
    content = content.encode('utf8')
    w = open(filename, 'w')
    w.write(content)
    w.close()


def gene_sql(data):

    fields = []
    for item in data.get('fields'):
        t_null = '' if item.get('null').lower().strip()=='y' else 'not null'
        t_default = '' if not item.get('default') else ('default ' + str(item.get('default')))

        temp = '%s %s %s %s'  % (item.get('name'), item.get('type'), t_null, t_default)

        fields.append (temp)
    sql = '''create table %s (%s) ''' % (data.get('table_name'), ','.join(fields))
    return sql

def gene_html (data):

    def load_data ():
        info = {}
        info['title'] = data.get('title')
        info['sub_title'] = data.get('sub_title')
        info['url'] = data.get('url')


        temp1 = ''    #for filter search
        temp2 = ''    #for data show title
        temp3 = ''    #for data show field name
        temp4 = ''    #for add info
        for x in data.get('fields'):
            if x.get('display') == 'n':
                continue
            
            field_type = 'text'
            if x.get('type') == 'date':
                field_type = 'date'
            elif x.get('type') == 'text':
                field_type = 'textarea'
            
            if field_type == 'textarea':
                input_template = "\n<label>%s</label><textarea name='%s' id='%s' rows='6' cols='80'></textarea>"
            else:
                input_template = "\n<label>%s</label><input type='##type##' name='%s' id='%s' value='' >".replace("##type##", field_type)
            input_field = input_template % (x.get('title'), data.get('name') + '_' + x.get('name'), data.get('name') + '_' + x.get('name') )
            
            temp1 +=  input_field

            temp2 += '<th>%s</th>'  % x.get('title')

            temp3 += '<td>{{item.get("%s")}}</td>\n'   %   x.get('name')

            warn_msg = '''<span id="%s_msg"></span>''' % x.get('name')
            temp4 += '\n<div class="item_input">    %s %s\n</div>' % (input_field, warn_msg)

        info['filter_fields'] = temp1
        info['field_names']   = temp2
        info['loop_fields'] = temp3
        info['add_fields']  = temp4
        return info

    def gene_list(data):
        info = load_data()

        template = file('template/tpl_list.html').read()
        content  = replace_template (template, info)

        write_file ('gene/templates/'+data.get('name') + '_list.html', content)

    def gene_edit (data):
        info = load_data()
        template = file('template/tpl_edit.html').read()
        content = replace_template (template, info)
        write_file ('gene/templates/' + data.get('name') + '_edit.html', content)


    gene_list (data)
    gene_edit(data)
    
    gene_py (data)


def gene_py (data):
    def load_data ():
        info = {}
        info['url']  = data.get('url')
        info['name'] = data.get('name')
        info['fields'] = str([ item.get('name') for item in data.get('fields') ])
        return info
    
    info = load_data()

    template = file('template/tpl_view.py').read()
    content  = replace_template (template, info)

    write_file ('gene/controller/'+data.get('name') + '.py', content)
    
    

def gene (data):
    #generate page for one table 
    default_fields = [
            {'name':'id', 'null':'n', 'title':u'主键', 'type':'int primary key auto_increment', 'default':'', 'display':'n'},
            {'name':'create_user_id', 'null':'y', 'title':u'创建用户', 'type':'int', 'default':'', 'display':'n'},
            {'name':'update_user_id', 'null':'y', 'title':u'修改用户', 'type':'int', 'default':'', 'display':'n'},
            {'name':'create_date', 'null':'y', 'title':u'创建时间', 'type':'date', 'default':'', 'display':'n'},
            {'name':'update_date', 'null':'y', 'title':u'修改时间', 'type':'date', 'default':'', 'display':'n'},
    ]
    data['fields'].extend (default_fields)
    
    print gene_sql(data)
    gene_html(data)
    gene_py(data)

def gene_url (item):
    print '"%s_list",            "controller.admin.%s.%s_list",' % (item['url'], item['name'], item['name'])
    print '"%s_read/(\d+)",      "controller.admin.%s.%s_read",' % (item['url'], item['name'], item['name'])
    print '"%s_edit/(\d+)",      "controller.admin.%s.%s_edit",' % (item['url'], item['name'], item['name'])
    print '"%s_delete/(\d+)",    "controller.admin.%s.%s_delete",' % (item['url'], item['name'], item['name'])
    print 
    
if __name__ == "__main__":
    execfile ('template/schema.py')
    for item in data:
        gene (item)
    print 
    for item in data:
        gene_url (item)
    print 'done'
