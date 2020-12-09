# from  CDN.models import CDN_urls
from django.http import HttpResponse
# 增加对分页的支持
import sys
sys.path.append("../..")


def listorders(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    # qs = Customer.objects.values()

    ph = request.GET.get('phone', None)
    retStr = ''
    # 如果有，添加过滤条件
    if ph:
        retStr="dsada"
        # qs = qs.filter(phonenumber=ph)

    # 定义返回字符串
    #
    # for customer in qs:
    #     for name, value in customer.items():
    #         retStr += f'{name} : {value} | '
    #     # <br> 表示换行
    #     retStr += '<br>'

    # HttpResponse,负责返回数据
    return HttpResponse(retStr)


