import sys
sys.path.append("../")
from utils.utils import request_domain
from utils.utils import logger_commucination as logger
import multiprocessing
import time
import pandas as pd
from database.database_sql import operation
from database.database import session
from sqlalchemy.ext.declarative import declarative_base
from utils.config import node_info      # TODO
from utils.utils import getRandomNameServer
import ipdb

Base = declarative_base()


# 多台服务器并行查找
def multi_request_domain(domain):
    try:
        start_time = time.time()
        totalCnameList = []
        totalAList = []
        host_list = [
            ['node1', node_info['node1']['deploy']['port']],
            ['node2', node_info['node2']['deploy']['port']],
            ['node3', node_info['node3']['proxy']['proxy_port']],
            ['node4', node_info['node4']['deploy']['port']]
        ]
        randomNameServer1 = getRandomNameServer()
        randomNameServer2 = getRandomNameServer()
        randomNameServer3 = getRandomNameServer()
        randomNameServer4 = getRandomNameServer()
        url_list = ['http://{host}.sunhanwu.top:{port}/query'.format(host=i[0], port=i[1]) for i in host_list]
        url_nameserver_list = zip(url_list, [randomNameServer1, randomNameServer2, randomNameServer3, randomNameServer4])
        pool = multiprocessing.Pool(processes=4)
        jobs = []
        for url, nameserver in url_nameserver_list:
            job = pool.apply_async(request_domain, args=(url, domain, nameserver))
            jobs.append(job)
        pool.close()
        pool.join()
        for host_job in jobs:
            host_result = host_job.get()
            if host_result.get("a") or host_result.get("cname"):
                totalCnameList += host_result["cname"]
                totalAList += host_result["a"]
        return {"cname": totalCnameList, "a": totalAList}
    except Exception as e:
        ipdb.set_trace()
        logger.error("multi_request_domain error: {}".format(e))
        return {'cname':[], 'a':[]}
    finally:
        logger.info("{},完成时间time:{time}".format(domain, time=time.time() - start_time))

def multi_request_domain_pool(domains:list, jobs=1):
    """
    多线程请求multi_request_domain
    :param domains: list， 多个域名组成的列表
    :return: 字典结构，{'cname': [], 'a':[]}
    """
    try:
        pool = multiprocessing.Pool(processes=jobs)
        results = []
        cname = []
        a = []
        for domain in domains:
            result = pool.apply_async(multi_request_domain, args=(domain, ))
            results.append(result)
        pool.close()
        pool.join()
        for result in results:
            cname += result.get()['cname']
            a += result.get()['a']
        return {'cname':cname, 'a':a}
    except Exception as e:
        logger.error("multi_request_domain_pool error, {}".format(e))
        return {'cname':[], 'a':[]}



if __name__ == '__main__':
    data_path = "../data/top-1m-12-08.csv"
    domain_list = pd.read_csv(data_path, header=None, encoding="utf-8")
    # 数据库连接初始化
    op = operation(session)
    for index in range(0, len(domain_list)):
        domain = domain_list.iloc[index, 1]
        # for domain in domain_group:
        #     if op.is_exist(domain):
        #         domain_group.remove(domain)
        # domain_group_result = multi_request_domain_pool(domain_group)
        result = multi_request_domain(domain)
        op.op_add(result)

