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

        temp0 = ''    #for read record ,show all fields
        temp1 = ''    #for filter search
        temp2 = ''    #for data show title
        temp3 = ''    #for data show field name
        temp4 = ''    #for add info
        temp5 = ''    #for check whether empty before sumbit the form
        temp4 += "<input type='hidden' name='%s_id' value='{{data.get('id') or ''}}' >"  % data.get('name')
        for x in data.get('fields'):

            
            if x.get('null') == 'n':
                temp5 += """ '%s_%s', """ % (data.get('name'), x.get('name'))
            
            field_type = 'text'
            if x.get('type') == 'date':
                field_type = 'date'
            elif x.get('type') == 'text':
                field_type = 'textarea'
            
            input_template = "\n\t\t<span style='white-space:nowrap;'><label>%s:</label>"
            if field_type == 'textarea':
                input_template += "<textarea name='%s' id='%s' rows='6' cols='80'></textarea></span>  "
            else:
                input_template += "<input type='##type##' name='%s' id='%s' value='{{ data.get('%s') or '' }}' ></span>  ".replace("##type##", field_type)
            input_field = input_template % (x.get('title'), data.get('name') + '_' + x.get('name'), data.get('name') + '_' + x.get('name') , x.get('name'))
            
            temp0 += "\n\t\t<tr><th>%s</th><td>{{data.get('%s') or '' }}</td></tr>"  % (x.get('title'),  x.get('name'))
            
            if x.get('display') == 'n':
                continue
            
            temp1 +=  input_field

            temp2 += '<th>%s</th>'  % x.get('title')

            temp3 += '<td>{{item.get("%s")}}</td>\n'   %   x.get('name')

            warn_msg = '''<span id="%s_%s_msg"></span>''' % (data.get('name'), x.get('name'))
            temp4 += '\n<div class="item_input">    %s %s\n</div>' % (input_field, warn_msg)

        info['all_fields']    = temp0
        info['filter_fields'] = temp1
        info['field_names']   = temp2
        info['loop_fields']   = temp3
        info['add_fields']    = temp4
        info['check_fields']  = temp5 
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

    def gene_read (data):
        info = load_data()
        template = file ('template/tpl_read.html').read()
        content = replace_template (template, info)
        write_file ('gene/templates/' + data.get('name') + '_read.html', content)
    
    gene_list (data)
    gene_edit(data)
    gene_read(data)
    
    gene_py (data)


def gene_py (data):
    def load_data ():
        info = {}
        info['url']  = data.get('url')
        info['name'] = data.get('name')
        info['fields'] = str([ item.get('name') for item in data.get('fields') ])
        info['input_fields'] = ''              #user input field
        info['fields_not_null'] = ''     #user input field , can't be empty
        for field in data.get('fields'):
            if field.get('display') == 'n' :
                continue
            info['input_fields']  += " '%s_%s', " % (data.get('name'), field.get('name'))
            
            if field.get('null') == 'n':     #can't be empty
                info['fields_not_null'] += " '%s_%s', " % (data.get('name'), field.get('name'))
        return info
    
    info = load_data()
    
    info['schema'] = '\n'.join ( [k + ': ' + v  for k,v in data.iteritems()  if type(v)!=type([]) ] )
    schema =  '\n----------database table-----\n'
    for line in data['fields']:
        line2=sorted(line.iteritems(),key=lambda x:x)
        schema += '\t'.join ( ['%s: %s;  ' % (k,v) for k,v in line2 ])
        schema += '\n'
    info['schema'] += schema

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
