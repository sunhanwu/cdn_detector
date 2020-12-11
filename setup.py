from database.database_sql import operation, mysql_neo4j
from database.database import session
from database.search_neo4j import search_domain_from_neo4j
import time

op = operation(session)
start_time = time.time()
cname, a, cdn = op.op_select('baidu.com.')
mysql_result = mysql_neo4j(cname, a, cdn)
print("mysql search time:{}".format(time.time() - start_time))
print("mysql result:".format(mysql_result))
start_time = time.time()
neo4j_result = search_domain_from_neo4j('baidu.com.')
print("neo4j search time:{}".format(time.time() - start_time))
print("neo4j result:".format(neo4j_result))
