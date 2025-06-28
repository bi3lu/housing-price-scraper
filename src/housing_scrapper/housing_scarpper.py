# -*- coding: utf-8 -*-
"""
Description:

Author: Jakub Bielecki
Created: 28-06-2025
"""


from bs4 import BeautifulSoup
import requests
import json


class HouseItem:
    def __init__(self, title, price, city, street, area, rooms, house_url):
        self.title = title
        self.price = price
        self.city = city
        self. street = street
        self.area = area
        self.rooms = rooms
        self.house_url = house_url
    

    def print_info(self):
        print(f"Title: {self.title}")
        print(f"Price: {self.price} PLN")
        print(f"City: {self.city}")
        print(f"Street: {self.street}")
        print(f"Area: {self.area}")
        print(f"Rooms: {self.rooms}")
        print(f"Link: {self.house_url}")
        print('*' * 100 + '\n')


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
    city = item.get('location', {}).get('address', {}).get('city', {}).get('name', 'no city')
    street = item.get('location', {}).get('address', {}).get('street', 'no street')
    area = item.get('areaInSquareMeters', 'no area')
    rooms = item.get('roomsNumber', 'no rooms')
    house_url = f"https://www.otodom.pl/pl/oferta/{item.get('slug', '')}"

    return HouseItem(title, price, city, street, area, rooms, house_url)


next_data_json = fetch_otodom_next_data_json("opolskie", "opole", page_num=1)
house_items = extract_listing_items(next_data_json)
item = get_item_info(house_items[0])
item.print_info()