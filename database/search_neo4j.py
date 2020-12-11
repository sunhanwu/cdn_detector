import py2neo
from utils.config import neo_graph
from utils.utils import logger_neo4j as logger



def search_domain_from_neo4j(domain):
    """
    从图数据库中查询某个域名的完整链
    :param domain: 待查询的域名
    return: nodes:list, edges:list, node_item:{'id':1,'domain_name':'www.baidu.com.', 'IF_CDN':false}, edge_item:{'from': 1, 'end':2, label: A}
    """
    try:
        cypher_cmd = "match p=(n:domain{domain_name:'%s'})-[*]->(:IP) return p;" % domain
        search_result = neo_graph.run(cypher_cmd)
        data = search_result.data()
        nodes = []
        edges = []
        index = 0
        exist_domains = {}
        for item in data:
            p = item['p']
            if 'IP' in p.end_node.__str__():
                end_node_type = 'IP'
            else:
                end_node_type = 'domain'
            start_node = {'domain_name': p.start_node['domain_name'], 'IF_CDN': p.start_node['IF_CDN']}
            if start_node['domain_name'] not in exist_domains.keys():
                exist_domains[start_node['domain_name']] = len(list(exist_domains.keys())) + 1
                start_node_id = exist_domains[start_node['domain_name']]
                start_node['id'] = start_node_id
                nodes.append(start_node)
            else:
                start_node_id = exist_domains[start_node['domain_name']]
            if end_node_type == 'domain':
                end_node = {'domain_name': p.end_node['domain_name'], 'IF_CDN': p.end_node['IF_CDN']}
                if end_node['domain_name'] not in exist_domains.keys():
                    exist_domains[end_node['domain_name']] = len(list(exist_domains.keys())) + 1
                    end_node_id = exist_domains[end_node['domain_name']]
                    end_node['id'] = end_node_id
                    nodes.append(end_node)
                else:
                    end_node_id = exist_domains[end_node['domain_name']]
            else:
                end_node = {'ip': p.end_node['ip_add'], 'area': p.end_node['area']}
                if end_node['ip'] not in exist_domains.keys():
                    exist_domains[end_node['ip']] = len(list(exist_domains.keys())) + 1
                    end_node_id = exist_domains[end_node['ip']]
                    end_node['id'] = end_node_id
                    nodes.append(end_node)
                else:
                    end_node_id = exist_domains[end_node['ip']]
            edge = {'from': start_node_id, 'to': end_node_id}
            if p.relationships.__str__()[1] == 'A':
                edge['label'] = "A"
            else:
                edge['label'] = "CNAME"
            edges.append(edge)
        logger.info("neo4j查询{}成功".format(domain))
        return nodes, edges
    except Exception as e:
        logger.error("neo4j 查询{}失败，错误:{}".format(domain, e))
        # 查询错误返回空列表
        return [], []






