"""
Author: sunhanwu
Date: 2020-12-07
"""
import sys
sys.path.append('../')
import dns.resolver
from utils.config import serverNames, dns_timeout, ip2name
import multiprocessing
from utils.utils import logger_dnsquery as logger

def dns_query_one_server(domain:str, type:str, server:str):
    """
    dns查询函数
    :param doname: 待查询的域名
    :param type: 域名类型
    :param server: 指定的DNS递归服务器
    :return: 如果是A类型的话，返回对应IP， 如果是CNAME类型的话返回对应的域名
    """
    try:
        cnameList = []
        aList = []
        # 实例化一个Resolver
        myResolver = dns.resolver.Resolver()
        # 设置dns查询超时时间
        myResolver.timeout = dns_timeout
        myResolver.lifetime = dns_timeout
        # 设置递归服务器
        myResolver.nameservers = [server]
        # 进行dns请求
        result = myResolver.query(domain, type)
        # 遍历dns响应
        for index, record in enumerate(result.response.answer):
            recordSplited = record.to_text().split(' ')
            if recordSplited[3] == 'CNAME':
                cnameList.append([recordSplited[0], recordSplited[4], index, server])
            elif recordSplited[3] == 'A':
                if '\n' in recordSplited[4]:
                    ip = recordSplited[4].split('\n')[0]
                else:
                    ip = recordSplited[4]
                aList.append([recordSplited[0], ip, index, server])
        return cnameList, aList
    except Exception as e:
        # 如果请求失败则返回
        logger.error("{} query server {} failed!, {}".format(ip2name[server], domain, e))
        return [], []


def dns_query_all_servers(domain: str, nameserver:list=None):
    """
    通过多个递归服务器查询某个域名, 使用多进程并发执行
    :param doname: 域名名称
    :return: CNAME列表和A列表
    """
    try:
        totalCnameList = []
        totalAList = []
        server_ips = list(serverNames.values())
        pool = multiprocessing.Pool(processes=10)
        argsPairs = [(domain, 'A', server_ip) for server_ip in nameserver]
        jobs = []
        for argsPair in argsPairs:
            job = pool.apply_async(dns_query_one_server, args=(argsPair[0], argsPair[1], argsPair[2], ))
            jobs.append(job)
        pool.close()
        pool.join()
        for job_result in jobs:
            cname, a = job_result.get()
            totalCnameList += cname
            totalAList += a
        return totalCnameList, totalAList

    except Exception as e:
        logger.error("{}".format(e))
        return [], []

if __name__ == '__main__':
    dns_query_all_servers('www.baidu.com')
