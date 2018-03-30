# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import stomp
import logging
import json

class DawnComPipeline(object):
    stomp_connection = None
    logger = logging.getLogger(__name__)

    def __init__(self, amqIPAddress, amqPort, amqUID, amqReq,amqPass):
        self.amqIPAddress   = amqIPAddress
        self.amqPort = amqPort
        self.amqUID = amqUID
        self.amqReq = amqReq
        self.amqPass = amqPass
        self.__connect()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            amqIPAddress=crawler.settings.get('AMQ_IP_ADD'),
            amqPort=crawler.settings.get('AMQ_PORT'),
            amqUID=crawler.settings.get('AMQ_UID'),
            amqReq=crawler.settings.get('AMQ_REQ'),
            amqPass=crawler.settings.get('AMQ_PASS', 'items')
        )

    def __connect(self):                
        DawnComPipeline.logger.info("Establishing connection with host ["+self.amqIPAddress + "] and port ["+str(self.amqPort)+"]")
        DawnComPipeline.stomp_connection = stomp.Connection([(self.amqIPAddress, self.amqPort)])
        DawnComPipeline.stomp_connection.start()
        DawnComPipeline.stomp_connection.connect(self.amqUID, self.amqPass, wait=True)

    def open_spider(self, spider):
        self.__connect()

    def close_spider(self, spider):
        DawnComPipeline.logger.info("Closing AMQ connection and disconnecting as well")
        DawnComPipeline.stomp_connection.disconnect()
        DawnComPipeline.stomp_connection.stop()

    def process_item(self, item, spider):        
        if DawnComPipeline.stomp_connection.is_connected == False:
            DawnComPipeline.logger.warning("Re-initiating the connection...")
            self.__connect()
        DawnComPipeline.logger.info("Sending message")
        # (ID#4)BUG! Item is disctionary and it is not proper JSON. Parsing it to JSON
        DawnComPipeline.stomp_connection.send(body=json.dumps(
            dict(item)), destination=self.amqReq, headers={'persistent': 'true'})
        return item
