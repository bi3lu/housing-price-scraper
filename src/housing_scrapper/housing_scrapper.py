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


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


class HouseItem:
    def __init__(self, title, price, area, rooms, house_url, city, address, district=None):
        self.title = title
        self.price = price
        self.area = area
        self.rooms = rooms
        self.house_url = house_url
        self.city = city
        self. address = address
        self.district = district
    

    def print_info(self):
        print(f"Title: {self.title}")
        print(f"Price: {self.price} PLN")
        print(f"Area: {self.area} m²")
        print(f"Rooms: {self.rooms}")
        print(f"Link: {self.house_url}")
        print(f"City: {self.city}")
        print(f"Address: {self.address}")
        print(f"District: {self.district}")
        print('\n' + '*' * 100 + '\n')


def get_max_page_num(voivodeship: str, city: str):
    test_page = 999 # big number to force redirection to max page
    url = f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/{voivodeship}/{city}?page={test_page}"
    response = requests.get(url, headers=HEADERS, allow_redirects=True)

    redirected_url = response.url

    if 'page=' in redirected_url:
        try:
            return int(redirected_url.split('page=')[1])
        except ValueError:
            pass

    return 1


def fetch_otodom_next_data_json(voivodeship: str, city: str, page_num: int = 1):
    url = f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/{voivodeship}/{city}?page={page_num}"
    response = requests.get(url, headers=HEADERS)
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

    area = item.get('areaInSquareMeters', 'no area')

    rooms_raw = item.get('roomsNumber')
    rooms = ROOMS_MAP.get(rooms_raw, 'unknown number of rooms')

    house_url = f"https://www.otodom.pl/pl/oferta/{item.get('slug', '')}"

    city = item.get('location', {}).get('address', {}).get('city', {}).get('name', 'no city')

    # checks if address_obj is None...
    address_obj = item.get('location', {}).get('address', {}).get('street', 'no street')
    address = f'{address_obj.get('name')} {address_obj.get('number')}' if isinstance(address_obj, dict) else 'no address'

    district = None
    locations = item.get('location', {}).get('reverseGeocoding', {}).get('locations', [])
    
    if locations:
        full_name = locations[-1].get('fullName', '')
        district = full_name.split(',')[0].strip() if full_name else None

    return HouseItem(title, price, area, rooms, house_url, city, address, district)


def get_items_list_from_page(house_items):
    items_list: list[HouseItem] = list()

    for h_item in house_items:
        items_list.append(get_item_info(h_item))
    
    return items_list


def scrap_multiple_pages(voivodeship: str, city: str, max_page_num: int):
    all_items = list()

    for page_num in range(1, max_page_num + 1):
        try:
            next_data_json = fetch_otodom_next_data_json(voivodeship, city, page_num)
            house_items = extract_listing_items(next_data_json)
            items_list = get_items_list_from_page(house_items)
            all_items.extend(items_list)
        except Exception as e:
            print(f'Error! | page num: {page_num} | desc: {e} ')
    
    return all_items


MAX_PAGE_NUM = get_max_page_num("opolskie", "opole")

all_items = scrap_multiple_pages('opolskie', 'opole', MAX_PAGE_NUM)
print(len(all_items))