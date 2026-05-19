import stylecloud
from tools.getDataBase import get_conn


# 实现标题词云
# 需要绘制的字段、图标名称、输出名称
def getTitleImg(field, icon_name, output_name):
    try:
        sql = f'select {field} from movies'
        conn, cursor = get_conn()
        cursor.execute(sql)
        data = cursor.fetchall()  # 获取查询结果
        text1 = ','.join([row[0] for row in data])
        text1 = ','.join(text1)  # 这个操作是将标题拆分为一个一个的字
        stylecloud.gen_stylecloud(text=text1, icon_name=icon_name,
                                  output_name=output_name,
                                  font_path='static/fonts/simhei.ttf')
    except Exception as e:
        print(e)

# 实现演员名词云
def getCastsImg(field, icon_name, output_name):
    try:
        sql = f'select {field} from movies'
        conn, cursor = get_conn()
        cursor.execute(sql)
        data = cursor.fetchall()  # 获取查询结果
        text1 = ','.join([row[0] for row in data])
        # text1 = ','.join(text1)#这个操作是将标题拆分为一个一个的字
        stylecloud.gen_stylecloud(text=text1, icon_name=icon_name,
                                  output_name=output_name,
                                  font_path='static/fonts/simhei.ttf')
    except Exception as e:
        print(e)


# 实现自定义
def getCommentsImg(field, serchWord, icon_name, output_name):
    try:
        sql = f'select {field} from comments where movieName="{serchWord}"'
        conn, cursor = get_conn()
        cursor.execute(sql)
        data = cursor.fetchall()  # 获取查询结果

        if not data:
            raise ValueError("数据库中没有找到对应的评论内容")
        text1 = ','.join([row[0] for row in data])

        if not text1.strip():
            raise ValueError("获取到的评论内容为空，无法生成词云")
        stylecloud.gen_stylecloud(text=text1, icon_name=icon_name,
                                  output_name=output_name,
                                  font_path='static/fonts/simhei.ttf')
    except Exception as e:
        print(e)
