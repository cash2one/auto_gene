#encoding:utf-8

from db import DB



class User (DB):
    def __init__ (self, table_name):
        DB.__init__(self, table_name)

class Area (DB):
    def __init__ (self, table_name):
        DB.__init__(self, table_name)

class Policy_category (DB):
    def __init__ (self, table_name):
        DB.__init__(self, table_name)

class Policy (DB):
    def __init__ (self, table_name):
        DB.__init__(self, table_name)

class Policy_user (DB):
    def __init__ (self, table_name):
        DB.__init__(self, table_name)

        


user = User('user')

area = Area('area')

policy_category = Policy_category('policy_category')

policy = Policy('policy')

policy_user = Policy_user('policy_user')



if __name__=="__main__":
    pass