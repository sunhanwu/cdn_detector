"""
Author: Sun Peishuai
Date: 2020-12-08
"""
import sys
sys.path.append('..')
from py2neo import Graph,Node,Relationship
from database.database import session, A, CNAME
from py2neo.matching import NodeMatcher
from utils.config import ip2name, neo_graph
from utils.utils import logger_neo4j as logger

import sys
sys.path.append("../")
#循环mysql的CNAME表

def neo4j_mysql(session,neo_graph):
    matcher = NodeMatcher(neo_graph)
    for i in session.query(CNAME):
        try:
            dns1=i.dns1
            dns2=i.dns2
            #看是否已经存在该节点，如果已指向这个点
            if matcher.match(domain_name=dns1).exists():
                dns1_node=matcher.match(domain_name=dns1).first()
            else:
                dns1_node=Node("domain",domain_name=dns1,IF_CDN=False,count=0)
                IP_list=session.query(A).filter_by(dns=dns1).all()
                for i in IP_list:
                    IP = Node("IP",ip_add=i.ip, area=ip2name[i.area])
                    dns_connect=Relationship(dns1_node,'A',IP)
                    neo_graph.create(dns_connect)
            if matcher.match(domain_name=dns2).exists():
                dns2_node=matcher.match(domain_name=dns2).first()
            else:
                IP_list=session.query(A).filter_by(dns=dns2).all()
                if len(IP_list)>=2:
                    dns2_node=Node("CDN_domain",domain_name=dns2,IF_CDN=False)
                    for i in IP_list:
                        IP = Node("IP",ip_add=i.ip, area=ip2name[i.area])
                        dns_connect=Relationship(dns2_node,'A',IP)
                        neo_graph.create(dns_connect)
                else:
                    dns2_node=Node("domain",domain_name=dns2,IF_CDN=False)
                    for i in IP_list:
                        IP = Node("IP",ip_add=i.ip, area=ip2name[i.area])
                        dns_connect=Relationship(dns2_node,'A',IP)
                        neo_graph.create(dns_connect)

            dns_connect=Relationship(dns1_node,'CNAME',dns2_node)
            neo_graph.create(dns_connect)
            logger.info("{}-{} insert successfully".format(dns1, dns2))
        except Exception as e:
            logger.error("neo4j insert error {}".format(e))


            
if __name__ == '__main__':
    neo4j_mysql(session,neo_graph)
