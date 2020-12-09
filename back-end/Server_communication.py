import sys
sys.path.append("..")
from utils import request_domain
import config
import requests
import multiprocessing
import time
# from config import serverNames

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
    time1=time.time()
    results=multi_request_domain("www.baidu.com.")
    print(len(results["a"]))
    print(time.time()-time1)
    print(results)



