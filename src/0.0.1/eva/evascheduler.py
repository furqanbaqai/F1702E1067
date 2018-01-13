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

def job_scrapy_dawn():
    logging.info('Starting crawler')
    output = os.popen('cd /mnt/hgfs/eva/dawn_com && scrapy crawl topnews').read()
    logging.debug('Output Recieved: '+output)
    logging.info('Crawler command finished')


def job_scrapy_tribune():
    logging.info('Starting crawler: tribune_com_pk')
    output = os.popen('cd /mnt/hgfs/eva/tribune_com_pk && scrapy crawl topnews').read()
    logging.debug('Output Recieved: ' + output)
    logging.info('Crawler command finished')


logging.basicConfig(format='[%(levelname)s] %(asctime)s:%(message)s', level=logging.DEBUG)

schedule.every(5).minutes.do(job_scrapy_dawn)
schedule.every(5).minutes.do(job_scrapy_tribune)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
