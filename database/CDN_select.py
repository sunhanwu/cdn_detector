# @File  : CDN_select.py
# @Author: Sun Peishuai
# @Date  :  2020/12/16
import sys
sys.path.insert(0,"..")

from database.database import session, A, CNAME
from utils.utils import logger_database as logger
from utils.config import ip2name
def select_CDN(session):
    cdn_list=[]
    all_dns=set(session.query(CNAME.dns2).all())
    for cname in all_dns:
        try:
            ip_area=session.query(A.ip, A.area).filter_by(dns=cname[0]).all()

            ip_area=set(item[0][::-1].split(".",1)[1]+item[1] for item in ip_area)
            if len(ip_area)>=2:
                cdn_list.append(cname[0])
        except:
            print(ip_area)

    return cdn_list,len(cdn_list)

cdn_list,length=select_CDN(session)
print(length)
with open("cdn_list.txt","w",encoding="utf-8") as w:
    for cdn in cdn_list:
        w.write(cdn)
        w.write("\n")







