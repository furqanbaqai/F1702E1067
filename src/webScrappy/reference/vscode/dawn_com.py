"""
WebScrapping utility for scrapping dawn.com
https://github.com/furqanbaqai/F1702E1067

Automzation script for browsing and scrapping https://www.dawn.com
This sript will pull all data and push JSON content to ActiveMQ queue

Distributed under GPLv3 license agreement. Please refere to link:
https://www.gnu.org/licenses/gpl-3.0.en.html for more details.

Authur: Muhammad Furqan Baqai [MFB]
Change History
[MFB:2017-11-30] Initial checkin

"""

import requests
from bs4 import BeautifulSoup

url = "https://www.dawn.com"
page = requests.get(url)
soup = BeautifulSoup(page.content,"html5lib")

# Iterate through all article tag
for article in soup.find_all('article',attrs={'data-layout':'story'}):
    print(type(article))

print("exiting")


