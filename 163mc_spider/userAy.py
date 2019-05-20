import pymysql
import pandas as pd
from pyecharts import Bar,Pie,Line,Scatter,Map

def getText():
    conn = pymysql.connect(host='localhost',  # mysql服务器地址
                           user='root',  # 用户名
                           passwd='lhf123456',  # 密码
                           db='163music',  # 数据库名
                           charset='utf8')  # 连接编码
    sql = 'select id,age,city FROM usermessage'
    text = pd.read_sql(sql, con=conn)
    return text

def analysis(user):
    # 用户年龄分布分析
    print("正在进行用户年龄分析......")
    age = user[user['age'] > 0]  # 清洗掉年龄小于1的数据
    age = age.id.groupby(age['age']).count()  # 以年龄值对数据分组
    bar = Bar('用户年龄分布')
    bar.add(
        '',
        age.index.values,
        age.values,
        is_fill=True,
    )
    bar.render(r'./用户年龄分布图.html')  # 生成渲染的html文件

    # 用户地区分布分析
    print("正在进行用户地域分析......")
    user['city'] = user['city'].apply(city_group)
    city = user.id.groupby(user['city']).count()
    map = Map('用户地区分布图', width=1200, height=600)
    attrs = city.index.values
    values = city.values
    map.add(
        '用户地区分布图',
        attrs,
        values,
        maptype='china',
        is_visualmap=True,
        visual_text_color='#000',
        is_label_show=True,
        visual_range=[0, 400]
    )
    map.render(r'./用户地区分布图.html')

# 城市code编码转换
def city_group(cityCode):
    cityCode = str(cityCode)
    city_map = {
        '11': '北京',
        '12': '天津',
        '31': '上海',
        '50': '重庆',
        '5e': '重庆',
        '81': '香港',
        '82': '澳门',
        '13': '河北',
        '14': '山西',
        '15': '内蒙古',
        '21': '辽宁',
        '22': '吉林',
        '23': '黑龙江',
        '32': '江苏',
        '33': '浙江',
        '34': '安徽',
        '35': '福建',
        '36': '江西',
        '37': '山东',
        '41': '河南',
        '42': '湖北',
        '43': '湖南',
        '44': '广东',
        '45': '广西',
        '46': '海南',
        '51': '四川',
        '52': '贵州',
        '53': '云南',
        '54': '西藏',
        '61': '陕西',
        '62': '甘肃',
        '63': '青海',
        '64': '宁夏',
        '65': '新疆',
        '71': '台湾',
        '10': '其他',
    }
    print("")
    return city_map[cityCode[:2]]

if __name__ == '__main__':
    text = getText()
    analysis(text)
