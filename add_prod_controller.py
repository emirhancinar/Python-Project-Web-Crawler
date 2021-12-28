


from typing import Text
from PyQt5.QtWidgets import QDialog

from Ui_addProd import Ui_dialog


class AddProdController(object):
    def __init__(self):
        self.ProdDialog = QDialog()
        self.prodController = Ui_dialog()
        self.prodController.setupUi(self.ProdDialog)
        self.ProdDialog.show()
        
        self.prodController.btn_ekle.clicked.connect(self.on_ekle)
    def on_ekle(self):
        self.prodController.lbx_url.addItem(self.prodController.txt_ad.toPlainText() +"  "+ self.prodController.txt_url.toPlainText())
         