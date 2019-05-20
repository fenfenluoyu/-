import pprint
import json
import pymysql
import random
import time
from urllib import request
from save import save_to_mysql

headers = {
    'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
  }
ROOT_URL = 'https://music.163.com/api/v1/user/detail/'

def getID():
    conn = pymysql.connect(host='localhost',  # mysql服务器地址
                           user='root',  # 用户名
                           passwd='lhf123456',  # 密码
                           db='163music',  # 数据库名
                           charset='utf8')  # 连接编码
    cursor = conn.cursor()
    sql = 'select userId from commentmessage where id>36000 and id<37000'
    try:
        cursor.execute(sql)
        res = cursor.fetchall()
        return res
    except Exception as e:
        print("Error ! ", e)
    finally:
        cursor.close()
        conn.close()
    return None

setList = set()
def getData(url):
    print('url =  ', url)
    try:
        req = request.Request(url, headers = headers) # 发送请求
        content = request.urlopen(req).read().decode('utf-8') # 信息获取
        userMg = json.loads(content) # 对获取的信息进行解析

        info = {} # 提取信息，存入字典
        info['userName'] = userMg['profile']['nickname']
        if info['userName'] not in setList: # name查重
            setList.add(info['userName'])
        else:
            return

        if int(userMg['profile']['birthday']) < 0: # 年龄小于0的用户信息不存
            return
        else:
            info['age'] = (2018-1970)-(int(userMg['profile']['birthday'])//(1000*365*24*3600))
            if int(info['age']) <= 3:
                return

        info['gender'] = userMg['profile']['gender']
        if info['gender'] == 1:
            info['gender'] = 'female'
        elif info['gender'] == 2:
            info['gender'] = 'male'
        else:
            info['gender'] = 'none'
        info['city'] = userMg['profile']['city']
        info['listenSongs'] = userMg['listenSongs']
        print('正在爬取用户" 【',
              info['userName'], '】 "的信息 :',
              ' gender:', info['gender'],
              ' age:', info['age'],
              ' city:', info['city'],
              ' songsNumber: ', info['listenSongs']
              )
        global f
        f = 1
        return info
    except Exception as e:
        print("Error : ", e)
    return None


if __name__ == '__main__':
    userID= getID() # 返回元组
    ID = list(userID)
    conn = pymysql.connect(host='localhost',  # mysql服务器地址
                           user='root',  # 用户名
                           passwd='lhf123456',  # 密码
                           db='163music',  # 数据库名
                           charset='utf8')  # 连接编码

    for i in ID:
        f = 0
        id = str(i[0])
        data = getData(ROOT_URL+id.strip())
        if f:
            # save_to_mysql(data, conn, 1)
            t = random.uniform(0.1, 3.0)
            time.sleep(t)
        else:
            print("用户信息不合格")
    conn.close()



'''
 1 女
 2 男
'''
