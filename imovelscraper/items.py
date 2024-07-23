# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImovelItem(scrapy.Item):
    nome = scrapy.Field()
    preco = scrapy.Field()
    codigo = scrapy.Field()
    area = scrapy.Field()
    quartos = scrapy.Field()
    url = scrapy.Field()
    images = scrapy.Field()
