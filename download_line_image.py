from email import header
from msilib import type_binary
import sys
from wsgiref import headers
import requests
from bs4 import BeautifulSoup
import os
import re
from PyQt6 import QtWidgets,QtGui
from PyQt6.QtWidgets import *
#前置的一些参数
agent = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.36'
}
proxies = {
    'http':'127.0.0.1:10809',
    'https':'127.0.0.1:10809'
}
url1 = 'https://store.line.me/stickershop/product/12126860/zh-Hans'
url2 = 'https://store.line.me/stickershop/product/1265244/zh-Hans'
save_path = os.path.join(os.getcwd(),'download')
def writeToFile(item,path,opt):
    '写入函数'
    if opt=='bin':
        with open(path,'wb') as file:
            file.write(item.content)
    elif opt=='str':
        with open(path,'w',encoding='utf-8') as file:
            for line in item.text.split('><'):
                file.write("<"+line+">\n")

def creatProductDir(url):
    '获取合集的id并创建文件夹'
    matchId = re.search(re.compile(
        'https://store.line.me/stickershop/product/(?P<id>.*)/*.*'
    ),url).group('id')
    path = os.path.join(save_path,matchId)
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        print("该储存目录已经存在,请勿重复下载!")
        selection = input("仍要使用这个目录吗?请输入y:") or "n"
        if selection == 'y':
            pass
        else:
            sys.exit()
    return path
def download(url):
    index = requests.get(url,stream=True,timeout=10,proxies=proxies,headers=agent)
    index = BeautifulSoup(index.content,'html.parser')
     #把找到的每个图片下载并且写入
    for link in index.find_all(class_='mdCMN09LiInner FnImage'):
        imgPathRE = re.search(
            re.compile(
                "https://stickershop.line-scdn.net/stickershop/v1/sticker/(?P<id>.*)/(android|iphone)/sticker.png"
                    ),str(link.contents[1]))
        img = requests.get(imgPathRE.group(),proxies=proxies,timeout=10)
        writeToFile(img,os.path.join(save_path,imgPathRE.group('id')+'.png'),'bin')




class window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()
    def initUi(self):
        #设置lab
        lab01 = QLabel()
        lab01.setText('请输入需要下载的表情贴纸合集网址')
        lab01.setFont(QtGui.QFont('微软雅黑', 12))
        lab02 = QLabel()
        lab02.setText('存储路径:./download')
        lab03 = QLabel()
        lab03.setText('设置代理')
        #设置勾选框
        check01 = QCheckBox()
        
        #设置line(输入框)
        line01 = QLineEdit()
        #设置按钮
        confrimBtn = QPushButton()
        confrimBtn.setText('确定')
        confrimBtn.clicked.connect(lambda: download(self.line01.text()))
        choosePathBtn = QPushButton()
        choosePathBtn.setText('选择路径')
        def changePath():
            save_path = os.path.abspath(QFileDialog.getExistingDirectory(None, "getExistingDirectory", "./"))
            lab02.setText('存储路径:'+save_path)
        choosePathBtn.clicked.connect(changePath)
        proxyBtn = QPushButton()
        proxyBtn.setText('设置代理')
        def setProxy():
            if check01.isChecked():
                proxies = {
                    'http':line01
                }
        proxyBtn.clicked.connect(setProxy)
        #设置布局
        layout1 = QVBoxLayout()
        layout1.addWidget(lab01)
        layout1.addWidget(line01)
        layout1.addWidget(confrimBtn)
        layout2 = QHBoxLayout()
        layout2.addWidget(lab02)
        layout2.addWidget(choosePathBtn)
        layout3 = QHBoxLayout()
        layout3.addWidget(lab03)
        layout3.addWidget(check01)
        vlayout = QVBoxLayout()
        vlayout.addLayout(layout1)
        vlayout.addLayout(layout2)
        #窗口设置
        self.setLayout(vlayout)
        self.setWindowTitle("下载表情贴纸")

class ProxyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()
    def initUi(self):
        #设置lab
        lab01 = QLabel()
        lab01.setText('请输入代理ip')
        lab01.setFont(QtGui.QFont('微软雅黑', 12))
        lab02 = QLabel()
        lab02.setText('请输入代理端口')
        lab02.setFont(QtGui.QFont('微软雅黑', 12))
        #设置line(输入框)
        line01 = QLineEdit()
        line02 = QLineEdit()
        #设置按钮
        confrimBtn = QPushButton()
        confrimBtn.setText('确定')
        def setProxy():
            global proxies
            proxies = {
                'http':'http://'+line01.text()+':'+line02.text(),
                'https':'https://'+line01.text()+':'+line02.text()
            }
            self.close()
        confrimBtn.clicked.connect(setProxy)
        #设置布局
        layout1 = QVBoxLayout()
        layout1.addWidget(lab01)
        layout1.addWidget(line01)
        layout2 = QVBoxLayout()
        layout2.addWidget(lab02)
        layout2.addWidget(line02)
        layout3 = QHBoxLayout()
        layout3.addLayout(layout1)
        layout3.addLayout(layout2)
        layout4 = QVBoxLayout()
        layout4.addLayout(layout3)
        layout4.addWidget(confrimBtn)
        #窗口设置
        self.setLayout(layout4)
        self.setWindowTitle("设置代理")
        self.show()

if __name__ == '__main__':
    #输入参数
    app = QApplication(sys.argv)
    webWgt = window()
    webWgt.show()
    sys.exit(app.exec())
    url = input("请输入要下载的表情贴纸合集网址:")
    
    selection = input("需要更改存储路径吗?需要请输入y(默认路径E:\download\line):") or 'n'
    if selection == 'y':
        save_path = os.path.abspath(input('请输入保存路径(绝对):'))
    selection = input('需要更换代理端口吗?需要请输入y(默认代理127.0.0.1:10809):') or 'n'
    if selection == 'y':
        proxies.clear()
        proxies['http'] = input('输入http:')
        proxies['https'] = input('输入https:')
    
    save_path = creatProductDir(url)
   
