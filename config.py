import os
db_config = {
    'host': 'www.sunhanwu.top',
    'port': 3306,
    'user': 'cdn_user',
    'password': 'cdn_123456',
    'database': 'cdn'
}

with open('./dns_servers.txt', 'r') as f:
    serverNames = {x.strip().split(':')[0]: x.strip().split(':')[1] for x in f.readlines()}
ip2name = {v:k for k, v in serverNames}

node_info = {
    'node1':{
        'deploy':{
            'ip': 'node1.sunhanwu.top',
            'port': 6009
        }
    },
    'node2':{
        'deploy':{
            'ip': 'node2.sunhanwu.top',
            'port': 6010
        }
    },
    'node3':{
        'proxy': {
            'proxy_ip': 'www.sunhanwu.top',
            'proxy_port': 6009,
        },
        'deploy': {
            'start_port': 8000
        }
    }
}



dns_timeout = 2