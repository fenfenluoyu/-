# 情感分析以表格形式展示
import pymysql
import pandas as pd
from snownlp import SnowNLP
from pyecharts import Bar, Pie, Line, Scatter, Map


def getText():
    print("正在提取信息......")
    conn = pymysql.connect(host='localhost',  # mysql服务器地址
                           user='root',  # 用户名
                           passwd='lhf123456',  # 密码
                           db='163music',  # 数据库名
                           charset='utf8')  # 连接编码
    sql = 'select id,content FROM commentMessage'
    dic = pd.read_sql(sql, con=conn)
    # print(type(dic))
    return dic

def getSemi(text):
    print("正在进行情感分析......")
    x = ["0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"]
    feel = text
    f = lambda x: round(SnowNLP(x).sentiments, 1)
    feel['content'] = feel['content'].apply(f)
    semiscore = feel.id.groupby(feel['content']).count()
    y = semiscore.values
    print(y)
    pie = Pie("情感比例分析")
    pie.add(
        "",
        x,
        y,
        is_label_show=True
    )
    pie.render(r'情感得分分析.html')
    print("标签生成成功......")
    print("正在生成评论情感标签图表......")
    text['content'] = text['content'].apply(lambda x: round(SnowNLP(x).sentiments, 2))
    text['content'] = text['content'].apply(lambda x:"积极乐观" if x>0.6 else "低沉伤感")
    semilabel = text.id.groupby(text['content']).count()
    bar = Bar('评论情感标签')
    # bar.use_theme('dark')
    bar.add(
        '',
        y_axis = semilabel.values,
        x_axis = semilabel.index.values,
        is_fill=True,
    )
    bar.render(r'情感标签分析.html')
    print("标签生成成功......")


if __name__ == '__main__':
    text = getText()
    getSemi(text)



