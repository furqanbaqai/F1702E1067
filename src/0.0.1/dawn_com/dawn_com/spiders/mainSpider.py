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

"""

import scrapy
import hashlib

class QuotesSpider(scrapy.Spider):
    name = "mainpage"

    def start_requests(self):
        url = 'https://www.dawn.com'        
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        articles=response.xpath('//article[@data-layout="story"]')
        for index,article in enumerate(articles):
            headline = article.xpath('h2/a[@class="story__link"]/text()').extract_first()
            excerpt = article.xpath('div[contains(@class,"story__excerpt")]/text()').extract_first()
            det_href = article.xpath('figure/div/a/@href').extract_first()
            imgpath = article.xpath('figure/div/a/img/@src').extract_first()            
            yield{
                'source': 'dawn.com',
                'section': 'main',
                'index' : str(index),
                'headline' : headline,
                'head_hash_sha256' : hashlib.sha256(str.encode(headline)).hexdigest(),
                'excerpt' : excerpt,
                'imagepath' : imgpath,
                'detail_href' : det_href,

            }            
            if index == 7:
                break