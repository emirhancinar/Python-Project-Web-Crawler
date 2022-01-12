from urllib import parse
from PyQt5 import QtCore
from PyQt5.QtCore import  QModelIndex
from PyQt5.QtWidgets import QDialog, QListWidgetItem, QMenu
from pydispatch import dispatcher
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from Ui_addProd import Ui_dialog
from PyQt5 import QtGui, QtSql
from scrapy.utils.project import get_project_settings
from crawler.ee_crawler.ee_crawler.spiders.hepsiburada import HepsiburadaSpider
from crawler.ee_crawler.ee_crawler.spiders.trendyol import TrendyolSpider 
from scrapyscript import Job,Processor

from urllib.parse import urlparse



#from application import DATABASE_NAME, SERVER_NAME


  
class AddProdController(object):
    tempResults = []
    def __init__(self,tableModel : QtSql.QSqlTableModel):
        self.table_urun = tableModel
        self.ProdDialog = QDialog()
        self.prodController = Ui_dialog()
        self.prodController.setupUi(self.ProdDialog)
        self.ProdDialog.show()
        
        
        
        

        
        self.prodController.btn_ekle.clicked.connect(self.on_ekle)
        self.prodController.btn_cwtest.clicked.connect(self.on_test)
        self.prodController.btn_kaydet.clicked.connect(self.on_kaydet)
        self.prodController.lbx_url.contextMenuEvent = self.contextMenuEvent;
        self.prodController.btn_kaydet.setDisabled(True)
        #self.prodController.lbx_url.
        #self.prodController.txt_url.paste.connect()
        
    def contextMenuEvent(self,event):
        contextMenu = QMenu(self.prodController.lbx_url)
        newAct = contextMenu.addAction("Sil",self.removeSelectedItem)
        openAct =contextMenu.addAction("Düzenle",self.editSelectedItem)
        action = contextMenu.exec_(self.prodController.lbx_url.mapToGlobal(event.pos()))
    
    def removeSelectedItem(self):
        selected = self.prodController.lbx_url.selectedIndexes()
        if(len(selected) > 0):
            self.prodController.lbx_url.takeItem(selected[0].row())
    def editSelectedItem(self):
        selected = self.prodController.lbx_url.selectedIndexes()
        if(len(selected) > 0):
            self.prodController.lbx_url.editItem(self.prodController.lbx_url.item(selected[0].row()))


    def testSuccsessful(self):
        self.prodController.btn_kaydet.setDisabled(False)    
    def testFailed(self):
        self.prodController.btn_kaydet.setDisabled(True)    
        

    def on_ekle(self):
        item = QListWidgetItem()
        item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable) 
        item.setText(self.prodController.txt_url.text())
        self.prodController.lbx_url.addItem(item)
        self.prodController.txt_url.clear()
    
    def spider_results(self,urls : list[str]):
        results = []
        trendyol = []
        hepsiburada = []
        for item in urls:
            parsedUrl = urlparse(item)
            domain = parsedUrl.netloc
            if(domain == "www.trendyol.com"):
                trendyol.append(item)
            elif(domain == "www.hepsiburada.com"):
                hepsiburada.append(item)
            elif (parsedUrl.scheme == "file") : hepsiburada.append(item)
            else: assert()    

        jobs = []

        if(len(trendyol) > 0):
           jobs.append(Job(TrendyolSpider, start_urls=trendyol))
        
        if(len(hepsiburada) > 0):
            jobs.append(Job(HepsiburadaSpider, start_urls=hepsiburada))
        
        
        # process = CrawlerProcess()        
        # process.crawl(TrendyolSpider,start_urls=["https://www.trendyol.com/msi/mpg-x570-gaming-plus-ddr4-4400-oc-mhz-atx-am4-p-6989910"])
        # process.start()

        processor = Processor({"USER_AGENT": ""})
        results = processor.run(jobs)
        return results

    def on_test(self):
        if(self.prodController.lbx_url.count() == 0): 
            self.prodController.crawl_result.setText("Lütfen İlk Olarak URL giriniz")
            return
        self.prodController.crawl_result.setText("Loading...")
        falseUrlCount = 0
        urlsToCrawl = []
        
        for item in range(self.prodController.lbx_url.count()):
            url = self.prodController.lbx_url.item(item).text()
            parsedUrl = urlparse(url)
            domain = parsedUrl.netloc
            if(parsedUrl.scheme == "file"): pass
            elif(domain not in ["www.trendyol.com","www.hepsiburada.com"]):
                falseUrlCount += 1
                continue
            urlsToCrawl.append(url)
        result = []
        if(len(urlsToCrawl) > 0):
            result = self.spider_results(urlsToCrawl)
            print(result)
        resultText = str(len(result)) + " tane ürün başarıyla çekildi."
        if(falseUrlCount > 0): resultText += f"\n{falseUrlCount} Tane Hatalı URL"
        if(len(urlsToCrawl) - len(result) != 0): resultText += "\n" + str(len(urlsToCrawl) - len(result)) + " tane ürünü okurken hata oluştu"
        self.prodController.crawl_result.setText(resultText)
        if(falseUrlCount == 0 and len(urlsToCrawl) - len(result) == 0):
            self.testSuccsessful()
        else : self.testFailed()

        
        
        

    def on_kaydet(self):

        insert = QtSql.QSqlQuery()
        insert.prepare("Insert into Urunler(urunAdi) values (:urunAdi) SELECT SCOPE_IDENTITY()")
        insert.bindValue(":urunAdi",self.prodController.txt_ad.text()) 
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
        self.ProdDialog.close()
       
       
        # newRecord= self.table_urun.record()
        # newRecord.remove(0)
        # 
        # newRecord.setValue("urunAdi",self.prodController.txt_ad.toPlainText())
        # liste=len(self.prodController.lbx_url)
        # self.table_urun.insertRecord(-1,newRecord)
        # err = self.table_urun.lastError()
        # print(err.text())

        
        



