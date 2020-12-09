import tornado.ioloop
import sys
sys.path.append("../")
import tornado.web
from utils.config import node_info
from dns_query.query import dns_query_all_servers
from utils.utils import logger_dnsquery as logger


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
            logger.info("QueryHandler, {}".format(self.request.uri))
            # 获取domain参数值
            domain = self.get_query_argument("domain")
            # 调用dns_query进行dns查询
            cname, a = dns_query_all_servers(domain)
            # 向resopnse写入字典信息，{'cname':cname, 'a':a}
            self.write({'cname': cname, 'a': a})
        except Exception as e:
            logger.error("QueryHandler timeout, query:{}, e:{}".format(self.request.uri, e))
            super().write_error(status_code=408, **kwargs)


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
            (r'/query', QueryHandler)
        ]
        tornado.web.Application.__init__(self, handlers)


def start_web_server():
    app = Application()
    app.listen(node_info['node3']['deploy']['port'])
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    start_web_server()
