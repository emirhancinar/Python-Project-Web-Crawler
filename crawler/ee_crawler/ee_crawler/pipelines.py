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
        self.mydb = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=crawler;")
    
    def process_item(self, item: dict, spider: Spider):
        adapter = ItemAdapter(item)
        sql = "INSERT INTO urun_sonuclari (urun_adi, urun_fiyati, satici) Values (%s,%s,%s)" % (adapter["urun-adi"],adapter["fiyati"],adapter["satici"])
        mycursor = self.mydb.cursor()
        mycursor.execute(sql)
        self.mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        return item
