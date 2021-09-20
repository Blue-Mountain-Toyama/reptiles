import re
import urllib
import urllib.request
import urllib.parse
import requests
from bs4 import BeautifulSoup
print("test")
# word encoder function
def w_encode():
    print("enter the key-word : ")
    w_raw = input()
    # encode the word
    w_quote = urllib.parse.quote(w_raw)
    return(w_quote)


linklist = []
while 1:
    word = w_encode()
    url = 'https://www.irasutoya.com/search?q=' + str(word)
    # 検索結果ページのhtmlを取得
    html = requests.get(url).text
    # 検索結果ページのオブジェクトを作成
    soup = BeautifulSoup(html, 'lxml')
    # 画像タグを取り出す(select_one で１つだけ)
    a_list =soup.select('div.boxmeta.clearfix > h2 > a')
    if len(a_list) != 0:
        print("Image was taken from : {}".format(url))
        break



#　画像リンクを取り出す
for a in a_list:
    link_url = a.attrs['href']
    linklist.append(link_url)

# linklistから画像ファイル１つを取ってくるまでループ
for page_url in linklist:
    html = requests.get(page_url).text
    # 先ほど作成した画像リンクリストから各画像リンクを取得
    soup = BeautifulSoup(html, "lxml")
    # Webページのソースコードをパース
    link = soup.select_one('div.entry > div > a > img')
    #img の URL が無かったらこのループをskip
    if link is None:
        print('link is NoneType')
        continue
    img_url = (link.attrs['src'])
    # URLの頭にhttp:がついているかチェック
    if img_url.find('https:') == -1 and img_url.find('http:') == -1:
        print("http: was added.")
        img_url = 'http:' + img_url
    #画像ファイルの名前を抽出
    filename = re.search(".*\/(.*png|.*jpg)$",img_url)
    print('img URL was captured at : {}'.format(img_url))
    try:
        #画像ファイルのデータを取得
        image = requests.get(img_url)
        #保存先のファイルパスを生成
        save_path = "/static/img/scraper/" + str(filename.group(1))
        #出力フォルダにデータを保存
        open(save_path , 'wb').write(image.content)
        print('saved file name:' + str(filename.group(1)))
    except ValueError:
        print("ValueError!!")
    break







"""""
参考サイト
・https://qiita.com/japanesebonobo/items/eb374a94ed0456c88ed7

・https://hashikake.com/scraping_img


"""""
#post > div.entry > p:nth-child(1) > a > img
#post > div.entry > div:nth-child(2) > a:nth-child(1) > img
#post > div.entry > p:nth-child(1) > a > img
#memo : need to separate the cases of p and div