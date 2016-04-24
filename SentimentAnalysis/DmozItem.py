import scrapy

class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

class FinanceCrawlerItem(scrapy.Item):
    date = scrapy.Field()
    keywords = scrapy.Field()
    body = scrapy.Field()