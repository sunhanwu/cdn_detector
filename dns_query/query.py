import dns.resolver
import os


def dns_query(doname, type, server):
    """
    dns查询函数
    :param doname: 待查询的域名
    :param type: 域名类型
    :param server: 指定的DNS递归服务器
    :return: 如果是A类型的话，返回对应IP， 如果是CNAME类型的话返回对应的域名
    """
    try:
        result = dns.resolver(doname, type)


