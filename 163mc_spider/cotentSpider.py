# -*- coding: utf-8 -*-
# 163mc.spider.py

import base64
import requests
import json
import time
import random
import pymysql
from Crypto.Cipher import AES
from time import sleep
from datetime import datetime
from save import save_to_mysql
from save import save_to_txtfile
from get_music_id import getMusicId


import re
import pprint
# 头部信息
headers = {
    'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
# 设置代理服务器
proxies = {
            'http:':'http://106.111.53.159',
            'https:':'https://111.177.189.148'
        }


# 第二个参数
second_param = "010001" 
# 第三个参数
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
# 第四个参数
forth_param = "0CoJUm6Qyw8W8jud"

# 获取参数，page为传入页数
def get_params(page): 
    iv = b"0102030405060708"#这里b默认后面是16进制字节byte
    first_key = forth_param
    second_key = 16 * 'F'
    if(page == 1): 
        # offset的取值为:(评论页数-1)*20,total第一页为true，其余页为false
        # first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}' # 第一个参数
        first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
        h_encText = AES_encrypt(first_param, first_key, iv)
    else:
        offset = str((page-1)*20)
        first_param = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' %(offset, 'false')
        h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText

# 获取 encSecKey
def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


# 解密过程
def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16

    text = text + (pad *chr(pad))
    #print("解密前", text)
    encryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv) #需要注意的是这里的传参

    text = text.encode('utf-8') # 还需要注意的是这里的text，text是16进制byte格式，要改变一下编码
    encrypt_text = encryptor.encrypt(text) # 如果编码不改变在这里传值，AES自带的encryptor.encrypt()函数会报错
    encrypt_text = base64.b64encode(encrypt_text)
    #print("解密后", str(encrypt_text, encoding="utf-8"))
    return str(encrypt_text, encoding="utf-8")   # 最后传回的值也要格式化成字符串模式，别的也没啥，你自己分析下吧

# 获得评论json数据
def get_json(url, params, encSecKey):
    data = {
         "params": params,
         "encSecKey": encSecKey
    }
    try:
        response = requests.post(url, headers=headers, data=data, proxies=proxies)
    except requests.exceptions.ConnectionError as e:
        print(e)
        return None

    # print(type(response.content))  # <class'bytes'>
    return response.content # 返回字节类型的文件

# 抓取某一首歌的全部评论
def get_all_comments(url):
    all_comments_list = [] # 存放所有评论
    #all_comments_list.append(u"用户ID 用户昵称 用户头像地址 评论时间 点赞总数 评论内容\n") # 头部信息
    setList = set()
    params = get_params(1)
    encSecKey = get_encSecKey()
    json_text = get_json(url, params, encSecKey) # 返回字节类型的文件,
    json_dict = json.loads(json_text) # 把json类型的数据转换成python类型的数据
    comments_num = int(json_dict['total']) # 全部评论总数
    if(comments_num % 20 == 0):
        page = int(comments_num / 20)
    else:
        page = int(comments_num / 20) + 1
    print("共有%d页评论!" % page)
    for i in range(page):  # 逐页抓取
        params = get_params(i+1)
        encSecKey = get_encSecKey()
        json_text = get_json(url,params,encSecKey)
        json_dict = json.loads(json_text) # 返回一个python字典

        if i == 0:
            print("共有%d条评论!" % comments_num) # 全部评论总数
        conn = pymysql.connect(host='localhost',  # mysql服务器地址
                               user='root',  # 用户名
                               passwd='lhf123456',  # 密码
                               db='163music',  # 数据库名
                               charset='utf8')  # 连接编码
        for item in json_dict['comments']:
            data = dict() # 字典类型
            data['content'] = item['content'].strip() # 评论内容 4
            if data['content'] == "":
                continue
            elif data['content'] not in setList:
                setList.add(data['content'])
            else:
                continue
            print("正在抓取评论-", data['content'])

            data['ID'] = item['user']['userId']  # 评论者id
            data['nickname'] = item['user']['nickname'].strip()  # 昵称
            data['likedCount'] = item['likedCount'] # 点赞总数
            data['time'] = datetime.fromtimestamp(item['time']//1000) # 评论时间(时间戳)
            # 保存文件
            # save_to_mysql(data, conn, 0)
            # save_to_csvfile(str(name)+'.csv', data, 0)
        print("第%d页抓取完毕!" % (i+1))

        conn.close()
        if i+1 > 200:
            break
        t = random.randint(0, 5)
        time.sleep(t)

if __name__ == "__main__":
    start_time = time.time() # 开始时间
    music_id = getMusicId()# 爬取歌曲id
    for music in music_id:
        print("对歌曲《", music['name'], "》的评论进行爬取......")
        url = "https://music.163.com/weapi/v1/resource/comments/R_SO_4_" + music['id'] + "?csrf_token="
        print("url = ", url)
        sleep(2)
        get_all_comments(url)


    