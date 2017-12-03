# -*- coding: utf-8 -*-
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
            triItem['headline'] = headline
            triItem['head_hash_sha256'] =  hashlib.sha256(str.encode(headline)).hexdigest()
            triItem['excerpt'] = excerpt
            triItem['imagepath'] = imagepath
            triItem['detail_href'] = detail_href
            yield triItem
        else:
            logging.warning("Breaking news not found. Skipping the breaking news spyder")
