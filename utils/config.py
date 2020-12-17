import sys
from py2neo import Graph
sys.path.append('')
db_config = {
    'host': '',
    'port': ,
    'user': '',
    'password': '',
    'database': ''
}
neo_graph = Graph(
    "",
     username="",
     password=""
)

with open('../dns_query/dns_servers.txt', 'r',encoding="utf-8") as f:
    serverNames = {x.strip().split(':')[0]: x.strip().split(':')[1] for x in f.readlines()}
ip2name = {v:k for k, v in serverNames.items()}

node_info = {
    'node1':{
        'deploy':{
            'ip': '',
            'port': 6009
        }
    },
    'node2':{
        'deploy':{
            'ip': '',
            'port': 6010
        }
    },
    'node3':{
        'proxy': {
            'proxy_ip': '',
            'proxy_port': 6009,
        },
        'deploy': {
            'port': 8000
        }
    },
    'node4':{
        'deploy':{
            'ip':'',
            'port':6009
        }
    }
}

log_path = '../log/'



dns_timeout = 1
