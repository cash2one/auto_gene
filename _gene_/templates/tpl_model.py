#encoding:utf-8

from db import DB


{% for table in tables %}
class {{ table.name.capitalize() }} (DB):
    def __init__ (self, table_name):
        DB.__init__(self, table_name)
{% endfor %}
        

{% for table in tables %}
{{ table.name.lower() }} = {{ table.name.capitalize() }}('{{ table.name }}')
{% endfor %}


if __name__=="__main__":
    pass
