"""
EVA: Job Scheduling utility which controls OS jobs
https://github.com/furqanbaqai/F1702E1067



Distributed under GPLv3 license agreement. Please refere to link:
https://www.gnu.org/licenses/gpl-3.0.en.html for more details.

Authur: Muhammad Furqan Baqai [MFB]
Change History
[MFB:2018-01-13] Initial checkin

"""

import schedule
import time
import os
import logging

EVA_HOME = os.environ.get('EVA_HOME',None)
logging.basicConfig(format='[%(levelname)s] %(asctime)s:%(message)s', level=logging.DEBUG)


def job_scrapy_dawn():
    logging.info('Starting crawler')
    output = os.popen('cd ' + EVA_HOME + '/dawn_com && scrapy crawl topnews -s  AMQ_IP_ADD=$AMQ_IP_ADD -s AMQ_PORT=$AMQ_PORT -s AMQ_UID=$AMQ_UID -s AMQ_PASS=$AMQ_PASS -s LOG_LEVEL=$LOG_LEVEL -s IMAGES_STORE=$IMAGES_STORE').read()
    logging.debug('Output Recieved: '+output)
    logging.info('Crawler command finished')


def job_scrapy_tribune():
    logging.info('Starting crawler: tribune_com_pk')
    # output = os.popen('cd /mnt/hgfs/eva/tribune_com_pk && scrapy crawl topnews').read()
    output = os.popen('cd ' + EVA_HOME + '/tribune_com_pk && scrapy crawl topnews -s  AMQ_IP_ADD=$AMQ_IP_ADD -s AMQ_PORT=$AMQ_PORT -s AMQ_UID=$AMQ_UID -s AMQ_PASS=$AMQ_PASS -s LOG_LEVEL=$LOG_LEVEL -s IMAGES_STORE=$IMAGES_STORE').read()
    logging.debug('Output Recieved: ' + output)
    logging.info('Crawler command finished')



schedule.every(5).minutes.do(job_scrapy_dawn)
schedule.every(5).minutes.do(job_scrapy_tribune)

if __name__ == '__main__':
    print('*******************')
    print('  _____ ____ _  ')
    print(' / -_) V / _` | ')
    print(' \___|\_/\__,_| ')
    print('*******************')
    logging.info('Starting eva scheduler service')
    logging.info('Cehcking required configurations..')    
    logging.info('EVA_HOME: '+EVA_HOME)
    if EVA_HOME == None:
        raise ValueError('Environment variable EVA_HOME not set. Exiting application')
    logging.info('Configurations exist. Initiating scheduler...')
    while True:
        schedule.run_pending()
        time.sleep(1)
