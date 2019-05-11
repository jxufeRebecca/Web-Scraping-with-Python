import requests
from bs4 import BeautifulSoup
import re
import bs4
import traceback
import csv
import pandas as pd

#获取第一页的信息
def get_first_page(first_url,encode):
    try:
       r=requests.get(first_url)
       r.raise_for_status()
       r.encoding=encode
       return r.text
    except:
        return ""

#解析第一页，获得详细网页的网站信息
def parse_first_page(html):
    try:
        work_list=[]
        soup=BeautifulSoup(html,'html.parser')
        big_table=soup.find('div', attrs={'class': 'dw_table'})
        class1s=big_table.find_all('div', attrs={'class': 'el'})
        for classe1 in class1s[1:]:
                a=classe1.find('a',attrs={'target':'_blank'})
                work_name = a.text.strip()#strip可以去掉前后的空格
                href = a.attrs['href']
                span=classe1.find_all('span')
                work_list.append([work_name,href,span[1].string,span[2].string,span[3].string])
        return work_list
    except:
        traceback.print_exc()

#解析一个招聘信息的详细网页，所有的都是数据框中的一条
def parse_detail_page(html):
    try:
        information=[]
        soup=BeautifulSoup(html,'html.parser')
        #爬取公司属性、规模、所属行业
        p1=soup.find_all('p',attrs={'class':'at'})#当某个网页不存在此标签时，P1是空列表，不能调用P1
        if len(p1)!=0:
            company_attr = p1[0].text
            company_sides = p1[1].text
            company_yield = p1[2].text.replace("\n", "")#去掉文本中的换行符
        else:
            company_attr=''
            company_attr=''
            company_yield=''
        #爬取公司福利
        span=soup.find_all('span',attrs={'class':'sp4'})
        company_welfare=[]
        if len(span)!=0:#若列表非空
            for i in range(len(span)):
              company_welfare.append(span[i].text)#注意不能像C语言一样，c[i]=span[i]，要用append添加列表元素！
        div=soup.find_all('div',attrs={'class':'cn'})
        if len(div)!=0:
            cn=div[0]#将列表类型变成可以操作的,才可以用.p取子标签
            work_name=cn.h1.text.strip()
            company_name=cn.find('a').text.strip()#find返回的不是列表，不用加[0]
            salary=cn.strong.text
            p_2 = cn.find_all('p', attrs={'class': 'msg ltype'})#[0].text.strip().split('|')#p2万一也没找到呢
            if len(p_2)!=0:
                p2=p_2[0].text.strip().split('|')#p2是不是空呢？
                address = p2[0].replace("\xa0\xa0", "")  # 工作地点
                experience = p2[1].replace("\xa0\xa0", "")  # 工作经验要求
                re_p = []
                for i in range(len(p2)):
                    re_p.append(p2[i].replace("\xa0\xa0", ""))  # 注意re_p是去掉的
                people_list = []
                release_time = []
                degree = []
                for j in re_p:  # 如何把缺失值标记？
                    people = re.findall(r'招.*?人', j)
                    if len(people) == 0:
                        continue
                    people_list.append(people[0])  # 提取的保存在people_list里
                for r in re_p:  # 如何把缺失值标记？
                    rtime = re.findall(r'\d{2}\-\d{2}发布', r)
                    if len(rtime) == 0:
                        continue
                    release_time.append(rtime[0])
                for d in p2:  # 如何把缺失值标记？
                    dg = re.findall(r'\xa0\xa0..\xa0\xa0', d)
                    if len(dg) == 0:
                        continue
                    degree.append(dg[0].replace("\xa0\xa0", ""))  # 注意degree是列表，里面有空元素，degree[0]会报错的
                if len(degree)==0:
                    degree.append('')
            else:
                 address=''
                 experience=''
                 work_name=''
                 company_name=''
                 salary=''
            information.append([work_name,company_name,address,company_attr,company_sides,company_yield,company_welfare,salary,degree[0],experience,people_list[0],release_time[0]])
        #print(information)
        return information
    except:
        traceback.print_exc()

#把详细的信息存储到csv文件中
def csv_write_detail(items):#本来编码是gb2312，但是有两个生僻字总读取不出来，换成gb18030才成功
    csvFile=open('C:/Users/mac/Desktop/detail/first_test.csv','a',newline='', encoding='gb18030')#a表示追加写入、newline=''可以解决csv写入下一行是空行问题
    try:
        writer=csv.writer(csvFile)
        for item in items:
             writer.writerow((item))
    finally:
        csvFile.close()

def main():
    flist = []
    file_list=[]
    csvFile = open('C:/Users/mac/Desktop/detail/first_test.csv', 'w+', newline='', encoding='gb18030')#每次运行都会刷新该文件
    writer = csv.writer(csvFile)
    writer.writerow(('职位名称', '公司名称', '工作地点', '公司属性', '公司规模', '公司所属行业', '公司福利', '薪资', '学历', '工作经验', '招收人数', '发布时间'))
    for page in  range(1,1000):#成功读取两页，调用了两次该函数  "+str(page)+",page是页数
       print("正在爬取第" + str(page) + "页数据...")
       furl="https://search.51job.com/list/000000,000000,0000,00,9,99,%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590,2,"+str(page)+".html"
       html=get_first_page(furl,'gbk')
       flist=parse_first_page(html)
       #挖掘详细信息
       for i in flist:
           detail_html=get_first_page(i[1],'gb2312')
           dlist = parse_detail_page(detail_html)
           csv_write_detail(dlist)
main()
