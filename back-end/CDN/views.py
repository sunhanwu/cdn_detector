# from  CDN.models import CDN_urls
from django.http import JsonResponse
# 增加对分页的支持
import sys
sys.path.append("../..")
import json
from database.database_sql import operation
from database.database import session
#from sqlalchemy.ext.declarative import declarative_base
sys.path.append("..")
from . import Server_communication

def listorders(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    # GET请求 参数在url中，同过request 对象的 GET属性获取
    if request.method == 'GET':
        request = request.GET
    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST', 'PUT', 'DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request = json.loads(request.body)

    # 根据不同的action分派给不同的函数进行处理
    action = request.get("domain",None)
    if action:
        return listcustomers(request,action)
    else:
        return JsonResponse({'ret': 0, 'msg': '不支持该类型http请求'})


def listcustomers(request,domain):
    # 数据库连接初始化
    op = operation(session)
    if op.is_exist(domain):
        pass
    else:
        result = Server_communication.multi_request_domain(domain)
        op.op_add(result)
    #查找该域名以及底下的CDN
    lists=op.op_select(domain)
    return JsonResponse({'ret': 0, 'retlist': lists})


