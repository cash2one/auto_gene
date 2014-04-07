#encoding:utf-8
import web

import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etc.conf import db
db1 = web.database(dbn= db['type'], db= db['name'], user=db['user'], pw=db['pawd'])


class DB :
    TABLE = ''
    def __init__ (self, table_name):
        self.TABLE = table_name
    
    def _where (self, myvar):
        cond = []
        for k in myvar.keys():
            cond.append( ' %s=$%s ' % (k,k) )
        where = 'and'.join(cond)
        return myvar, where
    
    def add (self, **info):
        return db1.insert (self.TABLE, **info)
        
    def get_amount (self, **myvar):
        tmp = self.get_many(0, 10000000000000, '', **myvar)
        return tmp.__len__()
        
        
    def exists (self, **myvar):
        if self.get_amount(**myvar) > 0:
            return True
        return False 
        
    def get_one (self, **myvar):
        temp = self.get_many(0,1, **myvar)
        if not temp:
            return None
        return list(temp)[0]
        
    def get_all (self, order =''):
        if order :
            return db1.select (self.TABLE, order=order)
        else:
            return db1.select (self.TABLE)
        
    def get_many (self, index, length, order = '', **myvar):
        myvar[1] = 1
        myvar, where = self._where (myvar)
        if order :
            result = db1.select (self.TABLE, myvar, where=where, order=order, limit=length, offset=index)
        else:
            result = db1.select (self.TABLE, myvar, where=where, limit=length, offset=index)
        if not result:
            return []
        else:
            return result
        
    def get_list (self, index, length, order='', **myvar):
        data   = self.get_many (index, length, order, **myvar)
        amount = self.get_amount(**myvar)
        return amount, data
        
    def delete (self, **myvar):
        if not myvar:
            print 'Delete Fail ,try to delete from %s without any filter condition'  % (self.TABLE)
            return None
        myvar,where = self._where (myvar)
        temp = db1.delete (self.TABLE, where = where, vars = myvar, _test=True)
        return temp
    
    '''
    def clear (self):
        return db1.delete (self.TABLE, _where = "1=1")
    '''
    
    
    def update (self, keyname, **values):
        where = "%s=$%s" % (keyname, keyname)
        myvar = {}
        myvar[keyname] = values[keyname]
        
        values.pop (keyname)
        return db1.update (self.TABLE, where , vars=myvar, **values)
        
    
    def upsert (self,keyname, **myvar):
        #update or insert
        if myvar[keyname] == 0:
            myvar.pop(keyname)
            return self.add (**myvar)
        else:
            return self.update (keyname, **myvar)
        
    
if __name__ == "__main__":

    #test case
    db = DB ('user')
    #print db.clear()
    print db.add (**{"name":"michael"})
    print db.add (**{"name":"xxxxxxx"})
    print db.get_one (**{'name':'michael'})
    print list(db.get_all())
    print db.get_many (0,1, **{'name':'michael'})
    print db.exists (**{'name':'michael','id':94})
    print db.exists (**{'name':'perter'})
    print db.get_amount ()
    print db.get_amount (**{'name':'michael'})
    
    print db.get_amount()
    print db.delete (**{'name':'michael'})
    print db.get_amount()
    print list(db.get_all())
    
    print db.update("id", **{'name':'yyyy', 'id':95})
    print list(db.get_all())
    
    print db.upsert ("id", **{'name':'zzzz', 'id':0})
    print db.upsert ("id", **{'name':'zzzz', 'id':95})
    print list(db.get_all())
    print 'Done'
    
        