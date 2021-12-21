import sys
from PyQt5.QtWidgets import QAbstractItemDelegate, QApplication,QTableWidget,QPushButton, QTableWidgetItem,QWidget, QWidgetItem
import pyodbc
import webcrawler

class Form2 (QWidget):
    def __init__(self):
        super().__init__()
        self.con=pyodbc.connect('Driver={SQL SERVER};''Server=DESKTOP-37H7N8V;''Database=sqlbasla;''Trusted_Connection=yes;')
        self.setWindowTitle("Listele")
        self.setGeometry(100,100,500,500)
        self.initIU()

    def initIU(self):
        
        self.tbwg_listele=QTableWidget(self)
        self.tbwg_listele.setGeometry(40,40,400,210)

        self.btn_list=QPushButton("Listele",self)
        self.btn_list.move(100,300)
        self.btn_list.clicked.connect(self.on_list)
        #self.closeEvent = lambda x : self.close()
        self.btn_git=QPushButton("Git",self)
        self.btn_git.move(300,300)
        self.btn_git.clicked.connect(self.new_form)

        self.show() 

    def new_form(self):
        self.web_crawler=webcrawler.Form1()
        
        # self.setHidden(True)

    def on_list(self):
        self.tablo_list()

    def tablo_list(self):
        
        cursor=self.con.cursor()
        cursor.execute('Select * from Urunler')
        data=cursor.fetchall()
       # urunler=[{"urunId":1,"urunAdi": "Çanta","fiyati":200},{"urunId":5,"urunAdi":"Ayakkabı","fiyati":300}]  
        row=0
        self.tbwg_listele.setColumnCount(3)
        self.tbwg_listele.setHorizontalHeaderLabels(["id","Ad","Fiyat"])
        self.tbwg_listele.setRowCount(len(data))

        for urun in data:
            self.tbwg_listele.setItem(row,0,QTableWidgetItem(str(urun[0])))
            self.tbwg_listele.setItem(row,1,QTableWidgetItem(urun[1]))
            self.tbwg_listele.setItem(row,2,QTableWidgetItem(str(urun[2])))
            row+=1

        self.con.close()

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=Form2()
    sys.exit(app.exec_())