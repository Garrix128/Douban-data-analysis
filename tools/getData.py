import os
import pandas as pd
from tools.getDataBase import get_conn
import warnings

warnings.filterwarnings('ignore')

# 获取当前文件所在目录的绝对路径
# D:\PythonProject\gzdouban\tools
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# D:\PythonProject\gzdouban\tools\data
TOOLS_DIR = os.path.join(BASE_DIR, 'data')
# 确保目录存在，不存在则创建
if not os.path.exists(TOOLS_DIR):
    os.makedirs(TOOLS_DIR)


# 数据获取
def dataExport():
    conn, cursor = get_conn()  # 获取数据库对象
    sql = 'select id,directors,rate,title,casts,year,types,country,lang,time,movieTime,commentLen,star from movies'
    data = pd.read_sql(sql, conn)  # 使用pandas获取数据库中的数据
    if not data.empty:  # 不为空则保存数据
        data.to_csv(os.path.join(TOOLS_DIR, 'moviesData.csv'), index=False, encoding='utf-8')
    else:
        print('查询结果为空,未导出数据！！！')


# 统计电影类型TOP5数据
def typesData():
    # 读取数据
    data = pd.read_csv(os.path.join(TOOLS_DIR, 'moviesData.csv'))
    # expand数据框  stack()堆叠  reset_index设置索引
    df_split = data['types'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)  # 180*6
    # 统计每个类型的数据
    type_counts = df_split.value_counts()
    # 转为DataFrame
    type_counts_df = type_counts.reset_index()  # 27*2
    # 构建新的标签
    type_counts_df.columns = ['类型', '数量']
    # 获取前5数据
    data01 = type_counts_df.head(5)
    # 将结果存储CSV文件中
    data01.to_csv(os.path.join(TOOLS_DIR, 'type_counts.csv'), index=False, encoding='utf-8')


# 年份电影数据量
def yearsData():
    # 读取数据
    data = pd.read_csv(os.path.join(TOOLS_DIR, 'moviesData.csv'))
    # 统计每个年份的数量
    year_counts = data['year'].value_counts()
    # 转为DataFrame
    year_counts_df = year_counts.reset_index()
    # 构建新的标签
    year_counts_df.columns = ['年份', '数量']
    # 获取前5数据
    data02 = year_counts_df.head(5)
    # 将结果存储CSV文件中
    data02.to_csv(os.path.join(TOOLS_DIR, 'year_counts.csv'), index=False, encoding='utf-8')


# 中英文电影占比
def langData():
    # 读取数据
    data = pd.read_csv(os.path.join(TOOLS_DIR, 'moviesData.csv'))
    # expand数据框  stack()堆叠  reset_index设置索引
    df_split = data['lang'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)
    # 统计语言的数量
    lang_counts = data['lang'].value_counts()
    # 转为DataFrame
    lang_counts_df = lang_counts.reset_index()
    # 构建新的标签
    lang_counts_df.columns = ['语言', '数量']
    # 获取前5数据
    data03 = lang_counts_df.head(2)
    # 将结果存储CSV文件中
    data03.to_csv(os.path.join(TOOLS_DIR, 'lang_counts.csv'), index=False, encoding='utf-8')


# 电影评论数折线图
def commentsData():
    # 读取数据
    data = pd.read_csv(os.path.join(TOOLS_DIR, 'moviesData.csv'))
    # 将评论数据转为整型类型
    data['commentLen'] = data['commentLen'].astype(int)
    # 根据commentLen列对数据近排序（高-低）
    topComments = data.sort_values('commentLen', ascending=False).head(5)
    # 获取排序后电影的名字和评论数据
    topComments = topComments[['title', 'commentLen']]
    # 构建新的标签
    topComments.columns = ['电影', '数量']
    # 将结果存储CSV文件中
    topComments.to_csv(os.path.join(TOOLS_DIR, 'comment_counts.csv'), index=False, encoding='utf-8')


# 统计不同国家地区的数据
def countryData():
    data = pd.read_csv(os.path.join(TOOLS_DIR, 'moviesData.csv'))
    # expand数据框  stack()堆叠  reset_index设置索引
    df_split = data['country'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)  # 180*6
    # 统计每个类型的数据
    type_counts = df_split.value_counts()
    # 转为DataFrame
    type_counts_df = type_counts.reset_index()  # 27*2
    # 构建新的标签
    type_counts_df.columns = ['国家', '数量']
    # 获取前5数据
    data01 = type_counts_df.head(10)
    # 将结果存储CSV文件中
    data01.to_csv(os.path.join(TOOLS_DIR, 'country_counts.csv'), index=False, encoding='utf-8')



def mainFun():
    dataExport()
    typesData()
    yearsData()
    langData()
    commentsData()
    countryData()


if __name__ == '__main__':
    mainFun()
