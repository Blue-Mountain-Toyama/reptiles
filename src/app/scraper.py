import re, os
import urllib
import urllib.request
import urllib.parse
import requests
from bs4 import BeautifulSoup
import pathlib

def scraper(input):
    linklist = []
    while 1:
        word = urllib.parse.quote(input)
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
        else:
            word = urllib.parse.quote("なつやすみ")
            url = 'https://www.irasutoya.com/search?q=' + str(word)
            # 検索結果ページのhtmlを取得
            html = requests.get(url).text
            # 検索結果ページのオブジェクトを作成
            soup = BeautifulSoup(html, 'lxml')
            # 画像タグを取り出す(select_one で１つだけ)
            a_list =soup.select('div.boxmeta.clearfix > h2 > a')
            break


    # 画像リンクを取り出す
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
            save_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/static/img/illustration/" + str(filename.group(1))
            #出力フォルダにデータを保存
            open(save_path , 'wb').write(image.content)
            return str(filename.group(1))
        except ValueError:
            return 'error'
        break
