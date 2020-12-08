"""
Author: sunhanwu
Date: 2020-12-08
"""
from locust import Locust, task, TaskSet, HttpUser
from utils import load_alexa_domains

class PressureTest(HttpUser):
    """
    利用locust工具对各个接口进行压力测试
    """

    @task()
    def test_query(self, domain):
        """
        测试query接口
        :param domain: 传入参数域名
        :return: None
        """
        self.client.get('/query?domain={}'.format(domain))

# class Mylocust(HttpUser):
#     task_set = PressureTest
#     host = "http://www.sunhanwu.top:6009"
#     min = 1000
#     max = 3000


