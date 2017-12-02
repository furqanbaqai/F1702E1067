# -*- coding: utf-8 -*-
"""
WebScrapping utility for scrapping tribune.com.pk
https://github.com/furqanbaqai/F1702E1067

Automzation script for browsing and scrapping https://www.tribune.com.pk
This sript will pull all data and push JSON content to ActiveMQ queue

Distributed under GPLv3 license agreement. Please refere to link:
https://www.gnu.org/licenses/gpl-3.0.en.html for more details.

Authur: Muhammad Furqan Baqai [MFB]
Change History
[MFB:2017-11-2] Initial checkin

"""
import scrapy
import hashlib
from tribune_com_pk.items import TribuneComPkItem


class MainpageSpider(scrapy.Spider):
    name = 'mainpage'
    allowed_domains = ['www.tribune.com.pk']
    start_urls = ['https://www.tribune.com.pk/']
    
    def parse(self, response):
        articles = response.xpath('//div[contains(@class, "main")]/div[@class="span-8"]/div')
        for index, article in enumerate(articles):
            headline = None
            hrefpath = None
            if index == 0:
                # extracting headline from top news
                headline = article.xpath('h1/a/text()').extract_first()
            else:
                headline = article.xpath('h2/a/text()').extract_first()
            excerpt = article.xpath('div/p[@class="excerpt"]/text()').extract_first()
            detail_href = article.xpath('div/a[@class="image"]/@href').extract_first()
            imagepath = article.xpath('div/a[@class="image"]/img[1]/@src').extract_first()
            # Creating item of the scrapped object
            triItem = TribuneComPkItem()                        
            triItem['source'] = 'tribune.com.pk'
            triItem['section'] = 'main'
            triItem['index'] = str(index)
            triItem['headline'] = headline
            triItem['head_hash_sha256'] =  hashlib.sha256(str.encode(headline)).hexdigest()
            triItem['excerpt'] = excerpt
            triItem['imagepath'] = imagepath
            triItem['detail_href'] = detail_href
            # Yielding item
            yield triItem