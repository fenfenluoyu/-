import requests
import re
import pprint
from urllib import request, parse
from lxml import etree

headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://music.163.com/',
        'Cookie': 'P_INFO="lihuifen_china@163.com|1554896764|0|unireg|00&99|null&null&null#hen&410500#10#0#0|&0||lihuifen_china@163.com"; mail_psc_fingerprint=58a355417d5c49313c492717465682a1; _iuqxldmzr_=32; _ntes_nnid=18037a37e6cd5e66bef0d6f5591a0a45,1554896864410; _ntes_nuid=18037a37e6cd5e66bef0d6f5591a0a45; WM_TID=YSB2Ec8LIhtFVREUVVIp2BQ6Bxt8RBpN; usertrack=CrHtflyt1+1o/IvAAwWHAg==; WM_NI=ZqdBmHEC11uH11ce%2BG7KsPpCORLBwRYzDpECPzsXFBpomQnXFBoyrqou4QnohT%2F%2Fr%2F4Lvd9%2FXzhWkb2AxGkcfQpLlOy1Q7yswa85vU%2FlJ1xxiLzyIEK%2BFQwfnqSjtpZueGU%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea3d84aa99f0099ef688def8ab6d54f879e9b85b7679597af8ac25b949a8882ec2af0fea7c3b92a9aafaca3f044879dffd2f844f3efad86aa4df595bdb1f3498d8e84a3f65a9ba68c91c84994a6bdb9c54ab4b1a3b2ed54869ea19af17badabfcb2ed65ac8ce1d0f125f894ba85bc259ca6a8b8ea6af29fb8a8ea69a68fc0adef45bbef9fd8fc79b5bff8d6f55fedb486d2fb74ab94b69acc4f89f58ab2f66eaeaf9d8bf77c9aababa8d837e2a3; JSESSIONID-WYYY=HTHfvdRPTtMmrGHankcfx%5CSUwpkhXYeCp%2BMfabIESxQTnjeIW7RI1GFiPy8yUjeDiCMHgSnPlog%5CHEnSsbKHF3ruw9Dm2A3p8YDB2S9NXsNFJV%2FpfY7kkBOkbsY%2Fs83T0vn6vtTDBf6mrODwUiD%2B4s7Bba70XJH%2BpVcw0KqzAEP6veFT%3A1556190190505'
    }
def getMusicId():
    print("正在爬取热门歌曲id......")
    url = "https://music.163.com/discover/toplist?id=3778678"
    res = request.Request(url, headers = headers)
    response = request.urlopen(res)
    html = response.read().decode('utf-8')
    # pprint.pprint(html)
    selector = etree.HTML(html)
    list = selector.xpath('//*[@class="f-hide"]/li')
    # print(list)
    regex = re.compile(r'(.*)=')
    item = dict()
    url_list = []
    for sel in list:  # 获取专辑的id
        item['name'] = sel.xpath('a/text()')[0]
        str = sel.xpath('a/@href')[0]
        item['id'] = regex.sub("", str)
        # print(item)
        url_list.append(item.copy())
    return url_list

# if __name__ == "__main__":
#     list = getMusicId()
"""
'//*[@id="13458480981556181977796"]/td[2]/div/div/div/span/a'
'//*[@id="13579998941556181977796"]/td[2]/div/div/div/span/a'
//*[@id="13595955201556187213304"]/td[2]/div/div/div/span/a/b/text()[1]
//*[@id="13595955201556187213304"]/td[2]/div/div/div/span/a/b/text()[2]
"""