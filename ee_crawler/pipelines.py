# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pyodbc
from scrapy.spiders import Spider

class EeCrawlerPipeline:
    def open_spider(self, spider):
        self.mydb = pyodbc.connect("DRIVER={SQL Server};SERVER=.\\SQLEXPRESS;DATABASE=Crawler;")
        self.UrunId = spider.UrunId
    
    def process_item(self, item: dict, spider: Spider):
        adapter = ItemAdapter(item)
        sql = "INSERT INTO CrawlSonuclari (UrunAdi, UrunSaticisi, UrunFiyati,UrunId,FetchTime,URL,Spider) Values (\'%s\',\'%s\',%f,%d,getdate(),\'%s\',\'%s\')" % (adapter["urun-adi"],adapter["satici"],float(adapter["fiyat"].replace(".","").replace(",",".")),self.UrunId,adapter["url"],spider.name)
        mycursor = self.mydb.cursor()
        mycursor.execute(sql)
        self.mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        return item
