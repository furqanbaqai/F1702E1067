# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import stomp
import logging

class DawnComPipeline(object):
    stomp_connection = None

    def __init__(self, amqIPAddress, amqPort, amqUID, amqPass):
        self.amqIPAddress   = amqIPAddress
        self.amqPort = amqPort
        self.amqUID = amqUID
        self.amqPass = amqPass
        self.__connect()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            amqIPAddress=crawler.settings.get('MONGO_URI'),
            amqPort=crawler.settings.get('AMQ_PORT'),
            amqUID=crawler.settings.get('AMQ_UID'),
            amqPass=crawler.settings.get('AMQ_PASS', 'items')
        )

    def __connect(self):        
        DawnComPipeline.stomp_connection = stomp.Connection([('192.168.131.144', 61613)])
        DawnComPipeline.stomp_connection.start()
        DawnComPipeline.stomp_connection.connect('admin', 'admin', wait=True)

    def process_item(self, item, spider):        
        if DawnComPipeline.stomp_connection.is_connected == False:
            logging.warning("Re-initiating the connection...")
            self.__connect()
        logging.info("Sending message")
        DawnComPipeline.stomp_connection.send(body=str(item), destination="DAWN_COM.REQ", headers={'persistent': 'true'})
        #c.disconnect()
        #c.stop()
        return item

    def __del__(self):
        logging.info("Closing AMQ connection and disconnecting as well")
        DawnComPipeline.stomp_connection.disconnect()
        DawnComPipeline.stomp_connection.stop()
