
"""
Alice::GoogleNLP: Utility for wrapping GoogleNLP features in pythong code
https://github.com/furqanbaqai/F1702E1067

Distributed under GPLv3 license agreement. Please refere to link:
https://www.gnu.org/licenses/gpl-3.0.en.html for more details.

Authur: Muhammad Furqan Baqai [MFB]
Change History
[MFB:2018-03-28] Initial checkin

"""
import json
import os
import logging
import uuid
import pymysql.cursors
from urllib.request import urlopen
from urllib.request import Request

logging.basicConfig(format='[%(levelname)s] %(asctime)s:%(message)s', level=logging.INFO)


class GoogleNLP(object):           
    logger = logging.getLogger(__name__)
    token = None
    _SQL_SEL_CONTENT_ENTITIES = 'SELECT entityID FROM ContentEntities WHERE name=%s'
    _SQL_INSERT_INTO_CONTENT = 'INSERT INTO ContentEntities(entityID,name,type,reference) VALUES(%s,%s,%s,%s)'
    _SQL_INSERT_INTO_CONTTOENT = 'INSERT INTO MetaContentTOEntities(entityID,ContentHash,salience) VALUE(%s,%s,%s)'
    _URL_ANALYZE_ENTITES = 'https://language.googleapis.com/v1/documents:analyzeEntities?key='
    connection = None

    def  __init__ (self,hashKey,contentBody,connection):
    # def __int__(self):
        self.logger.debug('Initializing class for content hash:' + hashKey)
        self.token = os.environ['GOOGLE_API_TOKEN']
        self.hashKey = hashKey
        self.contentBody = contentBody
        self.connection = connection

    def analyzeEntities(self):
        GoogleNLP.logger.info('Calling GoogleNLP AnalyzeEntities API')
        
        jsRequest = json.dumps({'document': {
                               'type': 'PLAIN_TEXT', 'content': self.contentBody}})
        GoogleNLP.logger.debug("Constructed JSON Request:" + jsRequest)
        req = Request(url=GoogleNLP._URL_ANALYZE_ENTITES + self.token, data=jsRequest.encode('utf-8'),
                      headers={'Content-type': 'application/json; charset=utf-8'}, method='POST')                        
        response = urlopen(req)                
        if response.getcode() == 200 :            
            response = json.loads(response.read().decode('utf-8'))
            GoogleNLP.logger.debug('Response received: ' + str(response))
            # process response received
            self.__processResponse(response)
        else:
            GoogleNLP.logger.info('Error response received:' + str(response.getcode()))
            return
    
    def __processResponse(self,entities):
        with self.connection.cursor() as cursor:            
            for item in entities['entities']:
                name = item['name']
                enttype = item['type']
                salience = item['salience']
                wik_url = None                
                # save to database            
                if type != 'OTHER':
                    self.__saveItToDB(cursor, name, enttype, wik_url,salience)
        self.connection.commit()


    def __saveItToDB(self, cursor, name, enttype, wik_url,salience):
        self.logger.info('Saving response to the database')
        # Step#1: Check if the entity already exist in the database
        entityID = self.__nameExist(name,cursor)        
        if  entityID == None:            
            GoogleNLP.logger.info('Name does not exist. Saving content in the database')                        
            entityID = str(uuid.uuid4())
            cursor.execute(self._SQL_INSERT_INTO_CONTENT,(entityID, name.title(),enttype,wik_url))            
        else:
            GoogleNLP.logger.info('Name exist. skipping the storing into entity store..')        
        # Insert content in the MetaContentTOEntities
        GoogleNLP.logger.debug('Saving entity with entityID:'+entityID + ' hashKey='+self.hashKey+' Salience='+str(type(salience)))        
        cursor.execute(self._SQL_INSERT_INTO_CONTTOENT,(entityID,self.hashKey,salience))

    def __nameExist(self,name,cursor):
        cursor.execute(self._SQL_SEL_CONTENT_ENTITIES,(name))
        result = cursor.fetchone()                                
        GoogleNLP.logger.debug("Result from redundancy check="+str(result))
        if result != None:
            return result['entityID']
        else:
            return result
    



if __name__ == "__main__":
    # Loading environment variables
    amqHost = os.environ['AMQ_IP_ADD']
    amqPort = os.environ['AMQ_PORT']
    amqUid = os.environ['AMQ_UID']
    amqPass = os.environ['AMQ_PASS']
    mysqlHost = os.environ['MYSQL_HOST']
    mysqlUser = os.environ['MYSQL_USER']
    mysqlPass = os.environ['MYSQL_PASSWORD']
    mysqlDB = os.environ['MYSQL_DB']
    mysqlCharSet = os.environ['MYSQL_CHARSET']
    # Connect to the database server
    connection = pymysql.connect(
         host=mysqlHost,
         user=mysqlUser,
         password=mysqlPass,
         db=mysqlDB,
         charset=mysqlCharSet,
         cursorclass=pymysql.cursors.DictCursor
     )

    googleNLP = GoogleNLP('46a68580619a0e2c62c467bd2a4d0d8da40c08b03a70b48e880bc3759bded3c8',
                          'Statement comes in wake of reports of suspected clashes making the rounds on Afghan media',
                          None)
    response = googleNLP.analyzeEntities()                          
    logging.debug("Response received: "+str(response))        
