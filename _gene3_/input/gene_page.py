#encoding:utf8

import os
import re
import sys
import shutil
import pymysql

reload(sys)  
sys.setdefaultencoding("utf-8")

from jinja2 import Template

num_per_page = 20  #number of articles in one list page
num_per_page_ar = 50  #number of articles in one archieve page

def write_file (filename, content):
    dirname = os.path.split(filename)[0]
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    
    content = content.encode('utf8')
    w = open(filename, 'w')
    w.write(content)
    w.close()
 
def gene () :
    tpl = open("detail.html").read()
    html_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'html')
    conn = pymysql.connect(host='127.0.0.1', port=3306,user='root',passwd='1234', db='blog', charset='utf8')  
    cur = conn.cursor()  
    cur.execute("SELECT * FROM article order by time desc limit 1000") 
    records = [] 
    for r in cur:  
        #print("row_number:"+str(cur.rownumber))  
        post_id = re.findall(r'\d+', r[1])[0]
        created = str(r[4])[:7]
        data = {}
        data['content'] = r[0]
        data['source']  = r[1]
        data['link']    = '/html/%s/%s.html' % (created, str(post_id))
        data['title'] = r[2]
        data['image'] = r[3]
        data['time']  = str(r[4])[:-3]
        data['summary'] = r[5]
        filename = os.path.join(html_dir, created, str(post_id)+".html")
        content  = Template (tpl).render(data=data)
        write_file (filename, content)
        records.append (data)
    
    for i in range(0, len(records)+1, num_per_page_ar):
        page     = i/num_per_page_ar
        fielname = os.path.join(html_dir, 'archieve', 'archieves_%s.html' % page)
        content  = Template(open('archieves.html').read()).render(records=records[i:i+num_per_page_ar], index=page, has_more=len(records) > i+num_per_page_ar )
        write_file (fielname, content)
    
    for i in range(0, len(records)+1, num_per_page):
        page     = i/num_per_page
        fielname = os.path.join(html_dir, 'list', 'list_%s.html' % page)
        content  = Template(open('list.html').read()).render(records=records[i:i+num_per_page], index=page, has_more=len(records) > i+num_per_page )
        write_file (fielname, content)
    
    #gene the index.html home page 
    shutil.copy(os.path.join(html_dir, 'list/list_0.html'), os.path.join(html_dir, 'index.html'))
    shutil.copy(os.path.join(html_dir, 'list/list_0.html'), os.path.join(os.path.dirname(html_dir), 'index.html'))
    cur.close()  
    conn.close()  


if __name__ == "__main__":
    gene()
    print 'Done'



