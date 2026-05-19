import json
import pandas as ps
from tools.getDataBase import get_conn  # 导入新的连接对象

def getComedyAndDramaByYear():
    allData = getAllData()
    drama_count = {}
    comedy_count = {}

    for movie in allData:
        year = movie[6]
        types = movie[7]

        if '剧情' in types:
            if year not in drama_count:
                drama_count[year] = 1
            else:
                drama_count[year] += 1

        if '喜剧' in types:
            if year not in comedy_count:
                comedy_count[year] = 1
            else:
                comedy_count[year] += 1

    years = sorted(set(list(drama_count.keys()) + list(comedy_count.keys())))
    drama_values = [drama_count.get(year, 0) for year in years]
    comedy_values = [comedy_count.get(year, 0) for year in years]

    return years, drama_values, comedy_values
def getAllData():
    """
    从数据库中读取所有电影数据，并对某些字段进行格式处理。
    返回处理后的二维列表数据。
    """

    def map_fn(item):
        """
        数据清洗函数，用于处理每条电影记录中的字段。
        主要包括将 None 值替换为默认值、将字符串按逗号分割成列表等操作。
        """
        item = list(item)  # 将元组转为列表，便于后续修改

        # 处理 directors 字段（索引1）
        if item[1] == None:
            item[1] = '无'
        else:
            item[1] = item[1].split(',')  # 按逗号拆分为导演列表

        # 处理 casts 字段（索引4）
        if item[4] == None:
            item[4] = '无'
        else:
            item[4] = item[4].split(',')  # 按逗号拆分为演员列表

        # 处理 types 字段（索引7），如果出错则设为 ['剧情']
        try:
            item[7] = item[7].split(',')
        except Exception as e:
            item[7] = ['剧情']

        # 处理 country 字段（索引8）
        if item[8] == None:
            item[8] = '中国大陆'
        else:
            item[8] = item[8].split(',')  # 拆分为国家/地区列表

        # 处理 lang 字段（索引9）
        if item[9] == None:
            item[9] = '汉语普通话'
        else:
            item[9] = item[9].split(',')  # 拆分为语言列表

        # 处理 star 字段（索引13），假设该字段一定存在
        item[13] = item[13].split(',')  # 拆分为星级标签列表

        # 处理 imgList 字段（索引15），假设该字段一定存在
        item[15] = item[15].split(',')  # 拆分为图片链接列表

        # 注意：原代码中有被注释掉的 json.loads(item[15])，
        # 如果图片链接是以 JSON 格式存储的字符串，应该使用 json.loads 解析。

        return item  # 返回清洗后的单条数据

    # 连接数据库
    conn, cursor = get_conn()

    # 执行 SQL 查询语句：查询 movies 表中所有数据
    cursor.execute('select * from movies')

    # 获取所有查询结果
    allData = cursor.fetchall()

    # 使用 map 函数对每条数据应用 map_fn 清洗函数
    allData = list(map(map_fn, list(allData)))

    # 返回清洗后的二维列表数据
    return allData


df = ps.DataFrame(getAllData(), columns=[
    'id',
    'directors',
    'rate',
    'title',
    'casts',
    'cover',
    'year',
    'types',
    'country',
    'lang',
    'time',
    'movieTime',
    'commentLen',
    'star',
    'summary',
    #'comments',
    'imgList',
    'detailLink'
])


def getMaxRate():
    return df['rate'].astype(float).max()


def getMinRate():
    return df['rate'].astype(float).min()


def getMaxCast():
    allData = getAllData()
    casts = {}
    maxName = ''
    maxNum = 0
    for i in allData:
        for j in i[4]:
            if casts.get(j, -1) == -1:
                casts[j] = 1
            else:
                casts[j] = casts[j] + 1
    for k, v in casts.items():
        if int(v) > maxNum:
            maxNum = v
            maxName = k
    return maxName


def getMaxLang():
    allData = getAllData()
    langs = {}
    maxLang = ''
    maxNum = 0
    for i in allData:
        for j in i[9]:
            if langs.get(j, -1) == -1:
                langs[j] = 1
            else:
                langs[j] = langs[j] + 1
    for k, v in langs.items():
        if int(v) > maxNum:
            maxNum = v
            maxLang = k
    return maxLang


def getTypesAll():
    allData = getAllData()
    types = {}
    for i in allData:
        for j in i[7]:
            if types.get(j, -1) == -1:
                types[j] = 1
            else:
                types[j] = types[j] + 1
    return types.keys()


def getType_t():
    allData = getAllData()
    types = {}
    for i in allData:
        for j in i[7]:
            if types.get(j, -1) == -1:
                types[j] = 1
            else:
                types[j] = types[j] + 1
    data = []
    for k, v in types.items():
        data.append({
            'name': k,
            'value': v
        })
    return data


def getRate_t():
    allData = getAllData()
    rates = {}
    for i in allData:
        if rates.get(i[2], -1) == -1:
            rates[i[2]] = 1
        else:
            rates[i[2]] = rates[i[2]] + 1
    return rates.keys(), rates.values()


def getTableList():
    def map_fn(item):
        item[1] = '/'.join(item[1])
        item[4] = '/'.join(item[4])
        item[7] = '/'.join(item[7])
        item[8] = '/'.join(item[8])
        item[9] = '/'.join(item[9])
        return item

    allData = list(getAllData())
    allData = map(map_fn, allData)
    return list(allData)
