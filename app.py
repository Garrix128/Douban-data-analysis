from functools import wraps

from tools.getDataBase import get_conn
from flask import Flask, render_template, request
from flask import redirect, url_for, session
from flask import jsonify


# 导入工具文件中的函数
from tools.actor import *
from tools.addressData import *
from tools.homeData import *
from tools.rateData import *
from tools.timeData import *
from tools.typeData import *
from tools.word_cloud import *

import pandas as pd
from pyecharts.charts import *  # 导入所有的图表
from pyecharts import options as opts  # 导入配置项

# 创建Flask的对象，指定静态文件和模板文件
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'ywqqq'

# 404错误处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 退出登录路由
@app.route('/logout')
def logout():
    # 清除session中的用户名
    session.pop('username', None)
    # 跳转回登录页面
    return redirect(url_for('login'))

# 登录验证装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# 实现一个视图函数，作为根路由
@app.route('/')
def rootRoute():
    return render_template('login.html')

# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']  # 获取用户名和密码
        password = request.form['password']
        if not username or not password:
            # 如果没有用户名和密码，则重定向回注册视图界面
            return redirect(url_for('register'))
        # 判断两次输入的密码是否一致
        if request.form['password'] != request.form['passwordCheked']:
            return '<h1>两次密码不一致！！！</h1>'
        # 获取数据
        conn, cursor = get_conn()
        cursor.execute('select username from users')
        data = cursor.fetchall()  # 查看数据库中所有的用户信息
        userList = [user[0] for user in data]
        if username in userList:
            return '<h1>用户名已经存在！！！</h1>'
        # 如果填写的信息完全正确，就将信息写入到数据库中
        cursor.execute('insert into users(username,password) values(%s,%s)', (username, password))
        conn.commit()
        return redirect(url_for('login'))  # 注册成功，跳转到登录页面
    return render_template('register.html')

# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']  # 获取用户名和密码
        password = request.form['password']
        if not username or not password:
            # 如果没有用户名和密码，则重定向回登录视图界面
            return redirect(url_for('login'))
        conn, cursor = get_conn()
        cursor.execute('select * from users where username = "%s" and password="%s"' % (username, password))
        user = cursor.fetchone()  # 找到一个即可
        if user:  # 如果存在用户名，则保存用户名到Session中，并且跳转到home界面
            session['username'] = username
            return redirect(url_for('home'))
        else:  # 如果没用户名则调整回到登录界面
            return redirect(url_for('login'))
    # TODO 实现登录的基本操作，登录成功后，跳转到首页
    return render_template('login.html')

# 首页
@app.route('/home')
@login_required
def home():
    username = session['username']
    # 获取首页需要显示的所有信息，并从后台--前端进行展示出来
    allData = getAllData()  # 获取所有的电影数据
    dataLen = len(allData)  # 统计电影长度
    maxRate = getMaxRate()  # 电影最高的分数
    maxCast = getMaxCast()  # 出场最多的演员
    typeAll = getTypesAll()  # 获取电影种类数据
    typeAll = len(typeAll)  # 统计种类长度
    maxLang = getMaxLang()  # 获取电影语言数据
    # 获取图标需要的数据
    types = getType_t()  # 电影种类饼状图的数据
    x, y = getRate_t()  # 电影评分折线图的数据
    return render_template('home.html', username=username,
                           dataLen=dataLen, maxRate=maxRate, maxCast=maxCast,
                           typeAll=typeAll, maxLang=maxLang,types=types,
                           x=list(x),y=list(y))

# 实现搜索
@app.route('/search/<int:searchId>', methods=['GET', 'POST'])
@login_required
def search(searchId):  # 使用GET？POST？请求
    username = session['username']
    allData = getAllData()  # 获取所有的电影数据
    data = []  # 用户存储过滤的数据
    if request.method == 'GET':
        if searchId == 0:
            return render_template('search.html', username=username, data=data)
        # 遍历所有的电影,找到跟点击电影ID一致的电影
        for i in allData:
            if i[0] == searchId:
                data.append(i)
        return render_template('search.html', username=username, data=data)
    else:  # POST
        searchWord = request.form['searchIpt']
        if not searchWord:  # 如果搜索框为空，则重定向回该界面
            return redirect(url_for('search', searchId=searchId))

        # 如果有数据，则进行过滤操作，定义一个过滤函数，用于过滤数据
        def filterFun(item):
            if item[3].find(searchWord) == -1:
                return False
            else:
                return True

        data = list(filter(filterFun, allData))
        return render_template('search.html', username=username, data=data)

 # 实现时间分析表
@app.route('/time_t')
@login_required
def time_t():
    username = session['username']
    x, y = getTimeList()  # 历年产量统计
    movieTimeData = getMovieTimeList()  # 电影数据时长分布占比
    return render_template('time_t.html', username=username,
                            x=list(x), y=list(y), movieTimeData=movieTimeData)

# 实现评分分析表
@app.route('/rate_t/<type>', methods=['GET', 'POST'])
@login_required
def rate_t(type):
    username = session['username']
    # 电影类型评分统计
    typeAll = getTypesAll()  # 获取电影种类
    if type == 'all':
        x, y = getRate_t()
    else:
        x, y = getRate_tType(type)  # 获取不同类型电影的数据
    #星级饼状图
    if request.method == 'GET':
        star,movieName=getStart('')#默认获取第一部电影
    else:
        searchWord = request.form['searchIpt'].strip()
        try:#如果没有问题就获取输入电影的星级占比和名称
            star,movieName=getStart(searchWord)
        except Exception as e:
            return redirect(url_for('rate_t', type=type))
    #年度评价评分柱状图
    x1,y1=getMean()
    y1=[round(y1_val,2) for y1_val in y1]
    #电影中外评分分布图
    x2,y2,y22=getCountryRating()
    return render_template('rate_t.html',username=username,
                           x=list(x),y=list(y),star=star,movieName=movieName,
                           x1=x1,y1=y1,x2=x2,y2=y2,y22=y22,typeAll=typeAll)

 # 实现数据分析表
@app.route('/datasort', methods = ['GET'])
@login_required
def movie_counts():
    username = session['username']

    # 获取国家和语言数据
    address_keys, address_values = getAddressData()
    lang_keys, lang_values = getLangData()

    # 构造国家电影数量列表 [{name: '中国', value: 100}, ...]
    country_data = [{"name": key, "value": value} for key, value in zip(address_keys, address_values)]
    lang_data = [{"name": key, "value": value} for key, value in zip(lang_keys, lang_values)]

    # 获取历年喜剧和剧情电影数量
    years, drama_count, comedy_count = getComedyAndDramaByYear()

    # 年度评价评分柱状图
    x1, y1 = getMean()
    y1 = [round(y1_val, 2) for y1_val in y1]

    return render_template(
        'datasort.html',
        username=username,
        country_data=country_data,
        lang_data=lang_data,
        lang_keys=lang_keys,
        x1=x1,y1=y1,
        years=years, drama_count=drama_count, comedy_count=comedy_count
    )


# 地图分析表
@app.route('/address_t')
@login_required
def address_t():
    username = session['username']
    x, y = getAddressData()  # 电影拍摄地点统计图
    x1, y1 = getLangData()  # 电影语言统计图
    return render_template('address_t.html', username=username,
                           x=x, y=y, x1=x1, y1=y1)

# 实现类型分析表
@app.route('/type_t')
@login_required
def type_t():
    username = session['username']
    result=getMovieTypeData()
    data=sorted(result, key=lambda x: x['value'], reverse=True)
    top10Data=data[:10]
    return render_template('type_t.html',username=username,top10Data=top10Data)

# 实现导演与演员
@app.route('/actor_t')
@login_required
def actor_t():
    username = session['username']
    x, y = getAllActorMovieNum()  # 导演作品数量前20
    x1, y1 = getAllDirectorMovieNum()  # 演员参演排名前20
    return render_template('actor_t.html', username=username,x=x,y=y,x1=x1,y1=y1)

#数据操做
@app.route('/tables/<int:id>')
@login_required
def tables(id):
    username = session['username']
    tablelist=[]
    if id==0:
        tablelist=getTableList()
    return render_template('tables.html',username=username,tablelist=tablelist)

#实现标题词云
@app.route('/title_c')
@login_required
def title_c():
    username = session['username']
    #调用词云文件中的函数，进行绘制词云
    getTitleImg('title','fas fa-heart','./static/images/title.png')
    return render_template('title_c.html',username=username)

#实现演员名词云
@app.route('/casts_c')
@login_required
def casts_c():
    username = session['username']
    # 调用词云文件中的函数，进行绘制词云
    getCastsImg('casts', 'fab fa-apple', './static/images/casts.png')
    return render_template('casts_c.html', username=username)

# 实现自定义词云
@app.route('/comments_c', methods=['GET', 'POST'])
@login_required
def comments_c():
    username = session['username']
    if request.method == 'GET':  # 不做任何操作
        return render_template('comments_c.html', username=username)
    else:  # POST请求
        searchWord = request.form['searchIpt']
        if not searchWord:
            return redirect(url_for('comments_c'))
        try:
            getCommentsImg('commentContent', searchWord,'fab fa-qq', './static/images/comments.png')
        except Exception as e:
            print(f"生成词云失败:{e}")
            return redirect(url_for('comments_c'))
    return render_template('comments_c.html', username=username)

# 实现大屏可视化界面
@app.route('/analysis1', methods=['GET', 'POST'])
@login_required
def index():
    # 获取首页需要显示的所有信息，并从后台--前端进行展示出来
    allData = getAllData()  # 电影的个数
    allData = len(allData)
    maxRate = getMaxRate()  # 电影最高分数
    typeAll = getTypesAll()  # 电影种类数
    typeAll = len(typeAll)
    maxLang = getMaxLang()[:2]
    data = {
        'allData': allData,
        'maxRate': maxRate,
        'typeAll': typeAll,
        'maxLang': maxLang
    }
    chart_html1 = typeData()
    chart_html2 = yearsData()
    chart_html3 = langData()
    chart_html4 = commentData()
    worldData()
    return render_template('analysis.html',
                           chart_html1=chart_html1,
                           chart_html2=chart_html2,
                           chart_html3=chart_html3,
                           chart_html4=chart_html4,
                           data=data)

@app.route('/bar1')
def bar1():
    return render_template('bar1.html')

# 电影类型统计
def typeData():
    # 读取数据
    data = pd.read_csv('./tools/data/type_counts.csv', encoding='utf-8')
    # [('剧情', 113), ('喜剧', 47), ('冒险', 41), ('奇幻', 38), ('爱情', 34)]
    pie_data = list(zip(data['类型'], data['数量']))
    pie = Pie(init_opts=opts.InitOpts(height='400px', width='500px'))
    pie.add('数量',
            pie_data,
            radius=['30%', '60%'],
            label_opts=opts.LabelOpts(formatter='{b}:{c}个',
                                      font_size=16,
                                      font_style='bold',
                                      color='#0f0')
            )
    # 设置配置项
    pie.set_global_opts(
        title_opts=opts.TitleOpts(title=""),
        tooltip_opts=opts.TooltipOpts(axis_pointer_type='shadow'),
        legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=16,color='#0f0')),

    )
    pie.render('static/html/type_data.html')
    chart_html1 = pie.render_embed()
    return chart_html1

#年份数据量统计
def yearsData():
    # 从CSV文件读取数据
    try:
        # 尝试读取CSV文件
        data = pd.read_csv('./tools/data/year_counts.csv', encoding='utf-8')

        # 验证数据格式（必须包含"年份"和"数量"列）
        if '年份' not in data.columns or '数量' not in data.columns:
            raise ValueError("CSV文件缺少'年份'或'数量'列")

        # 提取数据并转换类型（确保年份为字符串，数量为数值）
        years = data['年份'].astype(str).tolist()
        counts = data['数量'].astype(float).tolist()

        # 验证数据有效性（至少有一组数据）
        if len(years) == 0 or len(counts) == 0:
            raise ValueError("CSV文件中没有有效数据")

        # 验证数据一致性（年份和数量数量必须一致）
        if len(years) != len(counts):
            raise ValueError("年份和数量数据长度不一致")

    except FileNotFoundError:
        # 文件不存在时抛出明确异常
        raise FileNotFoundError("年份数据文件 year_counts.csv 不存在")
    except pd.errors.EmptyDataError:
        # 文件为空时抛出异常
        raise ValueError("CSV文件内容为空")
    except Exception as e:
        # 其他异常统一处理
        raise Exception(f"数据处理失败: {str(e)}")

    # 创建柱状图对象
    bar = Bar(init_opts=opts.InitOpts(height='400px', width='600px'))

    # 添加数据
    bar.add_xaxis(years)
    bar.add_yaxis("电影数量", counts, label_opts=opts.LabelOpts(is_show=True, position="top"))

    # 设置全局配置项
    bar.set_global_opts(
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(
            name="年份",
            axislabel_opts=opts.LabelOpts(rotate=45, interval="auto", font_size=12)
        ),
        yaxis_opts=opts.AxisOpts(
            name="数量",
            axislabel_opts=opts.LabelOpts(formatter="{value} 部")
        ),
        legend_opts=opts.LegendOpts(is_show=False)
    )

    # 优化柱状图样式
    bar.set_series_opts(
        itemstyle_opts=opts.ItemStyleOpts(
            color=lambda x: "#36cbcb" if x % 2 == 0 else "#ff7f0e"  # 蓝橙交替颜色
        ),
        label_opts=opts.LabelOpts(
            font_size=12,
            color="black"
        )
    )

    # 渲染图表到HTML文件
    bar.render("./static/html/years_bar_data.html")
    chart_html2 = bar.render_embed()
    return chart_html2


# 中英文电影占比饼图统计
def langData():
    # 从CSV文件读取数据
    try:
        data = pd.read_csv('./tools/data/lang_counts.csv', encoding='utf-8')

        # 验证数据格式（必须包含"语言"和"数量"列）
        if '语言' not in data.columns or '数量' not in data.columns:
            raise ValueError("CSV文件缺少'语言'或'数量'列")

        # 提取数据并转换类型
        langs = data['语言'].astype(str).tolist()
        counts = data['数量'].astype(int).tolist()

        # 验证数据有效性
        if len(langs) == 0 or len(counts) == 0:
            raise ValueError("CSV文件中没有有效数据")

        if len(langs) != len(counts):
            raise ValueError("语言和数量数据长度不一致")

        # 确保包含中文和英文数据（根据需求调整）
        if '汉语普通话' not in langs or '英语' not in langs:
            raise ValueError("数据中缺少'汉语'或'英语'分类")

    except FileNotFoundError:
        raise FileNotFoundError("语言数据文件 lang_counts.csv 不存在")
    except pd.errors.EmptyDataError:
        raise ValueError("CSV文件内容为空")
    except Exception as e:
        raise Exception(f"语言数据处理失败: {str(e)}")

    # 创建饼图对象
    pie = Pie(init_opts=opts.InitOpts(height='350px', width='400px'))

    # 准备饼图数据
    pie_data = list(zip(langs, counts))

    # 添加数据到饼图
    pie.add(
        "语言占比",
        pie_data,
        radius=["40%", "75%"],  # 环形饼图半径
        label_opts=opts.LabelOpts(
            formatter="{b}: {d}%",  # 显示格式：语言名称 + 百分比
            font_size=14,
            font_weight="bold"
        )
    )

    # 设置全局配置项
    pie.set_global_opts(
        title_opts=opts.TitleOpts(
            title_textstyle_opts=opts.TextStyleOpts(font_size=16)
        ),
        tooltip_opts=opts.TooltipOpts(
            trigger="item",
            formatter="{a} <br/>{b}: {c} ({d}%)"
        ),
        legend_opts=opts.LegendOpts(
            orient="vertical",
            pos_top="15%",
            pos_left="2%",
            textstyle_opts=opts.TextStyleOpts(font_size=12)
        )
    )

    # 设置系列配置项（颜色方案）
    pie.set_series_opts(
        itemstyle_opts=opts.ItemStyleOpts(
            border_width=2,
            border_color="#fff"
        ),
        label_opts=opts.LabelOpts(
            position="outside",
            padding=6,
            font_size=12
        )
    )

    # 渲染图表到HTML文件
    pie.render("./static/html/lang_pie_data.html")
    chart_html3 = pie.render_embed()
    return chart_html3


# 电影评论数折线图统计（仅两列数据）
def commentData():
    # 从comment_counts.csv读取数据
    try:
        data = pd.read_csv('./tools/data/comment_counts.csv', encoding='utf-8')

        # 验证数据格式（必须包含"电影"和"数量"列）
        if '电影' not in data.columns or '数量' not in data.columns:
            raise ValueError("CSV文件缺少'电影'或'数量'列")

        # 提取并转换数据
        movie_names = data['电影'].astype(str).tolist()
        comment_counts = data['数量'].astype(float).tolist()

        # 验证数据有效性
        if len(movie_names) == 0 or len(comment_counts) == 0:
            raise ValueError("CSV文件中没有有效数据")
        if len(movie_names) != len(comment_counts):
            raise ValueError("电影名称和评论数量数据长度不一致")

    except FileNotFoundError:
        raise FileNotFoundError("评论数据文件 comment_counts.csv 不存在")
    except pd.errors.EmptyDataError:
        raise ValueError("CSV文件内容为空")
    except Exception as e:
        raise Exception(f"评论数据处理失败: {str(e)}")

    # 创建折线图对象
    line = Line(init_opts=opts.InitOpts(height='400px', width='700px'))

    # 添加数据（x轴为电影名称，y轴为评论数量）
    line.add_xaxis(movie_names)
    line.add_yaxis(
        "评论数量",
        comment_counts,
        label_opts=opts.LabelOpts(
            is_show=True,
            position="top",
            formatter=lambda x: f"{x:,}"  # 千位分隔符格式化
        )
    )

    # 设置全局配置项
    line.set_global_opts(
        title_opts=opts.TitleOpts(
            title_textstyle_opts=opts.TextStyleOpts(font_size=18)
        ),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(
            name="电影",
            axislabel_opts=opts.LabelOpts(
                rotate=45,
                interval="auto",
                font_size=12
            )
        ),
        yaxis_opts=opts.AxisOpts(
            name="评论数量",
            axislabel_opts=opts.LabelOpts(
                formatter=lambda x: f"{x:,}"  # y轴数值格式化
            )
        ),
        legend_opts=opts.LegendOpts(is_show=False)
    )

    # 优化折线图样式
    line.set_series_opts(
        linestyle_opts=opts.LineStyleOpts(width=3),
        symbol="circle",
        symbol_size=10,
        itemstyle_opts=opts.ItemStyleOpts(color="#3182ce"),  # 蓝色主题
        label_opts=opts.LabelOpts(
            font_size=12,
            color="black"
        )
    )

    # 渲染图表到HTML文件
    line.render("./static/html/comment_line_data.html")
    chart_html4 = line.render_embed()
    return chart_html4

# 实现地球
def worldData():
    data = pd.read_csv('./tools/data/country_counts.csv', encoding='utf-8')
    # [['中国大陆', 87], ['美国', 65], ['中国香港', 21], ['英国', 20], ['日本', 12],
    # ['法国', 10], ['加拿大', 5], ['意大利', 5], ['中国台湾', 4], ['德国', 4]]
    data_list = data.values.tolist()
    # 提供国家地区数据，用于替换原来数据中的国家或地区的名称
    country_name = ['Russia', 'Canada', 'China', 'USA', 'Brazil', 'Australia', 'India', 'Argentina', 'France', 'Japan']
    # 进行替换
    replace_data = []
    for i in range(len(country_name)):
        replace_data.append([country_name[i], data_list[i][1]])
    map = MapGlobe(init_opts=opts.InitOpts(height='500px', width='450px'))
    map.add(maptype='world', series_name='数量', data_pair=replace_data)
    map.set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            min_=0,
            max_=100,
            type_='color',
            range_color=['#0f0', '#0f0'],
        )
    )
    map.render('static/html/map3d.html')

from tools.getData import mainFun
if __name__ == '__main__':
    with app.app_context():
        mainFun()
    app.run(debug=True, port=9898)