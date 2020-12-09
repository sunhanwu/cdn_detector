import sys
sys.path.append("..")
from utils import request_domain
from utils import logger
import config
import requests
import multiprocessing
import time
import pandas as pd
from tqdm import tqdm
from database_op import *
# from config import serverNames
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import sessionmaker
# from config import db_config      # TODO
import datetime
Base = declarative_base()

#多台服务器并行查找
def multi_request_domain(domain):
    try:
        totalCnameList = []
        totalAList = []
        host_list = [['node1', '6009'],
                     ['node2', "6010"],
                     ['www', "6009"],
                     ["node4","6009"]]
        url_list = ['http://{host}.sunhanwu.top:{port}/query'.format(host=i[0], port=i[1]) for i in host_list]
        pool = multiprocessing.Pool(processes=3)
        jobs = []
        for url in url_list:
            job = pool.apply_async(request_domain, args=(url,domain))
            jobs.append(job)
        pool.close()
        pool.join()

        for host_job in jobs:
            host_result = host_job.get()
            if host_result.get("a") or host_result.get("cname"):
                totalCnameList +=host_result["cname"]
                totalAList += host_result["a"]
        return {"cname":totalCnameList, "a":totalAList}
    except Exception as e:
        print("{}".format(e))




if __name__ == '__main__':
    data_path="../data/top-1m-12-08.csv"
    domain_list = pd.read_csv(r"C:\Users\Administrator\研究生大作业\域名安全\newrepo\cdn_detector\data\top-1m-12-08.csv", header=None,
                    encoding="utf-8")

    #数据库连接初始化
    engine = create_engine('mysql+pymysql://cdn_user:cdn_123456@www.sunhanwu.top:3306/cdn?charset=utf8')
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    op = operation(session)


    for index in tqdm(range(0,len(domain_list)-10,10)):
        domain_group=domain_list.iloc[index:index+10,1]
        pool = multiprocessing.Pool(processes=10)
        jobs = []
        time1=time.time()
        for domain in domain_group:
            try:
                #判断是否已经存在
                if op.is_exist(domain):
                    logger.info("{domain}is existing".format(domain=domain))
                    pass
                else:
                    logger.info("开始爬取{domain}".format(domain=domain))
                    job = pool.apply_async(multi_request_domain, args=(domain))
                    jobs.append(job)
                    logger.info("{domain}爬取成功".format(domain=domain))
            except Exception as e:
                logger.warning("插入错误")
        pool.close()
        pool.join()

        for host_job in jobs:
            domain_result = host_job.get()
            op.op_add(domain_result)

        logger.info("index:{index},时间time:{time}".format(index=index, time=time.time()-time1))




