# -*- coding = utf-8 -*-
# @Time : 2021/7/25 14:38
# @Author : Alex Qiu
# @File : downloader.py
# @Software: PyCharm

import os
import pandas as pd
from urllib.request import urlretrieve
import re

import requests


def download(downloadDF):
    n = len(downloadDF)
    linkFormula = re.compile('(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]')
    for i in range(0, n - 1):
        link = downloadDF.iloc[i, 2][1:-1]
        linkString = str(downloadDF.iloc[i, 2][1:-1])
        tempList = linkString.split("\'")
        idString = str(downloadDF.iloc[i, 0])
        linkListLen = len(tempList)
        if linkListLen == 1:
            print(idString + "，id没有图片。")
        else:
            linkCount = 0
            for k in range(1,linkListLen):
                matchObject = linkFormula.search(tempList[k])
                if matchObject is not None:
                    linkCount = linkCount + 1
                    print(idString + "，正在下载图片...")
                    download_img(matchObject.group(0),i)
                    urlretrieve(matchObject.group(0), './image/img'+ str(i) + '.png')
                    print(idString + "，图片下载完成，" + "共" + str(linkCount) + "张图片.")

def download_img(img_url,i):
    print(img_url)
    header = {'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
              '537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    r = requests.get(img_url, headers=header, stream=True)
    print(r.status_code) # 返回状态码
    if r.status_code == 200:
        open('./image/img'+ str(i) + '.png', 'wb').write(r.content) # 将内容写入图片
    del r



def downloadlistfetcher(path):
    csvData = pd.read_csv(path)
    dfData = pd.DataFrame(csvData)
    downloadDict = []
    downloadList = pd.DataFrame(downloadDict)
    downloadList[['ID', 'Date', 'Link']] = dfData[['id', 'date', 'photos']]
    return downloadList


def checkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print('路径不存在，创建成功')
        return True
    else:
        print('路径已存在')
        return False


if __name__ == '__main__':
    downloadPath = 'E:\WorkSpace\Python\Twint\data\italy\event1_pic'
    readPath = 'E:\WorkSpace\Python\Twint\data\italy\event1\event1.csv'
    checkdir(downloadPath)
    downloadDF = downloadlistfetcher(readPath)
    download(downloadDF)
