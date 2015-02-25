#encoding:utf-8
from common_import import *

def md5 (s):
    return hashlib.md5(s).hexdigest()

def tojson (data):
    return json.dumps (data)

def get_parameter (*p):
    result = {}
    for i in p:
        result[i] = request.form.get(i,'')
    return result

def get_site_info ():
    site_info = {}
    return site_info

site = get_site_info()

def default_error (msg):
    return render_template ('admin/default_error.html', msg=msg)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_login' not in session:
            return redirect(config.login_url)
        return f(*args, **kwargs)
    return decorated
from model.model_cms import User as db_User
from model.model_cms import Book as db_Book
from model.model_cms import Author as db_Author
from model.model_cms import Category as db_Category

from admin_user import *
from admin_book import *
from admin_author import *
from admin_category import *

