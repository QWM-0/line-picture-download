import sys
import requests
from bs4 import BeautifulSoup
import os
import re
import configparser

#前置的一些参数
agent = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.36',
    'Connection':'close',
}

def writeToFile(item,path,opt):
    '写入函数'
    if opt=='bin':
        with open(path,'wb') as file:
            file.write(item.content)
    elif opt=='str':
        with open(path,'w',encoding='utf-8') as file:
            for line in item.text.split('><'):
                file.write("<"+line+">\n")

def createSavePath(path):
    '创建存储路径'
    if not os.path.exists(path):
        os.mkdir(path)

def download(url,save_path,proxies):
    '把找到的每个图片下载并且写入'
    #生成合集id和存储路径
    matchId = re.search(re.compile(
        'https://store.line.me/stickershop/product/(?P<id>.*)//*.*'
    ),url).group('id')
    path = os.path.join(save_path,matchId)
    createSavePath(path)
    #获取网页源码
    session = requests.Session()
    session.keep_alive = False
    requests.adapters.DEFAULT_RETRIES = 5
    try:
        index = requests.get(url,stream=True,timeout=10,proxies=proxies,headers=agent)
    except requests.exceptions.SSLError as e:
        print(e)
        raise MaxConnectionError('连接超时')
    index = BeautifulSoup(index.content,'html.parser')
    #获取图片的url并下载
    for link in index.find_all(class_='mdCMN09LiInner FnImage'):
        imgPathRE = re.search(
            re.compile(
                "https://stickershop.line-scdn.net/stickershop/v1/sticker/(?P<id>.*)/(android|iphone)/sticker.png"
                    ),str(link.contents[1]))
        img = requests.get(imgPathRE.group(),proxies=proxies,timeout=10)
        writeToFile(img,os.path.join(path,imgPathRE.group('id')+'.png'),'bin')

def getConfig():
    config = configparser.ConfigParser()
    if not os.path.exists(os.getcwd() + '/config.ini'):
        with open(os.getcwd() + '/config.ini','w',encoding='utf-8') as file:
            file.write('[option]' + '\n' + 'save_path = ' + '\n' + '[proxy]' + '\n' + 'http = ' + '\n' + 'https = ')
    config.read(os.getcwd() + '/config.ini',encoding='utf-8')
    if config.get('option','save_path') != '':
        save_path = config.get('option','save_path')
    else:
        save_path = os.path.join(os.getcwd(),'download')
        createSavePath(save_path)
    proxies = {
    'http':'',
    'https':''
    }
    for key in proxies.keys():
        if config.get('proxy',key) != '':
            proxies[key] = config.get('proxy',key)
    return save_path,proxies

class MaxConnectionError(Exception):
    pass

if __name__ == '__main__':
    #输入参数
    # @param url:表情贴纸合集网址
    # @param save_path:存储路径
    # @param proxies:代理
    url = 'https://store.line.me/stickershop/product/12126860/en?from=sticker'
    save_path,proxies = getConfig()
    proxies = {
    'http':'127.0.0.1:10809',
    'https':'127.0.0.1:10809'
    }
    download(url,save_path,proxies)