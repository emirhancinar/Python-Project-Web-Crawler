import scrapy
from datetime import datetime

class TrendyolSpider(scrapy.Spider):
    name = 'trendyol'
    allowed_domains = ['trendyol.com']
    start_urls = [
        'https://www.trendyol.com/msi/mpg-x570-gaming-plus-ddr4-4400-oc-mhz-atx-am4-p-6989910',
    ]

    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        fiyat = response.css("div.product-price-container span.prc-dsc::text").get()
        if(fiyat == None):
            fiyat = response.css("div.product-price-container span.prc-slg::text").get()
        yield {
            'satici': response.css('a.merchant-text::text').get(),
            'fiyat':  fiyat.replace("TL","").strip(" \n\r\t"),
            'urun-adi': response.css("div.product-container h1.pr-new-br a::text").get() + response.css("div.product-container h1.pr-new-br span::text").get(),
            'url': response.url
        }
