# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SpiderBot.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import urllib.request,urllib.parse,urllib.error
from bs4 import BeautifulSoup as soup
import pandas as pd
import re
import os

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(640, 580)
        Form.setMinimumSize(QtCore.QSize(640, 580))
        Form.setMaximumSize(QtCore.QSize(640, 580))
        Form.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 16, 16))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(230, 170, 211, 81))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(115, 210, 22);")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(50, 280, 321, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(32, 74, 135);")
        self.label_3.setObjectName("label_3")
        self.IMDb = QtWidgets.QRadioButton(Form)
        self.IMDb.setGeometry(QtCore.QRect(60, 330, 191, 23))
        self.IMDb.setCheckable(True)
        self.IMDb.setChecked(False)
        self.IMDb.setObjectName("IMDb")
        self.amazon = QtWidgets.QRadioButton(Form)
        self.amazon.setGeometry(QtCore.QRect(60, 360, 112, 23))
        self.amazon.setObjectName("amazon")
        self.csvCrawl = QtWidgets.QPushButton(Form)
        self.csvCrawl.setGeometry(QtCore.QRect(60, 420, 281, 25))
        self.csvCrawl.setObjectName("csvCrawl")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(60, 480, 281, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(450, 530, 121, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(190, 10, 331, 161))
        self.label.setMaximumSize(QtCore.QSize(500, 500))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Images/crawler2.jpeg"))
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        #---------Adding functionality------------
        self.csvCrawl.clicked.connect(self.csvSave)
        self.pushButton.clicked.connect(self.excelSave)
        self.pushButton_2.clicked.connect(Form.close)



    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "SpiderBot"))
        self.label_3.setText(_translate("Form", "Choose the website to crawl"))
        self.IMDb.setText(_translate("Form", "IMDb"))
        self.amazon.setText(_translate("Form", "Amazon"))
        self.csvCrawl.setText(_translate("Form", "Crawl and save in csv"))
        self.pushButton.setText(_translate("Form", "Crawl and save in excel"))
        self.pushButton_2.setText(_translate("Form", "Exit"))




    def csvSave(self):
    	self.pushButton.setEnabled(False)
    	if self.amazon.isChecked():
    		page=1
    		
    		df={'title':[],'author':[],'rating':[],'price':[]}
    		i=1
    		while page<3:
    			url ="https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_pg_{p}?_encoding=UTF8&pg={p}".format(p=page)
    			
    			try:
    				conn = urllib.request.urlopen(url)
    			except urllib.error.URLError as e:
    				print("Connection fail")
    				Form.close()
    			html_data=conn.read()
    			conn.close()
    			soupData = soup(html_data,"html.parser")
    			items = soupData.findAll('span',{"class":"aok-inline-block zg-item"})
    			
    			for item in items:
    				title = item.find('div',{'class':'p13n-sc-truncate p13n-sc-line-clamp-1'}).text.strip()
    				author = item.find('a',{'class':'a-size-small a-link-child'})
    				if author is None:
    					author = item.find('span',{'class':"a-size-small a-color-base"})
    				author = author.text.strip()
    				rating = item.find('span',{'class':"a-icon-alt"})
    				if rating is None:
    					rating=' '
    				else:
    					rating=rating.text.strip()
    				price = item.find('span',{'class':"p13n-sc-price"}).text.strip()
    				df['title'].append(title)
    				df['author'].append(author)
    				df['rating'].append(rating)
    				df['price'].append(price)
    				i+=1
    			page+=1
    		pd.DataFrame(df).to_csv('books.csv',index_label='index')
    		msg_box= QtWidgets.QMessageBox()
    		msg_box.setText("Completed!!!!")
    		msg_box.exec_()

    	elif self.IMDb.isChecked():
    		page_no=1
    		df={"Name":[],"Role":[],"Movie":[]}
    		while page_no<=201:
	    		url="https://www.imdb.com/search/name/?birth_monthday=06-18&start={}&ref_=rlm".format(page_no)
	    		try:
	    			conn = urllib.request.urlopen(url)
	    		except urllib.error.URLError as e:
	    			print("Connection refused")
	    			Form.close()

	    		html_data = conn.read()
	    		conn.close()
	    		soupData = soup(html_data,'html.parser')
	    		items = soupData.findAll('div',{"class":"lister-item mode-detail"})
	    		for item in items:
	    			name=item.find('h3',{"class":"lister-item-header"}).a.text.strip()
	    			role = item.find('p',{'class':'text-muted text-small'}).text
	    			role=re.findall("\S+ ",role)[0].strip()
	    			movie = item.find('p',{'class':'text-muted text-small'}).a.text.strip()
	    			df['Name'].append(name)
	    			df['Role'].append(role)
	    			df['Movie'].append(movie)
	    		page_no +=50
	    	pd.DataFrame(df).to_csv("IMDb.csv",index_label="index")
	    	msg_box = QtWidgets.QMessageBox()
	    	msg_box.setText("Completed!!!")
	    	msg_box.exec_()


        







    def excelSave(self):
    	self.csvSave()
    	if self.IMDb.isChecked():
    		file = pd.read_csv("IMDb.csv")

    		file.to_excel("IMDb.xlsx",sheet_name='gkz',index=False)
    		os.remove("IMDb.csv")
    		
    	elif self.amazon.isChecked():
    		file=pd.read_csv("books.csv")
    		file.to_excel("Books.xlsx",sheet_name='gkz',index=False)
    		os.remove("books.csv")
    		



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
