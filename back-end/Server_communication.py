import sys
sys.path.append("..")
from utils import request_domain
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


pool = multiprocessing.Pool(processes=3)
jobs = []
for url in url_list:
    job = pool.apply_async(request_domain, args=(url,domain))
    jobs.append(job)
pool.close()
pool.join()

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
        time1=time.time()
        try:
            #判断是否已经存在
            if op.is_exist(domain):
                print("{domain}is existing".format(domain=domain))
            else:
                print("开始爬取{domain}".format(domain=domain))
                results=multi_request_domain(domain)

                print(results)
                time2=time.time()
                log("index:{index},爬取time:{time}".format(index=index, time=time2-time1))
                op.op_add(results)
                print("插入成功")
                print("index:{index},插入time:{time}".format(index=index, time=time.time()-time2))
                print(len(results["a"]))

            #插入数据
        except Exception as e:
            print("插入错误")



