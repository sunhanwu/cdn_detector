"""
Author: sunhanwu
date: 2020-12-08
"""
import pandas as pd
import requests
import logging
import logging.handlers
from utils.config import log_path
import os
from utils.config import serverNames
import random


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

def request_domain(url, domain, nameserver:list=None, proxy=False):
    """
    构造query请求
    :param url: 子节点的url
    :param domain: 查询的域名
    :return: 查询结果，字典结构 {'cname': cname, 'a':a}
    """
    try:
        response = requests.get(url + '?domain={}&nameserver1={}&nameserver2={}&nameserver3={}&nameserver4={}&nameserver5={}'.format(domain, nameserver[0],nameserver[1],nameserver[2],nameserver[3],nameserver[4]))
        if response.status_code != 200:
            return {}
        result = response.text
        result = eval(result)
        return result
    except Exception as e:
        print("request {} fail, info:{}".format(url, e))
        return {}

def getRandomNameServer():
    """
    随机返回一个
    :return:
    """
    nameServerIPS = list(serverNames.values())
    random_indexs = random.sample(range(0, 16), 5)
    return [nameServerIPS[x] for x in random_indexs]


def log(name):
    logger = logging.getLogger("cdn_detector-{}".format(name))
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    file_handler = logging.handlers.RotatingFileHandler(os.path.join(log_path, '{}-log.txt'.format(name)), \
                                                        maxBytes = 5 * 1024 * 1024,backupCount=10, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger

logger_commucination = log('commucination')
logger_dnsquery = log('dns-query')
logger_database = log('database')
logger_clawer = log('clawer')
logger_django = log("django")
logger_neo4j = log("neo4j")



if __name__ == '__main__':
    url = 'http://www.sunhanwu.top:6009/query'
    result = request_domain(url=url, domain='www.sunhanwu.top')
    print(result)
