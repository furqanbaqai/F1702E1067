# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import stomp
import logging

class TribuneComPkPipeline(object):
    stomp_connection = None

    def __init__(self, amqIPAddress, amqPort, amqUID, amqReq, amqPass):
        self.amqIPAddress = amqIPAddress
        self.amqPort = amqPort
        self.amqUID = amqUID
        self.amqReq = amqReq
        self.amqPass = amqPass
        self.__connect()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            amqIPAddress=crawler.settings.get('MONGO_URI'),
            amqPort=crawler.settings.get('AMQ_PORT'),
            amqUID=crawler.settings.get('AMQ_UID'),
            amqReq=crawler.settings.get('AMQ_REQ'),
            amqPass=crawler.settings.get('AMQ_PASS', 'items')
        )

    def __connect(self):
        TribuneComPkPipeline.stomp_connection = stomp.Connection([('192.168.131.144', 61613)])
        TribuneComPkPipeline.stomp_connection.start()
        TribuneComPkPipeline.stomp_connection.connect(self.amqUID, self.amqPass, wait=True)

    def open_spider(self, spider):
        self.__connect()

    def close_spider(self, spider):
        logging.info("Closing AMQ connection and disconnecting as well")
        TribuneComPkPipeline.stomp_connection.disconnect()
        TribuneComPkPipeline.stomp_connection.stop()

    def process_item(self, item, spider):
        if TribuneComPkPipeline.stomp_connection.is_connected == False:
            logging.warning("Re-initiating the connection...")
            self.__connect()
        logging.info("Sending message")
        TribuneComPkPipeline.stomp_connection.send(
            body=str(item), destination=self.amqReq, headers={'persistent': 'true'})
        #c.disconnect()
        #c.stop()
        return item   
