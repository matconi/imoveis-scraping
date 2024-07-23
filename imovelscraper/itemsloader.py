from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


class ImovelLoader(ItemLoader):
    default_output_processor = TakeFirst()
