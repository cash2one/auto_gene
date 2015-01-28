#encoding:utf-8
'''
dependence :  xlrd, jinja2 
'''
import os

def write_file (filename, content):
    dirname = os.path.split(filename)[0]
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    
    content = content.encode('utf8')
    w = open(filename, 'w')
    w.write(content)
    w.close()
    
def render(template_name, **context):
    '''
    render page with jinja2 template
    '''
    from jinja2 import Environment,FileSystemLoader
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
            extensions=extensions,
            )
    jinja_env.globals.update(globals)

    #jinja_env.update_template_context(context)
    return jinja_env.get_template(template_name).render(context)

def replace_template (content):
    content = content.replace ('#{', '{{')
    content = content.replace ('}#', '}}')
    content = content.replace ('#%', '{%')
    content = content.replace ('%#', '%}')
    return content

def excel_to_list (filename, sheets=[], skip_header=1, header_as_key=False):
    import xlrd
    #读取excel文件，返回一个或多个列表（一个sheet对应一个列表），每个列表相当于一个table
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
    
    data = xlrd.open_workbook (filename)
    result = None
    if not sheets:
        #取第一个sheet
        result = sheet_to_table (data.sheets()[0])
    else:
        result = []
        for sheet in sheets:
             result.append ( sheet_to_table (data.sheet_by_name(sheet)) )
    return result
    
def gene_sql (tables):
    '''
    generate the create table sql 
    '''
    
    for table in tables:
        sql = 'create table %s ('  %  table['name']
        tmp = []
        fk  = []
        for field in (table['fields']):
            line = ' %s %s %s %s'   % (field.get('field'), field.get('type'),  \
                                       ('null' if field.get('null')=='y' else 'not null' ),  \
                                       ('' if not field.get('default') else 'default '+ field.get('default'))) 
            if field.get('unique'):
                line += ' unique '
            if field.get('PK'):
                line += ' primary key auto_increment '
            if field.get('FK'):
                fk.append (' foreign key(%s) REFERENCES %s(id)' % (field.get('field'), field.get('FK')))
            tmp.append (line)
        sql += ','.join(fk+tmp) + ' ) default character set utf8;  '
        print sql
        
    print '-----end sql ----'
    print '-----------------'
    
def gene_url (data):
    
    content = ''
    for item in data:
        content += '#--------------%s -----------\n'  % item['name']
        content += '#----%s----\n'  % item['remark']
        content += '"/admin/%s_list",            "controller.admin.%s.%s_list",\n'   % (item['name'], item['name'], item['name'])
        content += '"/admin/%s_read/(\d+)",      "controller.admin.%s.%s_read",\n'   % (item['name'], item['name'], item['name'])
        content += '"/admin/%s_edit/(\d+)",      "controller.admin.%s.%s_edit",\n'   % (item['name'], item['name'], item['name'])
        content += '"/admin/%s_delete/(\d+)",    "controller.admin.%s.%s_delete",\n' % (item['name'], item['name'], item['name'])
        content += '#--------------end %s -------\n\n'  % item['name']
    
    content = render ('urls.py', admin_url=content)
    write_file ('../urls.py', content)

def gene_model (tables):
    content = render ('tpl_model.py', tables=tables)
    write_file ('../model/tables.py', content)
    
def gene_view (data):
    if not data:
        return 
    content = render ('tpl_view.py', item=data)
    write_file ('../controller/admin/'+data['name']+'.py', content)

def gene_read (data):
    content = render ('tpl_read.html', item=data)
    write_file ('../templates/admin/'+data['name']+'_read.html', replace_template(content) )

def gene_edit (data):
    content = render ('tpl_edit.html', item=data)
    write_file ('../templates/admin/'+data['name']+'_edit.html', replace_template(content) )
            
def gene_list (data):
    content = render ('tpl_list.html', item=data)
    write_file ('../templates/admin/'+data['name']+'_list.html', replace_template(content) )
      
def gene_admin_index (data):
    content = render ('tpl_admin.html', data=data)
    write_file ('../templates/admin/admin.html', replace_template(content))
  
def filter_comment_lines (lines, key, value):
    result = []
    for line in lines:
        if line.get(key,'').startswith( value ):
            continue
        result.append (line)
    return result
    

def fields (data, default_fields):
    tables = []
    for line in data:
        tmp = line.pop('table_name').strip()
        if not tmp or tmp.startswith('#'):
            continue
        
        for table in tables:
            if tmp == table.get('name'):
                table['fields'].append (line)
                break
        else:
            #this else will run if not trigger "break"
            tables.append ( {'name':tmp, 'fields':[line,]} )
        
    for table in tables:
        table['fields'].extend (default_fields)
        
    for table in tables:
        for field in table['fields']:
            remark = field['comment'] 
            if '{' in remark and '}' in remark:
                tmp = remark.replace('{','').replace('}','')
                if ',' in tmp:
                    tmp2 = tmp.split(',')
                elif u'，' in tmp:
                    tmp2 = tmp.split(u'，')
                options = []
                for tmp3 in tmp2:
                    tmp4 = tmp3.split('-',1)
                    tmp5 = "#% if value== '" + tmp4[0] + "' %# selected #% endif %#" 
                    options.append ( '<option value="%s" %s >%s</option>' % (tmp4[0], tmp5, tmp4[1]))   
                field['show_type'] = 'options'
                field['options']   = '\n'.join (options)   
                field['options_dict'] = dict ( [ (tmp6.split('-',1)[0], tmp6.split('-',1)[1]) for tmp6 in tmp2 ] )   
            elif field['type'] in ['datetime','date']:
                field['show_type'] = 'date'
            elif field['type'] in ['tinyint','int','integer']:
                field['show_type'] = 'number'
            elif field['type'] in ['text', 'mediumtext', 'longtext']:
                print field
                field['show_type'] = 'textarea'
            else:
                field['show_type'] = 'text'
                
    return tables
        
if __name__ == "__main__":
    page, table, default_field = excel_to_list ("./templates/schema.xlsx", ['admin', 'table', 'default_fields'], 1, True)
    page  = filter_comment_lines (page, 'name', '#')
    table = filter_comment_lines (table,'table_name', '#')
    
    tables = fields (table, default_field)   #{'name': 'user', 'fields': ['field': 'name', 'type':'int',...]}
    gene_sql (tables)
    gene_model (tables)
    
    for item in page:
        item['url'] = '/admin/%s'  % item['name']
        for table in tables:
            if table['name'] == item['name']:
                item['table'] = table
                break
        else:
            raise ("not found defination of table %s" % item['name'] )
    
    for item in page:
        gene_view (item)
        gene_read (item)
        gene_list (item)
        gene_edit (item)
        
    gene_admin_index (page)
    gene_url (page)
    
