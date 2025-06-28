# -*- coding: utf-8 -*-
"""
Description:

Author: Jakub Bielecki
Created: 28-06-2025
"""


from bs4 import BeautifulSoup
import requests
import json


def fetch_otodom_next_data_json(voivodeship: str, city: str, page_num: int = 1):
    url = f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/{voivodeship}/{city}?page={page_num}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find('script', id="__NEXT_DATA__", type="application/json")

    if not script_tag:
        raise Exception("Not found in <script id='__NEXT_DATA__'> tag.")

    json_data = json.loads(script_tag.string)

    return json_data


def extract_listing_items(next_data_json):
    try:
        return next_data_json['props']['pageProps']['data']['searchAds']['items']
    except KeyError:
        raise Exception("Not found any house items.")


def get_item_info(item):
    title = item.get('title', 'no title')
    price = item.get('totalPrice', {}).get('value', 'no price')
    city = item.get('location', {}).get('address', {}).get('city', {}).get('name', 'no city name')
    area = item.get('areaInSquareMeters', 'no square meters area')
    rooms = item.get('roomsNumber', 'no rooms')
    link = f'https://www.otodom.pl/pl/oferta/{item.get('slug', '')}'

    print(f"{title}")
    print(f"Cena: {price} PLN")
    print(f"Miasto: {city}")
    print(f"Powierzchnia: {area} m²")
    print(f"Pokoje: {rooms}")
    print(f"Link: {link}")


next_data_json = fetch_otodom_next_data_json("opolskie", "opole", page_num=1)
house_items = extract_listing_items(next_data_json)
get_item_info(house_items[0])
