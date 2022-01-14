from PyQt5 import QtCore,QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QWidget
from Ui_listele import Ui_MainWindow
from PyQt5 import QtSql
from Ui_addProd import Ui_dialog
import sys
from add_prod_controller import *
from prod_dialog_controller import ProdDialogController

#SERVER_NAME = 'DESKTOP-37H7N8V'
SERVER_NAME = '.\\SQLEXPRESS'
DATABASE_NAME = 'Crawler'


class Application(object):

    def showAddProd(self):
            self.addProd = AddProdController(self.selectUrunler)
        
    def showUrunDialog(self):
        model = self.controller.tbwg_listele.selectionModel()
        selectedIndexes = model.selectedIndexes()
        if(len(model.selectedIndexes()) > 0):
            self.prodDialog = ProdDialogController(selectedIndexes[0].siblingAtColumn(0).data())
        

    def __init__(self, *args):
        app = QApplication(sys.argv)
    
        db_list = QtSql.QSqlDatabase.addDatabase("QODBC")
        connString = f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME}'
        
        
    
        db_list.setDatabaseName(connString)
        if not db_list.open():
            print("connection not open")
        
        self.model = QtSql.QSqlQueryModel()
        #self.model.setTable("Urunler")

        self.listeleQuery = """Select 
                                u.UrunId,
                                u.UrunAdi 'Ürün Adı', 
                                Min(UrunFiyati) 'Min Fiyat',
                                Max(UrunFiyati) 'Max Fiyat',
                                AVG(UrunFiyati) 'Ortalama Fiyat'
                                from Urunler u 
                                left join CrawlSonuclari cs on u.UrunId = cs.UrunId
                                group by u.UrunAdi,u.UrunId"""

        self.model.setQuery(QtSql.QSqlQuery(self.listeleQuery))
        #self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        #self.model.select()
        

        window = QMainWindow()
        self.controller = Ui_MainWindow()
        self.controller.setupUi(window)
        self.controller.tbwg_listele.setModel(self.model)
        self.controller.tbwg_listele.hideColumn(0)
        self.controller.tbwg_listele.contextMenuEvent = self.contextMenuEvent
        self.controller.btn_listele.clicked.connect(self.listeleBtnClick)
        self.controller.action_r_n_Ekle.triggered.connect(self.showAddProd)
        self.controller.tbwg_listele.doubleClicked.connect(self.showUrunDialog)

        window.show()       
        sys.exit(app.exec_())

    def listeleBtnClick(self):
        self.selectUrunler()

    def selectUrunler(self):
        self.model.setQuery(QtSql.QSqlQuery(self.listeleQuery))

    def contextMenuEvent(self,event):
        contextMenu = QMenu(self.controller.tbwg_listele)
        newAct = contextMenu.addAction("Sil",self.removeSelectedItem)
        action = contextMenu.exec_(self.controller.tbwg_listele.mapToGlobal(event.pos()))

    def removeSelectedItem(self):
        model = self.controller.tbwg_listele.selectionModel()
        selectedIndexes = model.selectedIndexes()
        if(len(model.selectedIndexes()) > 0):
            urunId = selectedIndexes[0].siblingAtColumn(0).data()
            QtSql.QSqlQuery(f"delete from Urunler where UrunId = {urunId}")
            self.selectUrunler()
            

if __name__ == '__main__':
    app = Application()


