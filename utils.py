"""
Author: sunhanwu
date: 2020-12-08
"""
import pandas as pd
import requests
def load_alexa_domains(paths):
    """
    加载alexa 域名数据
    :param paths: 数据文件位置
    :return: 返回域名(str)组成的列表，[domain1, domain2, ...]
    """
    try:
        if not isinstance(paths, list):
            paths = [paths]
        result = []
        for path in paths:
            data = pd.read_csv(path, header=None)
            result += data[1].tolist()
        result = list(set(result))
        return result
    except:
        return []

def request_domain(url, domain):
    """
    构造query请求
    :param url: 子节点的url
    :param domain: 查询的域名
    :return: 查询结果，字典结构 {'cname': cname, 'a':a}
    """
    try:
        response = requests.get(url + '?domain={}'.format(domain))
        if response.status_code != 200:
            return {}
        result = response.text
        result = eval(result)
        return result
    except Exception as e:
        print("request {} fail, info:".format(url, e))
        return {}


if __name__ == '__main__':
    url = 'http://www.sunhanwu.top:6009/query'
    result = request_domain(url=url, domain='www.sunhanwu.top')
    print(result)