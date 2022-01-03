import sys
from typing import Text
from PyQt5.QtWidgets import QDialog,QMessageBox
from Ui_addProd import Ui_dialog
from PyQt5 import QtSql

#from application import DATABASE_NAME, SERVER_NAME


  
class AddProdController(object):
    def __init__(self,tableModel : QtSql.QSqlTableModel):
        self.table_urun = tableModel
        self.ProdDialog = QDialog()
        self.prodController = Ui_dialog()
        self.prodController.setupUi(self.ProdDialog)
        self.ProdDialog.show()

        
        self.prodController.btn_ekle.clicked.connect(self.on_ekle)
        self.prodController.btn_cwtest.clicked.connect(self.on_test)
        self.prodController.btn_kaydet.clicked.connect(self.on_kaydet)

    def on_ekle(self):
        self.prodController.lbx_url.addItem(self.prodController.txt_ad.toPlainText() +"  "+ self.prodController.txt_url.toPlainText())
    
    def on_test(self):
        pass

    def on_kaydet(self):

        insert = QtSql.QSqlQuery()
        insert.prepare("Insert into Urunler(urunAdi) values (:urunAdi) SELECT SCOPE_IDENTITY()")
        insert.bindValue(":urunAdi",self.prodController.txt_ad.toPlainText()) 
        insert.exec()
        insert.next()
        urunId = insert.value(0)
        urlCount = self.prodController.lbx_url.count()
        q = QtSql.QSqlQuery()
        q.prepare("insert into UrunURL(UrunId,Url) values " + ("(?, ?)," * urlCount).rstrip(","))

        for item in range(urlCount):
            q.addBindValue(urunId)
            q.addBindValue(self.prodController.lbx_url.item(item).text())
        q.exec()

        self.table_urun.select()
       
       
        # newRecord= self.table_urun.record()
        # newRecord.remove(0)
        # 
        # newRecord.setValue("urunAdi",self.prodController.txt_ad.toPlainText())
        # liste=len(self.prodController.lbx_url)
        # self.table_urun.insertRecord(-1,newRecord)
        # err = self.table_urun.lastError()
        # print(err.text())

        
        



