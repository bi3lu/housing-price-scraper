# -*- coding: utf-8 -*-
"""
Description:

Author: Jakub Bielecki
Created: 28-06-2025
"""

import requests
from bs4 import BeautifulSoup as bs


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "pl-PL,pl;q=0.9",
}

page_url = "https://www.otodom.pl/" # can be constant
page = requests.get(page_url, headers=headers)
soup = bs(page.content)

print(soup.prettify())