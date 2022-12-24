import sys
from PyQt6 import QtWidgets,QtGui
from PyQt6.QtWidgets import *
import os
import download_line_image
import configparser



class MainWindow(QTabWidget):
    def __init__(self):
        super().__init__()
        self.getConfig()
        self.initUi()
    def initUi(self):
        self.setWindowTitle('Line表情贴纸下载器')
        self.table1 = QWidget()
        self.table2 = QWidget()
        self.addTab(self.table1,'下载设置')
        self.addTab(self.table2,'代理设置')
        self.mainTableInit()
        self.proxyTableInit()
        self.resize(300,200)
    def getConfig(self):
        self.save_path, self.proxies = download_line_image.getConfig()
        
    #代理页面设置
    def proxyTableInit(self):
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
        if self.proxies['http'] != '':
            line01.setText(self.proxies['http'].split('//')[1].split(':')[0])
            line02.setText(self.proxies['http'].split('//')[1].split(':')[1])
        def setProxy():
            self.proxies = {
                'http':'http://'+line01.text()+':'+line02.text(),
                'https':'https://'+line01.text()+':'+line02.text()
            }
        line02.editingFinished.connect(setProxy)
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
        fromlayout = QFormLayout()

        self.table2.setLayout(layout4)
    #主页面设置
    def mainTableInit(self):
            #设置lab
            lab01 = QLabel()
            lab01.setText('请输入需要下载的表情贴纸合集网址')
            lab01.setFont(QtGui.QFont('微软雅黑', 12))
            lab02 = QLabel()
            lab02.setText('存储路径:\n./download')
            #设置line(输入框)
            line01 = QLineEdit()
            #设置按钮
            
            choosePathBtn = QPushButton()
            choosePathBtn.setText('选择路径')

            def changePath():
                save_path = os.path.abspath(QFileDialog.getExistingDirectory(None, "getExistingDirectory", "./"))
                lab02.setText('存储路径:\n'+save_path)
            choosePathBtn.clicked.connect(changePath)

            confrimBtn = QPushButton()
            confrimBtn.setText('确定')
            def confrim():
                self.getConfig()
                try:
                    download_line_image.download(line01.text(),self.save_path,self.proxies)
                    QMessageBox.information(self, "提示", "下载完成", QMessageBox.StandardButton.Ok)
                except download_line_image.MaxConnectionError:
                    QMessageBox.information(self, "提示", "下载失败,链接超时", QMessageBox.StandardButton.Ok)
            confrimBtn.clicked.connect(confrim)
            #设置布局
            layout1 = QVBoxLayout()
            layout1.addWidget(lab01)
            layout1.addWidget(line01)
            layout1.addWidget(confrimBtn)
            layout2 = QVBoxLayout()
            layout2.addWidget(lab02)
            layout2.addWidget(choosePathBtn)
            vlayout = QVBoxLayout()
            vlayout.addLayout(layout1)
            vlayout.addLayout(layout2)
            self.table1.setLayout(vlayout)
    def saveConfig(self):
        
        config = configparser.ConfigParser()
        config['option'] = {
            'save_path':self.save_path,
        }
        config['proxy'] = {
            'http':self.proxies['http'],
            'https':self.proxies['https']
        }
        with open('config.ini','w') as configfile:
            config.write(configfile)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    webWgt = MainWindow()
    webWgt.show()
    sys.exit(app.exec())