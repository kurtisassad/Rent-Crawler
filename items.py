# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Compose
import re

class ListingLoader(ItemLoader):
    default_output_processor = TakeFirst()

class Listing(scrapy.Item):
    url = scrapy.Field()
    price = scrapy.Field(input_processor = MapCompose(lambda string: re.search('\d+,*\d+.*\d*',string),
                                                      lambda string: string.group(0) if string is not None else None,
                                                      lambda string: string.replace(',','') if string is not None else None,
                                                      lambda string: float(string) if string is not None else None)
                        )
    location = scrapy.Field()
    beds = scrapy.Field(input_processor=MapCompose(lambda string: re.search('\d+',string),
                                                   lambda string: string.group(0) if string is not None else None,
                                                   lambda string: float(string) if string is not None else None)
                        )
    type = scrapy.Field()
    url = scrapy.Field()
    leaseTerm = scrapy.Field(input_processor=MapCompose(lambda string: re.search('\d+',string),
                                                        lambda string: string.group(0) if string is not None else None,
                                                        lambda string: float(string) if string is not None else None)
                            )

    availableSince = scrapy.Field()
    imageUrl = scrapy.Field()
