import scrapy
import re

class HepsiburadaSpider(scrapy.Spider):
    name = 'hepsiburada'
    allowed_domains = ['hepsiburada.com']
    start_urls = ['https://www.hepsiburada.com/xiaomi-redmi-9t-64-gb-xiaomi-turkiye-garantili-p-HBCV000008Z6HO?magaza=Hepsiburada']
        

    def parse(self, response):

        spans = response.css('.product-price-wrapper span')
        result = ""
        for item in spans:
            if not "data-bind" in dict(item.attrib) : continue
            if(str(item.attrib['data-bind']).find("markupText:'currentPriceBeforePoint'") != -1):
                result += item.css("::text").get()
            elif(str(item.attrib['data-bind']).find("markupText:'currentPriceAfterPoint'") != -1):
                result += "," + item.css("::text").get()
        
        yield {
            "fiyat" : result,
            "urun-adi" : response.css("#product-name::text").get().strip(" \n\r\t"),
            "satici" : response.css(".seller span > a ::text").get().strip(" \n\r\t"),
            }
        
