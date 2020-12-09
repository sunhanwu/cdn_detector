import sys
sys.path.append('../')
from database.database import DBSession
from database.database import CNAME, A, engine, create_engine, Base, sessionmaker


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

        self.session.add_all(all_record)
        self.session.commit()

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
            cname_record_result = self.session.query(CNAME).filter_by(dns1=dns)
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
        # a_record = []
        for dns_r in dns1_all_cname_list:
            a_record_result = self.session.query(A).filter_by(dns=dns_r)
            for record in a_record_result:
                a_record = [record.dns, record.ip, record.area, record.depth]
                a_all_list.append(a_record)

        return a_all_list

    def op_del(self):
        pass

    def op_chg(self):
        pass

if __name__ == '__main__':
    engine = create_engine('mysql+pymysql://cdn_user:cdn_123456@www.sunhanwu.top:3306/cdn?charset=utf8')
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    op = operation(session)

    data_dic = {'cname': [
        ['www.baidu.com', 'a.shifen.com', 0, '8.8.8.8'],
        ['www.sina.com', 'w.sina.com', 0, '114.114.8.8'],
        ['www.tent.com', 'tt.asdf.com', 0, '110.0.110.8'],
        ['www.ali.com', 'ali.ali.com', 0, '123.123.123.8']
    ],
                'a': [
                    ['a.shifen.com', '192.168.2.3', '8.8.8.8', '192.168.2.3', 2],
                    ['w.sina.com', '192.168.6.16', '114.114.8.8', '192.168.2.3', 2],
                    ['tt.asdf.com', '192.127.8.3', '110.0.110.8', '192.168.2.3', 2],
                    ['ali.ali.com', '192.26.2.3', '123.123.123.8', '192.168.2.3', 2]
                ]}

    # op.op_add(data_dic)

    data_dic_1 = {
        'cname': [['www.baidu.com', 'b.shifen.com', 0, '8.8.9.9'],
                  ['a.shifen.com', 'c.shifen.com', 0, '10.10.10.10']]
    }

    # op.op_add(data_dic_1)

    data_dic_2 = {
        'a': [['b.shifen.com', '192.156.15.3', '8.8.8.8', '192.168.2.3', 2],
              ['c.shifen.com', '192.211.123.3', '8.8.8.8', '192.168.2.3', 2]]
    }


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

    # op.op_add(data)

    # 查询所有
    # lists = op.op_select('www.baidu.com.')
    #
    # print('-')
    # for listss in lists:
    #     print(listss)

    ss = op.is_exist('www.baidu.com.')
    print(ss)

    sss = op.is_exist('www.tent.com.')
    print(sss)



