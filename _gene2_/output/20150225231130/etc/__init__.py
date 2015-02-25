#encoding:utf8

run_env = "dev"    #开发环境, 不同环境对应相应的的目录
#run_env = "test"  #测试环境
#run_env = "prod"  #生产环境

if run_env == "dev":
    from dev.env_config import *
    from dev.site_config import *

elif run_env == "prod":
    from prod.env_config import *
    from prod.site_config import *

elif run_env == "test":
    from test.env_config import *
    from test.site_config import *
    
else:
    raise Exception ("Import Environment config file error, unknown run environment:%s" % run_env)