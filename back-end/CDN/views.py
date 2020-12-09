from django.shortcuts import render
# from  CDN.models import CDN_urls
from django.http import HttpResponse
from django.http import JsonResponse
# 增加对分页的支持
from django.core.paginator import Paginator, EmptyPage
import sys
sys.path.append("../..")
import utils
import config
import json
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
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


def listcustomers(request,domain):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = Customer.objects.values()

    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(qs)

    return JsonResponse({'ret': 0, 'retlist': retlist})


