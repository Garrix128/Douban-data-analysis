import re
import pymysql
import requests
from lxml import etree


# 连接数据库
def get_conn():
    # 主机名、用户名、密码、数据库名
    conn = pymysql.connect(host='localhost', user='root', passwd='0902', database='movie_system')
    cursor = conn.cursor()
    return conn, cursor


# 设置浏览器请求头
headers = {
    'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        ' AppleWebKit/537.36 (KHTML, like Gecko)'
        ' Chrome/134.0.0.0 Safari/537.36'
}

# 获取movies表中的电影ID的数组  详细地址的样式==》  https://movie.douban.com/subject/27119724/
def get_MoviesdId():
    conn, cursor = get_conn()
    sql_select = 'select detailLink from movies'  # 定义查询语句
    cursor.execute(sql_select)  # 执行sql语句
    data = cursor.fetchall()  # 获取所有查询的结果
    mIdList = []
    for row in data:
        mId = re.findall(r'\d+', row[0])
        mIdList.append(mId[0])
    return mIdList


# 根据电影ID爬取评论数据
def spinder_main():
    conn, cursor = get_conn()
    #获取所有的电影的id
    mIdList = get_MoviesdId()
    # 根据ID进行获取对应的评论信息
    for mid in mIdList:
        for page in range(3):
            base_url = 'https://movie.douban.com/subject/{}/reviews?start={}'.format(mid, page * 20)
            # print(base_url)
            # 发起请求
            response = requests.get(base_url, headers=headers)
            print('评论内容URL的状态码:', response.status_code)
            if response.status_code != 200:
                continue
            xpathHTML = etree.HTML(response.text)
            # 获取电影名称
            movieName = xpathHTML.xpath('//div[@class="subject-title"]/a/text()')[0][2:]
            # 获取存放评论信息的div
            divs = xpathHTML.xpath('//div[@class="review-list  "]/div')
            # 循环提取div中的评论信息
            for div in divs:
                contents = div.xpath('.//div[@class="short-content"]/text()')
                try:
                    contentData = contents[0].strip().replace('\n', '').replace('(', '').replace(')', '').replace(' ', '')
                except Exception as e:
                    continue
                # 写入数据库中
                if contents and contentData and movieName:
                    sql_insert = 'insert into comments(movieName,commentContent) values(%s,%s)'
                    cursor.execute(sql_insert, (movieName, contentData))
            conn.commit()  # 提交事务
    conn.close()
    cursor.close()


if __name__ == '__main__':
    spinder_main()