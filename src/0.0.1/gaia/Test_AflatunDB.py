
import unittest
from AflatunDB import AflatunDB
import os
#import pymysql.cursors

class Test_AflatunDB(unittest.TestCase):
    #connection = None
    aflatunDB = None

    def setUp(self):        
        mysqlHost = os.environ['MYSQL_HOST'] = '192.168.139.180'
        mysqlUser = os.environ['MYSQL_USER'] = 'root'
        mysqlPass = os.environ['MYSQL_PASSWORD'] = 'admin'
        mysqlDB = os.environ['MYSQL_DB'] = 'aflatun'
        mysqlCharSet = os.environ['MYSQL_CHARSET'] = 'utf8mb4'
        self.aflatunDB = AflatunDB()

        
    def test_getTopNews(self):
        result = self.aflatunDB.getTopNews()                        
        self.assertTrue(len(result) > 0)

    def test_getMetaContent(self):
        result = self.aflatunDB.getEntities(
            '206c6ecf65679d728f13e3f1f5f26553b38db9a169b0e6810af759c17f29a720')
        print(result)        
        self.assertTrue(len(result) > 0)

if __name__ == '__main__':
    unittest.main()
