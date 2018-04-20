# -*- coding: utf-8 -*-
"""
WebScrapping utility for scrapping tribune.com.pk
https://github.com/furqanbaqai/F1702E1067

Automzation script for browsing and scrapping https://www.tribune.com.pk
This sript will pull all data and push JSON content to ActiveMQ queue
Class below will scrap breaking news only

Distributed under GPLv3 license agreement. Please refere to link:
https://www.gnu.org/licenses/gpl-3.0.en.html for more details.

Authur: Muhammad Furqan Baqai [MFB]
Change History
[MFB:2017-12-3] Initial checkin

"""
import scrapy
import hashlib
import logging
from tribune_com_pk.items import TribuneComPkItem

class BreakingNewsSpider(scrapy.Spider):
    name = 'breaking_news'
    allowed_domains = ['www.tribune.com.pk']
    start_urls = ['https://www.tribune.com.pk/']

    def parse(self, response):         
        triItem = TribuneComPkItem()                                
        headline = response.xpath('//div[contains(@class,"breaking-news")]/div/div/h1/a/text()').extract_first()
        if headline is not None:
            detail_href = response.xpath('//div[contains(@class,"breaking-news")]/div/div/h1/a/@href').extract_first()        
            imagepath = response.xpath('//div[contains(@class,"breaking-news")]/div/div/div[contains(@class,"content")]/div/a/img/@src').extract_first() 
            excerpt = response.xpath('//div[contains(@class,"breaking-news")]/div/div/div[contains(@class,"content")]/div/p/text()').extract_first()               
            triItem['source'] = 'tribune.com.pk'
            triItem['section'] = 'breaking'
            triItem['headline'] = headline.encode("ascii", "ignore").strip().decode("utf-8")
            triItem['head_hash_sha256'] =  hashlib.sha256(headline.encode("ascii", "ignore").strip()).hexdigest()
            triItem['excerpt'] = excerpt.encode("ascii", "ignore").strip().decode("utf-8")
            triItem['imagepath'] = imagepath
            triItem['detail_href'] = detail_href
            yield triItem
        else:
            logging.warning("Breaking news not found. Skipping the breaking news spyder")
