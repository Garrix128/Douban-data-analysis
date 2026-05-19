from pyecharts.charts import *
from pyecharts import options as opts

# 实现一个柱状图
x = ['广东', '广西', '贵州', '湖南', '湖北', '江西']
y = [123, 145, 56, 77, 168, 101]
# 创建对象的写法
bar = (
    Bar()
    .add_xaxis(x)
    .add_yaxis('省份', y)
    .set_global_opts(
        title_opts=opts.TitleOpts(title='各省份的销售情况',
                                  title_textstyle_opts=opts.TextStyleOpts(font_size=20, color='#0f0'),
                                  pos_left='center'),
        xaxis_opts=opts.AxisOpts(name='地区', name_gap=50, name_location='middle'),
        yaxis_opts=opts.AxisOpts(name='数量', name_gap=50, name_location='middle'),
        legend_opts=opts.LegendOpts(is_show=True, pos_left='left')
    )
)
bar.render('bar2.html')
