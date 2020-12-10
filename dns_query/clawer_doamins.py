import requests
from lxml import etree
from utils.utils import logger_clawer as logger

def claw_subdomains(domain):
    """
    爬取百度搜索的一页内容
    :param domain: 域名
    :return: 一个
    """
    try:
        domains = []
        for i in range(1, 6):
            url = "http://tool.chinaz.com/subdomain?domain={}&page={}".format(domain, i)
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'max-age=0',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
            }
            response = requests.get(url=url, headers=headers)
            if response.status_code != 200:
                return domains[:100]
            text = response.text
            html = etree.HTML(text=text)
            blocks = html.xpath('/html/body/div[3]/div[1]/ul/li')
            for i in range(2, len(blocks)):
                target = html.xpath('/html/body/div[3]/div[1]/ul/li[{}]/div[2]/a/text()'.format(i))
                domains.append(target[0])
        logger.info("{} claw complete, total {} domains".format(domain, len(domains)))
    except Exception as e:
        logger.error("error occur, e {}".format(e))
    finally:
        return domains[:100]

if __name__ == '__main__':
    print(claw_subdomains()('google.com'))