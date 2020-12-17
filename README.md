# cdn_detector
An efficient distributed CDN domain name detector

## 一、代码介绍

1. dns_query：负责爬取dns解析记录并提供访问API接口
   + clawer_domains.py：爬取指定域名下的所有子域名列表
   + query.py: 爬取给定DNS递归服务器指定域名的DNS解析路径，支持一次查询一个递归服务器，也支持一次查询多个递归服务器
   + web_server.py：提供一个web形式的API，方便中心节点向子节点下发任务
     + 接口名：/query
     + 参数1：待查域名
     + 参数2：递归服务器ip列表
2. database: 定义mysql数据库表已经数据库查询插入等操作
   + database.py: 定义存储A记录的关系表A和存储CNAME记录的CNAME表

   + database_op.py: 以对象/关系映射（ORM）形式封装数据库，以面向对象的形式操作数据库。

     + is_exist(), 判断域名是在数据库中；

     + op_add(), 添加CNAME记录/A记录，以字典的形式传入；

     + op_select(), 查找某个域名，返回与之相关的系列CNAME域名（如果CNAME解析的IP个数大于等于某个阈值，如2）。

   + search_neo4j.py：从图数据库neo4j中取出某个域名到所有的IP的完整路径，并格式化为两个字典列表格式，用于前端渲染
3. test: 使用locust压力测试工具进行压力测试
  
   + pressure_test.py： 压力测试类
4. utils: 提供配置和一些常用工具函数
  
   + config：定义了数据库配置信息，DNS递归服务器信息，子节点信息等
5. back_end: 使用django实现的主节点web服务
6. dns_manage: 核心框架：[Vue](https://cn.vuejs.org/v2/guide/)
   - 状态管理：[Vuex](https://vuex.vuejs.org/zh-cn/intro.html)
   - 路由映射：[vue-router](https://router.vuejs.org/zh-cn/)
   - UI组件库：[Muse-UI](https://museui.github.io/#/index),[Element](http://element.eleme.io/#/zh-CN/component/quickstart)
   - HTTP请求库：[axios](https://github.com/mzabriskie/axios)
   - CSS的预处理框架：[中文文档](http://www.zhangxinxu.com/jq/stylus/),[sass](http://sass.bootcss.com/)
   - 资源加载打包工具：[Webpack](https://webpack.github.io/)
   - 其他：[ES6](https://wohugb.gitbooks.io/ecmascript-6/content/index.html),[node.js](https://nodejs.org/en/),[npm](https://www.npmjs.com/), vis

## 二、部署



### 2.1 环境搭建

> 主节点在

1. python环境：提供requirements.txt文件

   ```bash
   pip install -r requirements.txt
   ```

2. 数据库环境: 

   + mysql
   + neo4j

### 2.2 部署

> 在utils/config中配置好mysql和各个节点的信息

1. dns解析记录子节点部署

   ```bash
   cd dns_query
   python web_server.py
   ```

2. 部署主节点

   ```bash
   cd back_end
   python Server_communication.py
   ```

3. 部署web服务

   ```bash
   cd back_end
   python manage.py runserver
   ```

   
