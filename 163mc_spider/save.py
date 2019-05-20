import csv
import re
import pymysql
import pprint

# 将评论写入mysql
def save_to_mysql(item, conn, f):
    cur = conn.cursor()
    try:
        if f == 0: # 插入评论信息表,去除表情符号与英文
            item['content']= filter_emoji(item['content'])
            item['content'] = re.sub(r'[a-zA-Z]', "", item['content'])
            if item['content'] == "":
                return
            sql = "INSERT INTO commentMessage(userId, nickname, likedCount, content, time) VALUES (%s,%s,%s,%s,%s)"
            cur.execute(sql, (item['ID'], item['nickname'], item['likedCount'], item['content'], item['time']))
        else:  # 用户信息表
            sql = "INSERT INTO usermessage(userName, gender, age, city, songNumber) VALUES (%s,%s,%s,%s,%s)"
            cur.execute(sql, (item['userName'], item['gender'], item['age'], item['city'], item['listenSongs']))
        print('保存成功！')
    except:
        print('保存出错！')
    finally:
        cur.connection.commit()
        cur.close()
    #     conn.close()

def save_to_csvfile(filename, item, c):
    # print(filename)
    csvFile = open(filename, 'a', encoding='gbk')
    csv_writer = csv.writer(csvFile)
    if c == 1:
        csv_writer.writerow(['userId', 'nickname', 'likedCount', 'content', 'time'])
    try:
        csv_writer.writerow((item['ID'], item['nickname'], item['likedCount'], item['content'], item['time']))
        print("写入文件成功!")

    except:
        print("写入文件失败")
    # csv_writer.close()

def save_to_txtfile(filename, content):
    txtFile = open(filename, 'a', encoding='utf-8')
    try:
        txtFile.write(content)
        print("写入文件成功")
    except:
        print("写入文件失败")
    txtFile.close()

def filter_emoji(desstr):
    '''
    过滤表情
    '''
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(r'', desstr)