"""
WebScrapping utility for scrapping dawn.com
https://github.com/furqanbaqai/F1702E1067

Automzation script for browsing and scrapping https://www.dawn.com
This sript will pull all data and push JSON content to ActiveMQ queue

Distributed under GPLv3 license agreement. Please refere to link:
https://www.gnu.org/licenses/gpl-3.0.en.html for more details.

Authur: Muhammad Furqan Baqai [MFB]
Change History
[MFB:2017-11-30] Initial checkin
[MFB:2017-12-26] Re-aligning by implementing items

"""

import scrapy
import hashlib
import logging
from dawn_com.items import DawnComItem
from scrapy.http import Request

class QuotesSpider(scrapy.Spider):
    name = "topnews"
    allowed_domains = ['www.dawn.com']
    start_urls = ['https://www.dawn.com']
    

    # Procedure called for parsing the content
    def parse(self, response):        
        articles=response.xpath('//article[@data-layout="story"]')       
        for index,article in enumerate(articles):
            dawnItem = DawnComItem()
            headline = article.xpath('h2/a[@class="story__link"]/text()').extract_first()
            excerpt = article.xpath('div[contains(@class,"story__excerpt")]/text()').extract_first()
            det_href = article.xpath('figure/div/a/@href').extract_first()
            imgpath = article.xpath('figure/div/a/img/@src').extract_first() 
            # Serializing the extracted components
            dawnItem['source']				= 'dawn.com'
            dawnItem['section']			    = 'main'
            dawnItem['index']				= str(index)
            dawnItem['headline']			= headline.encode("ascii", "ignore").strip().decode("utf-8")
            dawnItem['head_hash_sha256'] 	= hashlib.sha256(headline.encode("ascii", "ignore").strip()).hexdigest()
            dawnItem['excerpt'] 			= excerpt.encode("ascii", "ignore").strip().decode("utf-8")
            dawnItem['imagepath'] 			= imgpath            
            dawnItem['detail_href'] 		= det_href
            # Saving items for subsequent detail poage call
            if det_href:
                logging.info('*** following link:'+det_href)
                request = Request(url=det_href, callback=self.parseDetail_page,meta={'dawnItem':dawnItem})   
                yield request         
            else:
                yield dawnItem        
            if index == 7:
                break
           
    
    # Procedure which will be called for parsing 
    def parseDetail_page(self, response):
        dawnItem = response.meta['dawnItem']
        # dawnItem['authur'] = 'Bhai sahab'
        yield dawnItem
