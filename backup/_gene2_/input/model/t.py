#encoding:utf8

import model_cms


def extract_info (module):
    model_info = []
    for i in dir(module):
        tmp = getattr(getattr(module, i, None), '__class__', None)
        if str(tmp) == "<class 'flask_sqlalchemy._BoundDeclarativeMeta'>":
            table = getattr(module, i)
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
                        model_info.append ( [i,j,field_type, remark, int(order), desc, is_pk] )
                        
    return sorted (model_info, key=lambda x:x[4])


                    

    
if __name__ == "__main__":
    print extract_info (model_cms)

