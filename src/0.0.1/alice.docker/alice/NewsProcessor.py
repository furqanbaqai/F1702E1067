"""
Alice: Utlity for fetching content from AMQ and saving it in the datbase
https://github.com/furqanbaqai/F1702E1067



Distributed under GPLv3 license agreement. Please refere to link:
https://www.gnu.org/licenses/gpl-3.0.en.html for more details.

Authur: Muhammad Furqan Baqai [MFB]
Change History
[MFB:2018-01-13] Initial checkin

"""
import logging
import stomp
import time
import json
import pymysql.cursors
import uuid
import os
from google.GoogleNLP import GoogleNLP

logging.basicConfig(format='[%(levelname)s] %(asctime)s:%(message)s', level=logging.INFO)

amqHost = os.environ['AMQ_IP_ADD']
amqPort = os.environ['AMQ_PORT']
amqUid = os.environ['AMQ_UID']
amqPass = os.environ['AMQ_PASS']
mysqlHost = os.environ['MYSQL_HOST']
mysqlUser = os.environ['MYSQL_USER']
mysqlPass = os.environ['MYSQL_PASSWORD']
mysqlDB = os.environ['MYSQL_DB']
mysqlCharSet = os.environ['MYSQL_CHARSET']

class Processor(object):    

    def __init__(self, queue,uid):        
        self.queue = queue
        self.id = uid        
        self.stompConnection = None
        self.__connect()

    def __connect(self):
        logging.info('Connecting with AMQ')        
        self.stompConnection = stomp.Connection([(amqHost, amqPort)])
        self.stompConnection.set_listener('NEWS_LISTENER',NewsListener())
        self.stompConnection.set_listener('STATS_LISTENER', MyStatsListener())

        self.stompConnection.start()
        self.stompConnection.connect(mysqlUser, mysqlPass, wait=True)
        self.stompConnection.subscribe(destination=self.queue, id=self.id, ack='auto')


    def processNews(self):
        # Step#1: Connect to AMQ
        if self.stompConnection.is_connected == False:
            self.__connect()        
        logging.info('Fetching message from the queue: '+ self.queue)
        # Step#2: GET news from queue specified in self.queueName

    def disconnect(self):
        self.stompConnection.disconnect()

    

class NewsListener(stomp.ConnectionListener):    
    _SQL_INS_AUTHURMASTER   = 'INSERT INTO AuthurMaster(AuthurID,name,reference,description) VALUES(%s,%s,%s,%s)'    
    _SQL_INS_METACONTMASTER = 'INSERT INTO MetaContentMaster (ContentHash, ContentKey,AuthurID,source,contentIndex,excerpt, body, fetchedOn, imageFileName, imageURL, detailURL) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    
    _SQL_SELECT_AUTHMASTER_GETAUTHID = 'SELECT AuthurID from AuthurMaster WHERE name = %s'
    _SQL_SEL_METACONTMASTER_GETHASH = 'SELECT ContentHash FROM MetaContentMaster WHERE ContentHash=%s'


    connection = None # MYSQL Connection

    def on_error(self, headers, message):
        print('Error received: ' + message)

    def on_message(self, headers, message):
        logging.info("Message received..")
        logging.debug("***** Headers *****" +"\n"+ str(headers))
        logging.debug("***** Message *****" + "\n" + str(message))
        data = json.loads(message)        
        # Step#2: Extract all content from the json object        
        source = data['source']
        section = data['section']
        index = data['index']
        headline = data['headline']
        hash256 = data['head_hash_sha256']
        excerpt = data['excerpt']
        image_urls = data['image_urls']
        images = data['images']
        detail_href = data['detail_href']
        authur = data['authur']
        detailNews = data['detailNews']
        fetchedOn = data['fetchedTime']
        self.saveToDB(source, section, index, headline, hash256, excerpt,
                      image_urls, images, detail_href, authur, detailNews, fetchedOn)

    def saveToDB(self,source, section, index,headline,hash256,excerpt,image_urls,images,detail_href,authur,detailNews,fetchedOn):
        # Step#1: Connect to the database server
        if self.connection == None :
            logging.info("Connecting to the database server")
            self.connection = pymysql.connect(
                host=mysqlHost,
                user = mysqlUser,
                password=mysqlPass,
                db=mysqlDB,
                charset=mysqlCharSet,
                cursorclass=pymysql.cursors.DictCursor
            )
                
        with self.connection.cursor() as cursor:
            authurID = str(uuid.uuid4())
            # Check if the authur name already present in the AuthurMaster
            cursor.execute(self._SQL_SELECT_AUTHMASTER_GETAUTHID,(authur))
            result = cursor.fetchone()
            if result != None and result['AuthurID'] != None:
                logging.info('Authur already present in the database')
                authurID = result['AuthurID']
            else:
                # If not, save authur in the AuthurMaster
                logging.info('Authur not found in the database. Saving Authur.')
                cursor.execute(self._SQL_INS_AUTHURMASTER,(authurID, authur, source, ''))
            # Check if the content is already saved in the database or not
            cursor.execute(self._SQL_SEL_METACONTMASTER_GETHASH,(hash256))
            result = cursor.fetchone()
            if result == None or result['ContentHash'] == None:
                logging.info('New content, saving it in the database')
                # Save news information in the MetaContentMaster table
                cursor.execute(self._SQL_INS_METACONTMASTER, (hash256, headline,
                                                            authurID, source, index, excerpt, detailNews, fetchedOn,images,image_urls,detail_href))
                # TODO! Call another class for fetching analytical data of the detailNews                                                            
                googleNLP = GoogleNLP(hash256,detailNews,self.connection)
                googleNLP.analyzeEntities()
            else:
                logging.info('Skipping content. Same content found in the database server')                                                        
            self.connection.commit()
    
        
                

class MyStatsListener(stomp.StatsListener):
    def on_disconnected(self):
        super(MyStatsListener, self).on_disconnected()
        print('MyStatsListener:\n{}\n'.format(self))




if __name__ == "__main__":
    # Step#1: Instantiate the News Processor
    # TODO! Fetch these queue list from environment variable
    queues = ['DAWN_COM.REQ', 'TRIBUNE_COM_PK.REQ']    
    
    # Step#2: Iterate through the array and call Processor
    while True:
        count = 1
        for queue in queues:        
            processor = Processor(queue, count)
            processor.processNews()  
            count = count + 1
            time.sleep(3)
            processor.disconnect()
    
    processor.disconnect()
         
   
