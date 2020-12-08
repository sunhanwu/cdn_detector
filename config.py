db_config = {
    'host': 'www.sunhanwu.top',
    'port': 3306,
    'user': 'cdn_user',
    'password': 'cdn_123456',
    'database': 'cdn'
}

with open('./dns_servers.txt', 'r') as f:
    serverNames = {x.strip().split(':')[0]: x.strip().split(':')[1] for x in f.readlines()}

node_info = {
    'node1':{
        'ip': 'www.sunhanwu.top',
        'visit_port': 6009,
        'start_port': 8000
    }
}

