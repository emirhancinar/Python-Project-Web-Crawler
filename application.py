from PyQt5 import QtCore,QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QWidget
from Ui_listele import Ui_MainWindow
from PyQt5 import QtSql
from Ui_addProd import Ui_dialog
import sys
from add_prod_controller import AddProdController

SERVER_NAME = '.\\'
DATABASE_NAME = 'Crawler'


class Application(object):

    def showAddProd(self):
        self.addProd = AddProdController()
        
    def __init__(self, *args):
        app = QApplication(sys.argv)
    
        db = QtSql.QSqlDatabase.addDatabase("QODBC")
        connString = f'DRIVER={{SQL Server}};'\
                    f'SERVER={SERVER_NAME};'\
                    f'DATABASE={DATABASE_NAME}'
        
    
        db.setDatabaseName(connString)
        if not db.open():
            print("connection not open")
        
        
        self.model = QtSql.QSqlTableModel()
        #self.model.setQuery(QtSql.QSqlQuery("Select * from Urunler u Where u.urunId=1",db))
        self.model.setTable("Urunler")
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()


        window = QMainWindow()
        controller = Ui_MainWindow()
        controller.setupUi(window)
        controller.tbwg_listele.setModel(self.model)
        controller.tbwg_listele.hideColumn(0)
        controller.btn_listele.clicked.connect(lambda x : self.model.select())
        controller.action_r_n_Ekle.triggered.connect(self.showAddProd)
        
        window.show()
        
        sys.exit(app.exec_())

        

if __name__ == '__main__':
    app = Application()


