import jieba # 结巴分词
import wordcloud # 词云展示库
import collections # 词频统计库
import matplotlib.pyplot as plt
import csv
import pprint
import time
def getText():
    csvfile = open('commentmessage.csv', encoding='utf-8')
    reader = csv.DictReader(csvfile)
    column = [row['content'] for row in reader]
    text = ''.join(str(s.strip()) for s in column if s)
    return text

def display(text):
    # 停用词设置
    stopwords = [line.strip() for line in open('stopwords.txt', 'r', encoding='utf-8').readlines()]
    stopwords = set(stopwords)
    # 文本分词
    print("下面进行词云的生成......")
    seg_list_exact = jieba.cut(text, cut_all=True) # 全模式分词/
    object_list = []
    for word in seg_list_exact: # 循环读出每个分词
        if word not in stopwords:
            object_list.append(word) # 分词追加到列表

    word_pic = wordcloud.WordCloud(
        background_color="white",
        width=800,
        height=500,
        max_words=150, # 设置最大显示的字数
        max_font_size=150, # 设置字体最大值
        min_font_size=10,
        random_state=42, # 随机生成多少种颜色
        relative_scaling = 0.5,
        font_path='C:/Windows/Fonts/simkai.ttf'   # 中文处理，用系统自带的字体
        )
    # 词频统计,对分词做词频统计
    word_counts = collections.Counter(object_list)
    word_pic.generate_from_frequencies(word_counts)

    plt.imshow(word_pic)    # 生成词云
    plt.axis('off')  # 关闭坐标轴

    # 保存图片到指定路径，语句不能写错位置
    plt.savefig(r'D:\Cc\Desktop\Demo\163mc_spider\wordcloud.png')
    plt.show() # 显示图像

if __name__ == '__main__':
    print("正在读取文件......")
    text = getText()
    display(text)


