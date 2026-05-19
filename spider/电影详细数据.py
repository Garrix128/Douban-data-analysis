# 导入依赖
import json
import re
import time

import pymysql
import requests
from lxml import etree
from bs4 import BeautifulSoup
import random


# 定义一个方法来获取数据库的链接
def get_conn():
    # 主机名、用户名、密码、数据库名
    conn = pymysql.connect(host='localhost', user='root', passwd='0902', database='movie_system')
    cursor = conn.cursor()
    return conn, cursor


# 设置浏览器的请求头信息
headers = {
    'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        ' AppleWebKit/537.36 (KHTML, like Gecko)'
        ' Chrome/134.0.0.0 Safari/537.36',
    'Referer':'https://movie.douban.com/',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Cookie':'_vwo_uuid_v2=D05F46F68BAB5BAFAF899770AFE298F37|791368d109bd71da1bd12ffa267cdc97; __yadk_uid=uR2UTvfQshHyE4Ng8nuvsgki05gaWcsa; __utma=30149280.1293679863.1707132455.1724392777.1732768893.3; __utma=223695111.93825112.1707132455.1724392777.1732768893.3; _vwo_uuid_v2=D05F46F68BAB5BAFAF899770AFE298F37|791368d109bd71da1bd12ffa267cdc97; bid=sysN60aZMds; dbcl2="289397822:umH9+zzpZwg"; ck=reP1'
}


# 编写程序来爬取电影的基础数据和详细信息数据
def spider_main(spiderTarget, page):
    # 通过request。get方法来访问获取
    params = {'start': page}  # 拼接参数-翻页
    session = requests.Session()
    session.headers.update(headers)
    moviesAllRes = requests.get(spiderTarget, params=params, headers=headers)  # 发起请求
    print('请求API的状态码:', moviesAllRes.status_code)
    # 获取响应信息
    moviesAll = moviesAllRes.json()
    # 根据data键获取值该页的所有电影信息，正常情况是每页20部电影
    moviesInfo = moviesAll['data']
    # 判断不存在电影的情况
    if not moviesInfo:  # 判断不存在电影的情况
        print('不存在电影的信息！！！')
        return []
    # 有电影数据、定义result数组用于存放数据
    result = []
    # 从API响应的信息中获取需要的电影数据 、进行遍历操作处理
    for i, movieInfo in enumerate(moviesInfo):
        resultData = {}  # 初始化空字典，用来存储每一部电影的详细信息
        # 1.导演（数组）
        resultData['directors'] = ','.join(movieInfo['directors'])
        # 2.评分  rate
        resultData['rate'] = movieInfo['rate']
        # 3.标题 title
        resultData['title'] = movieInfo['title']
        # 4.详细地址 detailLink
        resultData['detailLink'] = movieInfo['url']
        # 5.主演（数组） casts
        resultData['casts'] = ','.join(movieInfo['casts'])
        # 6.封面地址    cover
        resultData['cover'] = movieInfo['cover']
        # ----------再次发起请求，通过详细URL地址获取剩下的信息----------------
        detailMovieRes = requests.get(movieInfo['url'], headers=headers)
        print('请求详细URL的状态码:', detailMovieRes.status_code)
        if detailMovieRes.status_code != 200:  # 不正常的时候，继续
            continue
        # 通过XPath和BS4解析网页中的内容
        xpathHTML = etree.HTML(detailMovieRes.text)  # 修正HTML数据，获取网页数据
        soup = BeautifulSoup(detailMovieRes.text, 'lxml')  # BS对象
        # 7.上映年份  xpathHTML
        year = xpathHTML.xpath('//span[@class="year"]/text()')[0].strip('()')
        resultData['year'] = year if year else None
        # 8.影片类型（数组,多个） xpathHTML
        types = xpathHTML.xpath('//span[@property="v:genre"]/text()')
        resultData['types'] = ','.join(types) if types else None
        # 9.制片国家/地区 使用BeautifulSoup实现
        infoCountry = soup.find('div', id='info')
        country_match = re.findall(r'<span class="pl">制片国家/地区:</span>(.*?)<br/>', str(infoCountry), re.S)
        country = re.sub(r'\s+', '', country_match[0]).replace('/', ',') if country_match else None
        resultData['country'] = country
        # 10.语言
        infoLang = soup.find('div', id='info')
        lang_match = re.findall(r'<span class="pl">语言:</span>(.*?)<br/>', str(infoLang), re.S)
        lang = re.sub(r'\s+', '', lang_match[0]).replace('/', ',') if lang_match else None
        resultData['lang'] = lang
        # 11.上映时间
        try:
            upTime = soup.find_all('span', property="v:initialReleaseDate")
            upTimeStr = []
            for i in upTime:
                upTimeStr.append(i.get_text())  # 2025-03-07(韩国)
            time = re.findall(r'\d*-\d*-\d*', upTimeStr[0])
            resultData['time'] = time[0] if time else None
        except (IndexError, AttributeError):
            resultData['time']=None
        # 12.影片时长（如果有时长则获取，如果没有则随机生成一个整数作为时长）
        if soup.find('span', property="v:runtime"):
            mt = soup.find('span', property="v:runtime").get_text()
            mt = re.findall(r'\d+', mt)
            resultData['movieTime'] = mt[0] if mt else None
        else:
            resultData['movieTime'] = str(random.randint(30, 100))
        # 13.评论个数
        try:
            commentLen = xpathHTML.xpath('//span[@property="v:votes"]/text()')[0]
            resultData['commentLen'] = commentLen if commentLen else None
        except (IndexError, AttributeError):
            resultData['commentLen'] = None
        # 14.星级占比
        starAll = xpathHTML.xpath('//span[@class="rating_per"]/text()')
        resultData['star'] = ','.join(starAll) if starAll else None
        # 15.简介              summary
        summary = soup.find('span', property="v:summary")
        summary = re.sub(r'\s+', '', summary.get_text().strip())
        resultData['summary'] = summary if summary else None
        # 16.4张详情图  xpath  imgList
        imgList = xpathHTML.xpath('//div[@id="related-pic"]/ul/li/a/img/@src')
        imgList = ','.join(imgList)
        resultData['imgList'] = imgList if imgList else None
        result.append(resultData)  # 存储该页所有电影的数据
    return result


# 主函数
def main():
    # 数据库连接
    conn, cursor = get_conn()
    # 遍历页码 1-20页
    for page in range(13,20):
        # spiderTarget = 'https://movie.douban.com/j/new_search_subjects?start=' + str(page * 20)
        spiderTarget = 'https://movie.douban.com/j/new_search_subjects' # 改用豆瓣的 API 接口
        # spiderTarget = 'https://movie.douban.com/explore' 豆瓣对爬虫请求有严格的反爬机制，直接访问 explore 页面会被拒绝。
        # 调用方法来获取电影数据
        data = spider_main(spiderTarget, page * 20)
        # TODO 写入到数据库中
        sql_insert = '''
            insert into movies(directors,rate,title,casts,cover,year,types,country,lang,time
              ,movieTime ,commentLen,star,summary,imgList,detailLink 
            )values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        '''
        print(f'开始插入第{page + 1}页数据')
        for movie in data:
            params = (
                movie['directors'],
                movie['rate'],
                movie['title'],
                movie['casts'],
                movie['cover'],
                movie['year'],
                movie['types'],
                movie['country'],
                movie['lang'],
                movie['time'],
                movie['movieTime'],
                movie['commentLen'],
                movie['star'],
                movie['summary'],
                movie['imgList'],
                movie['detailLink']
            )
            # 执行sql数据语句
            cursor.execute(sql_insert, params)
        conn.commit()  # 提交事务
        time.sleep(random.uniform(5,10))  # 随机延时，避免过于频繁的请求
    # 关闭连接
    conn.close()
    cursor.close()


# 程序的入口
if __name__ == '__main__':
    main()
