
import sys
from PyQt5.QtWidgets import QPushButton,QLineEdit,QApplication,QWidget,QLabel

class Form1(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200,200,350,200)
        self.setWindowTitle("Web Crawler")
        
        self.initIU()

    
    def initIU(self):
        self.lbl_1=QLabel(self)
        self.lbl_1.setText("Ürün Adı:")
        self.lbl_1.setGeometry(20,20,100,20)
        self.lbl_2=QLabel(self)
        self.lbl_2.setText("Link:")
        self.lbl_2.setGeometry(20,50,100,20)
        #self.lbl_2.setHidden(True)

        self.txt_urun=QLineEdit(self)
        self.txt_urun.setGeometry(80,20,200,20)
        self.txt_link=QLineEdit(self)
        self.txt_link.setGeometry(80,50,200,20)
        #self.txt_link.setHidden(True)

        self.btn_ara=QPushButton("Kaydet",self)
        self.btn_ara.move(20,120)
        self.btn_ara.clicked.connect(self.on_kaydet)

        
        self.show()
        

    def on_kaydet(self):
        self.setHidden(True)    
            

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=Form1()
    sys.exit(app.exec_())

