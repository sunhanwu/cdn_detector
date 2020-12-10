import sys
sys.path.append('../')
from database.database import session, A, CNAME
from utils.utils import logger_database as logger


class operation():
    def __init__(self, session):
        self.session = session

    # 添加数据
    def op_add(self, new_data_dic):
        '''
        添加数据，传进来的数据是一个字典，字典有两个键值对，一个是cname，一个是a，对应的值就是要添加的数据
        其中值是列表的形式组合的。
        :param new_data_dic: 要添加的数据
        :return: null
        '''
        new_cname_list = new_data_dic.get('cname', [])    # 传入数据的‘cname’键值
        new_a_list = new_data_dic.get('a', [])      # 传入数据的‘a’键值
        all_record = []

        cname_record_list = []
        if new_cname_list is not None:
            for new_cname in new_cname_list:
                cname = CNAME(dns1=new_cname[0], dns2=new_cname[1], area=new_cname[3])
                cname_record_list.append(cname)

        a_record_list = []
        if new_a_list is not None:
            for new_a in new_a_list:
                # ip_24 = '.'.join(new_a[3].split('.')[:3])
                a = A(dns=new_a[0], ip=new_a[1], area=new_a[3], depth=new_a[2])
                a_record_list.append(a)

        all_record.extend(cname_record_list)
        all_record.extend(a_record_list)

        for item in all_record:
            try:
                self.session.add(item)
                self.session.commit()
                logger.info(item)
            except Exception as e:
                self.session.rollback()
                # logger.error("op_add error: {}".format(e))

    # 判断是否存在
    def is_exist(self, dns):
        record = self.session.query(CNAME).filter_by(dns1=dns)
        length = 0
        for sub in record:
            length += 1
        # 不存在
        if length == 0:
            return False
        else:
            return True

    # 查找
    def op_select(self, dns1):
        '''
        查询cname表中包含原始DNS是dns1的所有记录。
        而上面的结果中的cname记录可能还会有cname记录，所以需要继续查询
        经过上述操作得到dns1的所有cname记录后，进一步查询a表，查到所有的a记录。
        :param dns1: 原始域名
        :return: 与dns有关的所有cname在a表中的记录
        '''

        dns1_all_cname_list = []    # 保存于dns1所有有关的cname
        dns1_research_list = [dns1]     # 用于存储在cname表中查询的dns1.（包括查询出来的dns2）

        # 查询dns1所有的cname
        for dns in dns1_research_list:
            # print('查询前的域名：', dns1_research_list)
            # print('查询的域名：', dns)
            cname_record_result = self.session.query(CNAME.dns1.like("%{}%".format(dns)))
            # print(cname_record_result)    # 只是一条SQL语句

            # 将查询cname结果放到要查询的列表中，后续继续迭代查询
            result_length = 0
            for record in cname_record_result:
                result_length += 1
                # 判断一下是否已经在查询的表里了。
                if record.dns2 not in dns1_research_list:
                    dns1_research_list.append(record.dns2)
                    dns1_all_cname_list.append(record.dns2)     # 保存每次查询的结果

            # print('查询后的新结果：', dns1_research_list)

        # 查询cname的a记录
        a_all_list = []
        cdn_list = []
        # a_record = []
        index = 1
        for dns_r in dns1_all_cname_list:
            a_record_result = self.session.query(A).filter_by(dns=dns_r)
            state_depth_great1 = False
            # 注意，这里要注意，不能简单地遍历次数，以为可能IP是一样的，只是递归服务器不一样而已。
            ip_list = []
            for record in a_record_result:
                a_record = {'domain_name': record.dns, 'ip_addr': record.ip, 'recur_server': record.area, 'depth': record.depth}
                a_all_list.append(a_record)
                ip_list.append(record.ip)
                if record.depth >= 1:   # 深度大于等于1
                    state_depth_great1 = True

            # 如果深度大于等于1且IP个数大于等于2
            if state_depth_great1 and (len(set(ip_list)) >= 2):
                strs = 'cdn_' + str(index)
                cdn_list.append({strs: a_all_list[-1]['domain_name']})
                index += 1
                # temp_cdn = a_all_list[-1].copy()    # 深拷贝，不共用地址
                # dic_ip = {}
                # index = 1
                # for i in set(ip_list):
                #     strs = 'ip_'+str(index)
                #     dic_ip[strs] = i
                #     index += 1
                # temp_cdn['ip_addr'] = dic_ip
                # cdn_list.append(temp_cdn)

        return a_all_list, cdn_list

    def op_del(self):
        pass

    def op_chg(self):
        pass

if __name__ == '__main__':
    data = {
        'cname': [['www.baidu.com.', 'www.a.shifen.com.', 0, '37.235.1.174'],
                  ['www.a.shifen.com.', 'www.wshifen.com.', 1, '37.235.1.174'],
                  ['www.baidu.com.', 'www.a.shifen.com.', 0, '79.141.82.250'],
                  ['www.a.shifen.com.', 'www.wshifen.com.', 1, '79.141.82.250'],
                  ['www.baidu.com.', 'www.a.shifen.com.', 0, '80.80.80.80'],
                  ['www.a.shifen.com.', 'www.wshifen.com.', 1, '80.80.80.80'],
                  ['www.baidu.com.', 'www.a.shifen.com.', 0, '221.11.1.67'],
                  ['www.baidu.com.', 'www.a.shifen.com.', 0, '61.132.163.68'],
                  ['www.baidu.com.', 'www.a.shifen.com.', 0, '45.248.197.53'],
                  ['www.a.shifen.com.', 'www.wshifen.com.', 1, '45.248.197.53'],
                  ['www.baidu.com.', 'www.a.shifen.com.', 0, '168.95.1.1'],
                  ['www.a.shifen.com.', 'www.wshifen.com.', 1, '168.95.1.1'],
                  ['www.baidu.com.', 'www.a.shifen.com.', 0, '202.14.67.4'],
                  ['www.a.shifen.com.', 'www.wshifen.com.', 1, '202.14.67.4'],
                  ['www.baidu.com.', 'www.a.shifen.com.', 0, '210.22.70.3'],
                  ['www.baidu.com.', 'www.a.shifen.com.', 0, '165.87.13.129'],
                  ['www.a.shifen.com.', 'www.wshifen.com.', 1, '165.87.13.129'],
                  ['www.baidu.com.', 'www.a.shifen.com.', 0, '45.248.197.53'],
                  ['www.a.shifen.com.', 'www.wshifen.com.', 1, '45.248.197.53'],
                  ['www.baidu.com.', 'www.a.shifen.com.', 0, '168.95.1.1'],
                  ['www.a.shifen.com.', 'www.wshifen.com.', 1, '168.95.1.1'],
                  ['www.baidu.com.', 'www.a.shifen.com.', 0, '202.14.67.4'],
                  ['www.a.shifen.com.', 'www.wshifen.com.', 1, '202.14.67.4'],
                  ['www.baidu.com.', 'www.a.shifen.com.', 0, '165.87.13.129'],
                  ['www.a.shifen.com.', 'www.wshifen.com.', 1, '165.87.13.129'],
                  ['www.baidu.com.', 'www.a.shifen.com.', 0, '84.200.69.80'],
                  ['www.a.shifen.com.', 'www.wshifen.com.', 1, '84.200.69.80']],
        'a': [['www.wshifen.com.', '104.193.88.123', 2, '37.235.1.174'],
              ['www.wshifen.com.', '103.235.46.39', 2, '79.141.82.250'],
              ['www.wshifen.com.', '103.235.46.39', 2, '80.80.80.80'],
              ['www.a.shifen.com.', '110.242.68.4', 1, '221.11.1.67'],
              ['www.a.shifen.com.', '14.215.177.38', 1, '61.132.163.68'],
              ['www.wshifen.com.', '119.63.197.151', 2, '45.248.197.53']]
    }

    op = operation(session)
    op.op_add(data)



