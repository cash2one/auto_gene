#encoding:utf-8
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import web

from etc.conf import db
db1 = web.database(dbn= db['type'], db= db['name'], user=db['user'], pw=db['pawd'])


class DB :
    TABLE = ''
    def __init__ (self, table_name):
        self.TABLE = table_name
    
    def _where (self, myvar):
        if not myvar:
            return {},' 1=1 '
        cond = []
        for k in myvar.keys():
            cond.append( ' %s=$%s ' % (k,k) )
        where = 'and'.join(cond)
        return myvar, where
    
    def add (self, **info):
        new_info = {}
        for k,v in info.iteritems():
            if len(str(v).strip()) > 0:
                new_info[k] = v
        return db1.insert (self.TABLE, **new_info)
        
    def get_amount (self, **myvar):
        myvar, where = self._where(myvar)
        sql = "select count(*) as amount from %s where %s" % (self.TABLE, where)
        tmp = db1.query (sql, vars=myvar)
        if tmp:
            return tmp[0]['amount']
        return 0
        
        
    def exists (self, **myvar):
        if self.get_amount(**myvar) > 0:
            return True
        return False 
        
    def get_one (self, **myvar):
        temp = self.get_many(0,1, **myvar)
        if not temp:
            return {}
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
        temp = db1.delete (self.TABLE, where = where, vars = myvar)
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
        print 'try to upsert record into database , key:%s,  data:%s' % (keyname, myvar)
        if int(myvar.get(keyname) or 0) == 0:
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
    
        