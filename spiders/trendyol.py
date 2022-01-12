import scrapy


class TrendyolSpider(scrapy.Spider):
    name = 'trendyol'
    allowed_domains = ['trendyol.com']

    def parse(self, response):
        yield {
            'satici': response.css('a.merchant-text::text').get(),
            'fiyati': response.css("div.product-price-container span.prc-dsc::text").get(),
            'urun-adi': response.css("div.product-container h1.pr-new-br a::text").get() + response.css("div.product-container h1.pr-new-br span::text").get(),
        }
