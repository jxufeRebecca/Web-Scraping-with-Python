## 招聘网站定向爬虫实例

    朱爱璐 江西财经大学
    
程序实现了获取前程无忧网站“数据分析”岗位搜索页面的信息，并从中提取招聘企业信息、招聘岗位信息，存储在本地csv文件中。
+ 技术路线：requests——BeautifulSoup——re
+ 程序的结构设计：
                1. 获取基本信息网页的内容<br>
　　　　　　　　　2. 解析基本信息网页，并返回详细信息网页的网址<br>
　　　　　　　　　3. 获取详细信息网页的内容<br>
                4. 解析详细网页<br>
                5. 将结果存储至CSV文件中

