import unittest
from GoogleNLP import GoogleNLP
import os
import pymysql.cursors

class TestGoogleNLP(unittest.TestCase):
    connection = None

    def setUp(self):
        # setup environment
        print('Initiating setup..')
        amqHost = os.environ['AMQ_IP_ADD'] = ''
        amqPort = os.environ['AMQ_PORT'] = '32770'
        amqUid = os.environ['AMQ_UID'] = ''
        amqPass = os.environ['AMQ_PASS'] = ''
        mysqlHost = os.environ['MYSQL_HOST'] = ''
        mysqlUser = os.environ['MYSQL_USER'] = ''
        mysqlPass = os.environ['MYSQL_PASSWORD'] = ''
        mysqlDB = os.environ['MYSQL_DB'] = ''
        mysqlCharSet = os.environ['MYSQL_CHARSET'] = 'utf8mb4'
        os.environ['GOOGLE_API_TOKEN'] = ''
        # setup db connection
        self.connection = pymysql.connect(
            host=mysqlHost,
            user=mysqlUser,
            password=mysqlPass,
            db=mysqlDB,
            charset=mysqlCharSet,
            cursorclass=pymysql.cursors.DictCursor
        )

    def test_analyzeEntities(self):        
        googleNLP = GoogleNLP('1514c84371228b78b6ad1dadd814d0fa791fb1e71b86d5a8633b00de9f600e64',
                              'KARACHI:Pakistan stock markets growth momentum slowed down on Friday as selling pressure built in that outweighed bullish sentiments.Most heavyweight sectors, including cement and fertiliser, fell prey to profit-booking and closed in the red.At close, the benchmark KSE 100-share Index recorded an increase of 70.68 points or 0.16% to settle at 45,560.30.Arif Habib Ltd Sales, in its report, said the KSE-100 Index remained range bound throughout the day, which was also the last day of rollover.Selling pressure in blue chips kept bulls in control, however, at the sessions end news of price increases by Aisha Steel Mills and International Steels generated some activity in both stocks, the report said.Market watch: KSE-100 rises over 300 points on enhanced investor interestCement, exploration and production, fertiliser and auto sectors closed in the red and failed to generate any significant activity.There was optimism about the beginning of next quarter and month on Monday. Sectors contributing to the increase included commercial bank (+87 points) and auto (+19 points).Stocks that contributed significantly to the volumes included K-Electric, TRG Pakistan, Engro Polymer and Chemicals, JS Bank and Pak Elektron that accounted for 39% of total volumes.Stocks that contributed positively included Habib Bank (+60 points), United Bank (+28 points), Kohinoor Textile Mills (+16 points), Mari Petroleum (+13 points) and Packages Limited (+13 points).Stocks that contributed negatively included Pakistan Tobacco (-27 points), TRG Pakistan (-19 points), MCB Bank (-18 points), Cherat Cement (-11 points) and Dawood Hercules (-11 points).Market watch: Stocks advance on back of cement, auto sectorsOverall, trading volumes decreased to 230 million shares compared with Thursdays tally of 296 million.Shares of 374 companies were traded. At the end of the day, 152 stocks closed higher, 206 declined while 16 remained unchanged. The value of shares traded during the day was Rs9.46 billion.K-Electric was the volume leader with 23.8 million shares, losing Rs0.05 to close at Rs7.01. It was followed by TRG Pakistan with 22.4 million shares, losing Rs1.84 to close at Rs36.36 and Engro Polymer with 21.8 million shares, gaining Rs1.32 to close at Rs35.65.Foreign institutional investors were net sellers of Rs152.5 million worth of shares during the trading session, according to data compiled by the National Clearing Company of Pakistan.',
                  self.connection)
        googleNLP.analyzeEntities()
        

if __name__ == '__main__':
    unittest.main()



