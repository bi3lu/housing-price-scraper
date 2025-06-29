# -*- coding: utf-8 -*-
"""
Description:

Author: Jakub Bielecki
Created: 28-06-2025
"""


from bs4 import BeautifulSoup
import requests
import json


ROOMS_MAP = {
    'ONE': 1,
    'TWO': 2,
    'THREE': 3,
    'FOUR': 4,
    'FIVE': 5,
    'SIX': 6,
    'SEVEN': 7,
    'EIGHT': 8,
    'NINE': 9,
    'TEN': 10
}


class HouseItem:
    def __init__(self, title, price, city, address, area, rooms, house_url):
        self.title = title
        self.price = price
        self.city = city
        self. address = address
        self.area = area
        self.rooms = rooms
        self.house_url = house_url
    

    def print_info(self):
        print(f"Title: {self.title}")
        print(f"Price: {self.price} PLN")
        print(f"City: {self.city}")
        print(f"Address: {self.address}")
        print(f"Area: {self.area} m²")
        print(f"Rooms: {self.rooms}")
        print(f"Link: {self.house_url}")
        print('\n' + '*' * 100 + '\n')


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
    title =  item.get('title', 'no title')

    # checks if total_price is None...
    total_price = item.get('totalPrice')
    price = total_price.get('value') if isinstance(total_price, dict) else 'no price'

    city = item.get('location', {}).get('address', {}).get('city', {}).get('name', 'no city')

    # checks if address_obj is None...
    address_obj = item.get('location', {}).get('address', {}).get('street', 'no street')
    address = f'{address_obj.get('name')} {address_obj.get('number')}' if isinstance(address_obj, dict) else 'no address'

    area = item.get('areaInSquareMeters', 'no area')

    rooms_raw = item.get('roomsNumber')
    rooms = ROOMS_MAP.get(rooms_raw, 'unknown number of rooms')

    house_url = f"https://www.otodom.pl/pl/oferta/{item.get('slug', '')}"

    return HouseItem(title, price, city, address, area, rooms, house_url)


def get_items_list_from_page(house_items):
    items_list: list[HouseItem] = list()

    for h_item in house_items:
        items_list.append(get_item_info(h_item))
    
    return items_list


next_data_json = fetch_otodom_next_data_json("opolskie", "opole", page_num=1)
house_items = extract_listing_items(next_data_json)
items_list = get_items_list_from_page(house_items)

for item in items_list:
    item.print_info()