import pymysql
from sqlalchemy import create_engine

# 连接数据库
def get_conn():
    # 主机、用户名、密码、数据库名称、端口号
    conn = pymysql.connect(host='127.0.0.1', user='root', password='0902', database='movie_system', port=3306)
    cursor = conn.cursor()
    return conn, cursor