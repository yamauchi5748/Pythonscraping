import re
import time
import random
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

# スクレイピングClassの実装
class Model():

    def __init__(self, name, root_url, target_url, target_save, target_params, target_contents):
        self.name = name
        self.root_url = root_url
        self.target_url = target_url
        self.target_save = target_save
        self.target_params = target_params
        self.target_contents = target_contents
        self.soup = object
        self.content_list = []

    def run(self):
        #Requestsを使って、webから取得
        res = requests.get(self.target_url)

        #要素を抽出
        self.soup = BeautifulSoup(res.content, 'lxml')

        #HTMLファイルとして保存したい場合はファイルオープンして保存
        with open('files/'+ self.name + '.html', mode='w', encoding = 'utf-8') as fw:
            fw.write(self.soup.prettify())

        #「target_contents」の項目を全て取得
        for target_content in self.target_contents:
            content = target_content['selector']

            # エレメント取得
            elems = self.soup.select(content)

            # 初回のみコンテンツを格納する配列を初期化
            if len(self.content_list) < len(elems):

                # Jsonオブジェクトを取得した要素数分確保
                self.content_list = [ {} for i in range(len(elems)) ]
            
            # 各要素を配列に格納
            self.setContents(elems, target_content['type'], target_content['elem'])
        
        #「params」の項目を各オブジェクトに付与する
        for i in range(len(self.target_params)):
            param = self.target_params[i]
            key = [key for key in param][0]

            for j in range(len(self.content_list)):
                self.content_list[j].update({ key:param[key] })

        
        return self.content_list;
    

    def setContents(self, elems, _type, prop):

        # Jsonオブジェクトに変換しリストに格納する
        for i in range(len(elems)):

            elem = elems[i].getText() if _type == "text" else self.replace(elems[i][_type])
            print(elem)
            
            self.content_list[i].update({ prop:elem })


    def replace(self, item):
        #相対urlを絶対urlに置換するパターン
        pattern = '^http(s)'

        if not re.match(pattern, item):
                
            if not re.match('^/', item):

                item = '/' + item
            item = self.root_url + item
        return item
