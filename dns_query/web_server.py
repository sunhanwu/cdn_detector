import tornado.ioloop
import sys
sys.path.append("../")
import tornado.web
from config import node_info
from dns_query.query import dns_query_all_servers
from utils import request_domain
import os
import multiprocessing


class QueryHandler(tornado.web.RequestHandler):
    """
    query接口的处理函数
    """
    def get(self, *args, **kwargs):
        """
        处理get请求
        :param args: 参数
        :param kwargs: 参数
        :return: None
        """
        try:
            print(self.request.uri)
            # 获取domain参数值
            domain = self.get_query_argument("domain")
            # 调用dns_query进行dns查询
            cname, a = dns_query_all_servers(domain)
            # 向resopnse写入字典信息，{'cname':cname, 'a':a}
            self.write({'cname': cname, 'a': a})
        except Exception as e:
            super().write_error(status_code=408, **kwargs)

class SendHandler(tornado.web.RequestHandler):
    """
    """
    def get(self, *args, **kwargs):

        try:
            domain = self.get_query_argument('domain')
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


class Application(tornado.web.Application):
    """
    app主函数
    """
    def __init__(self):
        """
        构造函数
        """
        # 处理各种接口
        handlers = [
            (r'/query', QueryHandler),
            (r'/send', SendHandler)
        ]
        tornado.web.Application.__init__(self, handlers)


def start_web_server():
    app = Application()
    app.listen(node_info['node2']['deploy']['port'])
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    start_web_server()
