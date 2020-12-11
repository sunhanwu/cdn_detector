from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher
from database.database import session, A, CNAME
neo_graph = Graph(
    "http://node1.sunhanwu.top:7474",
    username="neo4j",
    password="sunhanwu"
)
import sys

sys.path.append("../")
from database.database import session

matcher = NodeMatcher(neo_graph)
# 循环mysql的CNAME表
for i in session.query(CNAME):
    dns1 = i.dns1
    dns2 = i.dns2
    # 看是否已经存在该节点，如果已指向这个点
    if matcher.match(domain_name=dns1).exists():
        dns1_node = matcher.match(domain_name=dns1).first()
    else:
        dns1_node = Node("domain", domain_name=dns1, IF_CDN=False, count=0)

    if matcher.match(domain_name=dns2).exists():
        dns2_node = matcher.match(domain_name=dns2).first()
    else:
        dns2_node = Node("domain", domain_name=dns2, IF_CDN=False, count=0)
    # 判断是否是CDN域名
    if session.query(A).filter_by(dns=dns2).count() >= 2:
        dns2_node["IF_CDN"] = True
    dns_connect = Relationship(dns1_node, 'point', dns2_node)
    neo_graph.create(dns_connect)
    # 初始化更新程序
    tx = neo_graph.begin()
    dns1_node["count"] += 1
    dns2_node["count"] += 1  # 边数count+1
    tx.push(dns1_node)
    tx.push(dns2_node)
    tx.commit()  # 提交更新
