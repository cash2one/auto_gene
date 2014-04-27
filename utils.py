#encoding:utf-8

def excel_to_list (filename, sheets=[], skip_header=1, header_as_key=False):
    '''
    读取excel文件，将其转换为list 返回
    读取excel文件，返回一个或多个列表（一个sheet对应一个列表），每个列表相当于一个table
    '''
    import xlrd
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
    
    data = xlrd.open_workbook(filename)
    result = None
    if not sheets:
        result = sheet_to_table (data.sheets()[0])    #取第一个sheet
    else:
        result = []
        for sheet in sheets:
             result.append ( sheet_to_table (data.sheet_by_name(sheet)) )
    return result

if __name__ == "__main__":
    temp = excel_to_list ('temp/schema.xlsx', ['admin','table','default_fields'], 1, True)
    
    print temp[0]