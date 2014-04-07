#encoding:utf-8

from db import DB

class User (DB):
    def __init__ (self, table_name):
        DB.__init__(self, table_name)
    

user = User('user')

if __name__=="__main__":
    print user.get_amount()