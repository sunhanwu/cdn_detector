from database.database_sql import operation, mysql_neo4j
from database.database import session
from database.search_neo4j import search_domain_from_neo4j
import time
from back_end.manage import main

op = operation(session)
# op.op_add(data)
cname, a, cdn = op.op_select('google.com.')
nodes, edges = mysql_neo4j(cname, a, cdn)
print(nodes, edges)
main()
