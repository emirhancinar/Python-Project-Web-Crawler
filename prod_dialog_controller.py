

from ast import While
from sys import hexversion
from time import time
from urllib import parse
from urllib.parse import urlparse
from PyQt5 import QtSql
from PyQt5.QtGui import QTextFormat
from PyQt5.QtWidgets import QDialog

from Ui_prodDialog import Ui_ProdDialog
from models.urun import Urun
from scrapyscript import Job,Processor
from ee_crawler.spiders.trendyol import TrendyolSpider
from ee_crawler.spiders.hepsiburada import HepsiburadaSpider
from scrapy.utils.project import get_project_settings


import matplotlib.pyplot 
import numpy as np

class ProdDialogController():
    def __init__(self, urunId : int):
        self.urunId = urunId

        query = QtSql.QSqlQuery()
        query.prepare("""Select u.UrunAdi, Min(UrunFiyati) MinFiyat,Max(UrunFiyati) MaxFiyat,AVG(UrunFiyati) AvgFiyat
                        from CrawlSonuclari cs 
                        left join Urunler u on u.UrunId = cs.UrunId
                        where cs.UrunId = :urunId
                        group by u.UrunAdi""")
        query.bindValue(":urunId",urunId)
        query.exec()
        query.next()
        rawUrun = query.record()
        
    
        self.queryText = f"""select 
                                cs.UrunAdi as 'Ürün Adı',
                                cs.UrunSaticisi as 'Ürün Saticisi',
                                cs.UrunFiyati as 'Ürün Fiyatı',
                                cs.FetchTime as 'Zaman',
                                cs.Spider as 'Spider',
                                cs.URL as 'URL'
                                from CrawlSonuclari cs 
                                where UrunId = {urunId}
                                order by cs.FetchTime
                                """
        
        
        self.model = QtSql.QSqlTableModel()
        self.model.setQuery(QtSql.QSqlQuery(self.queryText))
        #self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()
        
        self.ProdDialog = QDialog()
        self.prodController = Ui_ProdDialog()
        self.prodController.setupUi(self.ProdDialog)
        self.ProdDialog.show()

        self.prodController.tableView.setModel(self.model)
        self.prodController.tableView.hideColumn(0)
        self.prodController.minFiyat.setText(str(rawUrun.value("MinFiyat")))
        self.prodController.maxFiyat.setText(str(rawUrun.value("MaxFiyat")))
        self.prodController.avgFiyat.setText(str(rawUrun.value("AvgFiyat")))
        self.prodController.tableView.setColumnWidth(5,450)
        self.prodController.urunAdi.setText('<html><head/><body><p><span style=" font-size:18pt;">%s</span></p></body></html>' % (str(rawUrun.value("UrunAdi"))))
        
        self.prodController.crawl.clicked.connect(self.crawl)
        self.prodController.pushButton_3.clicked.connect(self.on_graf)

    def crawl(self):
        query = QtSql.QSqlQuery()
        query.prepare("Select * from UrunURL where UrunId = :urunId")
        query.bindValue(":urunId",self.urunId)
        query.exec()
        urls = list(str())
        while(query.next()):
            rawUrunURL = query.record()
            urls.append(rawUrunURL.value("Url"))
        
        trendyol = list(str())
        hepsiburada = list(str())
        for item in urls:
            parsedItem  = urlparse(item)
            scheme = parsedItem.scheme
            if(scheme == "file"):
                hepsiburada.append(item)
                continue
            if(parsedItem.netloc == "www.trendyol.com"):
                trendyol.append(item)
            elif(parsedItem.netloc == "www.hepsiburada.com"):
                hepsiburada.append(item)
        
        self.prodController.crawlText.setText("Crawling...")
        self.prodController.crawlText.repaint()
        jobs = []
        jobs.append(Job(spider=TrendyolSpider,start_urls=trendyol,UrunId=self.urunId))
        jobs.append(Job(spider=HepsiburadaSpider,start_urls=hepsiburada,UrunId=self.urunId))
        processor = Processor(get_project_settings())
        processor.run(jobs)
        self.prodController.crawlText.setText("Sucsess")
        self.model.setQuery(QtSql.QSqlQuery(self.queryText))
    
    def on_graf(self):
        graf_sonuc_query=QtSql.QSqlQuery("Select * from CrawlSonuclari ")
        #graf_sonuc_query.next()
        rec=graf_sonuc_query.record()
        
        nameCol=rec.indexOf("UrunAdi")
        dateCol=rec.indexOf("FetchTime")
        priceCol=rec.indexOf("UrunFiyati")
        a=0
        date1=[]
        price=[]
        while graf_sonuc_query.next():
            if a==0:
                tit=graf_sonuc_query.value(nameCol)
            
            a+=1
            date1.append((graf_sonuc_query.value(dateCol).toPyDateTime()))
            price.append(graf_sonuc_query.value(priceCol))
        
        xpoint=np.array(date1)
        ypoint=np.array(price)
        matplotlib.pyplot.plot(xpoint,ypoint)
        #for i in date1:
            
        # plt.xlabel("Time")
        # plt.ylabel("Price")
        # plt.title(tit)
        matplotlib.pyplot.show()

     
        

        

