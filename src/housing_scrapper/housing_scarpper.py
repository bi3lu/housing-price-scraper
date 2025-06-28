# -*- coding: utf-8 -*-
"""
Description:

Author: Jakub Bielecki
Created: 28-06-2025
"""


import requests
from bs4 import BeautifulSoup as bs


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "pl-PL,pl;q=0.9",
}


def get_houses_bs_content(voivodeship, city):
    root_url = f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/{voivodeship}/{city}/"
    page = requests.get(root_url, headers=HEADERS)
    soup = bs(page.content)
    
    return soup


soup_obj = get_houses_bs_content('opolskie', 'opole')
print(soup_obj.prettify())