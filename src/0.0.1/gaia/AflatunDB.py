"""
AflatunDB:Class wrapping mysql databse engine
https://github.com/furqanbaqai/F1702E1067

Distributed under GPLv3 license agreement. Please refere to link:
https://www.gnu.org/licenses/gpl-3.0.en.html for more details.

Pre-requisite:
pip install flask
pip install flask-httpauth
pip install pymysql

Authur: Muhammad Furqan Baqai [MFB]
Change History
[MFB:2018-04-06] Initial checkin

set MYSQL_HOST=192.168.139.180
set MYSQL_USER=root
set MYSQL_PASSWORD=admin
set MYSQL_DB=aflatun
set MYSQL_CHARSET=utf8mb4
"""

import logging
import os
import pymysql.cursors
import json

logging.basicConfig(
    format='[%(asctime)s:%(name)s:%(process)d:%(lineno)d %(levelname)s] %(message)s', level=logging.INFO)

class AflatunDB():
    __dbConnection = None
    __mysqlHost = None
    __mysqlUser = None
    __mysqlPass = None
    __mysqlDB = None
    __mysqlCharSet = None    
    __logger = logging.getLogger("AflatunDB")

    __SQL_GETTOPNEWS = 'SELECT ContentHash,ContentKey as heading,AuthurID,source,excerpt,contentIndex,CAST(fetchedOn AS CHAR) as fetchedOn, imageFileName,imageURL,detailURL from MetaContentMaster order by fetchedOn desc LIMIT 10 OFFSET 0;'
    __SQL_GETENTITIES = 'SELECT entityID,name,type,reference,description from ContentEntities where entityID in (select entityID from MetaContentTOEntities where ContentHash = %s);'

    def __init__(self):
        # step#1: load all environment variables
        self.__logger.info('Initializing DBHelper')
        if self.__mysqlHost == None:
            self.__logger.info('Loading environment variables')            
            # *** Loading environment variables for connecting with the database server ***
            self.__mysqlHost = os.environ['MYSQL_HOST']
            self.__mysqlUser = os.environ['MYSQL_USER']
            self.__mysqlPass = os.environ['MYSQL_PASSWORD']
            self.__mysqlDB = os.environ['MYSQL_DB']
            self.__mysqlCharSet = os.environ['MYSQL_CHARSET']
            # *** END ***            

    def __connect(self):
        # if self.__dbConnection == None or self.__dbConnection.open == False:            
        logging.info('Connecting to the database server [%s]' \
            % (self.__mysqlHost+'::'+self.__mysqlDB))
        self.__dbConnection = pymysql.connect(
            host=self.__mysqlHost,
            user = self.__mysqlUser,
            password = self.__mysqlPass,
            db = self.__mysqlDB,
            charset = self.__mysqlCharSet,
            cursorclass = pymysql.cursors.DictCursor
        )
        logging.info('Connected...')

    #
    # Procedure for returning top 10 news
    #
    def getTopNews(self):
        self.__connect()
        with self.__dbConnection.cursor() as cursor:
            cursor.execute(self.__SQL_GETTOPNEWS,())
            result = cursor.fetchall()
            if len(result) < 0:
                raise ValueError('No result returned')
            logging.debug('** Result for getTopNews():'+str(result))                        
            return json.dumps({'result' :result})

    #
    # Procedure for returning content entities for specific news
    #
    def getEntities(self,hashCode):
        self.__connect()        
        with self.__dbConnection.cursor() as cursor:
            cursor.execute(self.__SQL_GETENTITIES,(hashCode))
            logging.debug("Fetching entities for hashcode: "+hashCode)
            result = cursor.fetchall()
            if len(result) < 0:
                raise ValueError('No value returned')
            logging.debug('** Result for getMertaContent:'+str(result))
            return json.dumps({'result' : result})



