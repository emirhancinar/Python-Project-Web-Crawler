

from PyQt5 import QtSql
from PyQt5.QtWidgets import QDialog

from Ui_prodDialog import Ui_ProdDialog


class ProdDialogController():
    def __init__(self, urunId : int):
        self.urunId = urunId

        query = QtSql.QSqlQuery()
        query.prepare("Select * from Urunler where UrunId = :urunId")
        query.bindValue(":urunId",urunId)
        query.exec()
        query.next()
        urun = query.record()
        print(urun.field(1).value())


        self.ProdDialog = QDialog()
        self.prodController = Ui_ProdDialog()
        self.prodController.setupUi(self.ProdDialog)
        self.ProdDialog.show()

