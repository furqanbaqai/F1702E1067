# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TribuneComPkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    headline             = scrapy.Field()
    head_hash_sha256     = scrapy.Field()
    index                = scrapy.Field()
    source               = scrapy.Field()
    image_urls           = scrapy.Field()
    images               = scrapy.Field()
    detail_href          = scrapy.Field()
    section              = scrapy.Field()
    excerpt              = scrapy.Field()
    authur               = scrapy.Field()
    detailNews           = scrapy.Field()
    fetchedTime          = scrapy.Field(serializer=str)
    body                 = scrapy.Field()

    
