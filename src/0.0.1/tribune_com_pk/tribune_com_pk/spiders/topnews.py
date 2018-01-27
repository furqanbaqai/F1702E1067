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
[MFB:2017-12-2] Initial checkin
[MFB:2017-12-30] Adding logic to download detail content and images
"""
import scrapy
import hashlib
import logging
import urllib.request

from time import gmtime,strftime
from scrapy.http import Request
from tribune_com_pk.items import TribuneComPkItem
from bs4 import BeautifulSoup



class MainpageSpider(scrapy.Spider):
    name = 'topnews'
    allowed_domains = ['www.tribune.com.pk','tribune.com.pk']
    start_urls = ['https://www.tribune.com.pk/']
    
    def parse(self, response):
        # Step#1:                                                 
        # Step#1: Scrap all latest news
        settings = self.settings
        articles = response.xpath('//div[contains(@class, "main")]/div[@class="span-8"]/div')
        for index, article in enumerate(articles):
            headline = None            
            triItem = TribuneComPkItem()
            if index == 0:
                # extracting headline from top news
                headline = article.xpath('h1/a/text()').extract_first()
            else:
                headline = article.xpath('h2/a/text()').extract_first()
            excerpt = article.xpath('div/p[@class="excerpt"]/text()').extract_first()
            detail_href = article.xpath('div/a[@class="image"]/@href').extract_first()
            imagepath = article.xpath('div/a[@class="image"]/img[1]/@src').extract_first()
            # Creating item of the scrapped object  
            head_hash                   = hashlib.sha256(headline.encode("ascii", "ignore").strip()).hexdigest()          
            triItem['source']           = 'tribune.com.pk'
            triItem['section']          = 'main'
            triItem['index']            = str(index)
            triItem['headline']         = headline.encode("ascii", "ignore").strip().decode("utf-8")
            triItem['head_hash_sha256'] =  head_hash
            triItem['excerpt']          = excerpt.encode("ascii", "ignore").strip().decode("utf-8")
            triItem['image_urls']       = imagepath
            triItem['images']           = head_hash+ '.' + imagepath.split('.')[3:][1]    
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(imagepath, settings['IMAGES_STORE'] + '/tribune_com_pk' + head_hash + '.' + imagepath.split('.')[3:][1])
            # urlretrieve (imagepath, settings['IMAGES_STORE']+head_hash+ imagepath.split('.')[3:][1]) 
            triItem['detail_href']      = detail_href
            triItem['fetchedTime']      = strftime("%Y-%m-%d %H:%M:%S", gmtime())                        
            if detail_href:
                logging.info('*** following link:'+detail_href)
                request = Request(url=detail_href, callback=self.parseDetail_page,meta={'triItem':triItem})   
                yield request
            else:
                yield triItem
            

    # Procedure which will be called for parsing 
    def parseDetail_page(self, response):        
        triItem = response.meta['triItem']
        story = response.xpath('//div[contains(@class,"story")]')
        triItem['authur'] = story.xpath('div[@class="meta"]/div[@class="author"]/a[1]/text()').extract_first()        
        body = story.xpath('div[contains(@class,"story-content")]/p')
        content = ''
        for index,bodyT in enumerate(body):
            if bodyT:
                content = content + bodyT.get().strip()
        content = content.encode("ascii","ignore").strip().decode("utf-8")        
        triItem["detailNews"] = BeautifulSoup(content,'html.parser').get_text()
        yield triItem                    
