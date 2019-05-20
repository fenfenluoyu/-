# 情感分析以表格形式展示
import pymysql
import pandas as pd
from snownlp import SnowNLP
from pyecharts import Bar,Pie,Line,Scatter,Map


def getText():
    conn = pymysql.connect(host='localhost',  # mysql服务器地址
                           user='root',  # 用户名
                           passwd='lhf123456',  # 密码
                           db='163music',  # 数据库名
                           charset='utf8')  # 连接编码
    sql = 'select id,time,content FROM commentMessage'
    dic = pd.read_sql(sql, con=conn)
    # print(type(dic))
    return dic

def getTime(text):

    # 评论时间(按小时)分布分析
    try:
        comments_hour = text
        comments_hour['time'] = comments_hour['time'].dt.hour
        data = comments_hour.id.groupby(comments_hour['time']).count()
        line = Line('评论时间(按小时)分布')
        # line.use_theme('dark')
        line.add(
            '',
            data.index.values,
            data.values,
            is_fill=True,
        )
        line.render(r'./评论时间(按小时)分布.html')
    except:
        pass

if __name__ == '__main__':
    text = getText()
    getTime(text)


