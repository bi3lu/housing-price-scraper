# -*- coding: utf-8 -*-
"""
housing_scarper.py

This script scrapes apartment listing data from Otodom (a Polish real estate website)
for a given voivodeship and city. It collects details such as title, price, area, number 
of rooms, address, and district from multiple pages of results and saves the data into a CSV file.

Author: Jakub Bielecki
Created: 28-06-2025
"""


from bs4 import BeautifulSoup
import requests
import json
import csv
import os


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
    """
    Represents a single house/apartment listing.
    """
    def __init__(self, title, price, area, rooms, house_url, city, address, district=None):
        self.title = title
        self.price = price
        self.area = area
        self.rooms = rooms
        self.house_url = house_url
        self.city = city
        self.address = address
        self.district = district
    

    def print_info(self):
        """
        Print formatted information about the listing.
        """
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
    """
    Determines the number of pages available for listings in the given location.

    Parameters:
        voivodeship (str): The voivodeship (province) name.
        city (str): The city name.

    Returns:
        int: The maximum page number.
    """
    test_page = 999 # Large number to trigger redirect to the last page
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
    """
    Fetches the JSON data from the Otodom listing page.

    Parameters:
        voivodeship (str): The voivodeship name.
        city (str): The city name.
        page_num (int): The page number to fetch.

    Returns:
        dict: Parsed JSON data embedded in the page.
    """
    url = f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/{voivodeship}/{city}?page={page_num}"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find('script', id="__NEXT_DATA__", type="application/json")

    if not script_tag:
        raise Exception("Not found in <script id='__NEXT_DATA__'> tag.")

    json_data = json.loads(script_tag.string)

    return json_data


def extract_listing_items(next_data_json):
    """
    Extracts listing items from the embedded JSON data.

    Parameters:
        next_data_json (dict): Parsed JSON object from the Otodom page.

    Returns:
        list: List of raw listing items.
    """
    try:
        return next_data_json['props']['pageProps']['data']['searchAds']['items']
    except KeyError:
        raise Exception("Not found any house items.")


def get_item_info(item):
    """
    Extracts relevant details from a single listing item.

    Parameters:
        item (dict): A single listing item from the Otodom JSON data.

    Returns:
        HouseItem: An object representing the listing.
    """
    title =  item.get('title', 'no title')

    # checks if total_price is None...
    total_price = item.get('totalPrice')
    price = total_price.get('value') if isinstance(total_price, dict) else 'no price'

    area = item.get('areaInSquareMeters', 'no area')

    rooms_raw = item.get('roomsNumber')
    rooms = ROOMS_MAP.get(rooms_raw, 'unknown number of rooms')

    house_url = f"https://www.otodom.pl/pl/oferta/{item.get('slug', '')}"

    city = item.get('location', {}).get('address', {}).get('city', {}).get('name', 'no city')

    address_obj = item.get('location', {}).get('address', {}).get('street', 'no street')
    address = f'{address_obj.get('name')} {address_obj.get('number')}' if isinstance(address_obj, dict) else 'no address'

    district = None
    locations = item.get('location', {}).get('reverseGeocoding', {}).get('locations', [])
    
    if locations:
        full_name = locations[-1].get('fullName', '')
        district = full_name.split(',')[0].strip() if full_name else None

    return HouseItem(title, price, area, rooms, house_url, city, address, district)


def scrap_multiple_pages(voivodeship: str, city: str, max_page_num: int):
    """
    Scrapes all pages of listings and collects unique results.

    Parameters:
        voivodeship (str): The voivodeship name.
        city (str): The city name.
        max_page_num (int): The number of pages to scrape.

    Returns:
        dict: A dictionary of unique HouseItem objects, keyed by listing ID.
    """
    all_items_unique = {}

    for page_num in range(1, max_page_num + 1):
        try:
            next_data_json = fetch_otodom_next_data_json(voivodeship, city, page_num)
            house_items = extract_listing_items(next_data_json)

            for item in house_items:
                item_id = item.get('id')

                if item_id not in all_items_unique:
                    item_obj = get_item_info(item)
                    all_items_unique[item_id] = item_obj

        except Exception as e:
            print(f'Error! | page num: {page_num} | desc: {e} ')
    
    return all_items_unique


def save_items_to_csv(items_dict: dict, filename: str):
    """
    Saves the scraped house items into a CSV file.

    Parameters:
        items_dict (dict): Dictionary of HouseItem objects.
        filename (str): Output path for the CSV file.
    """
    fieldnames = ['title', 'price', 'area', 'rooms', 'url', 'city', 'address', 'district']

    with open(filename, mode='w', newline='', encoding='utf-8') as csv_f:
        writer = csv.DictWriter(csv_f, fieldnames=fieldnames)
        writer.writeheader()

        for i in items_dict.values():
            writer.writerow({
                'title': i.title,
                'price': i.price,
                'area': i.area,
                'rooms': i.rooms,
                'url': i.house_url,
                'city': i.city,
                'address': i.address,
                'district': i.district
            })


# Entry point for processing
VOIDESHIP = 'opolskie'
CITY = 'opole'
MAX_PAGE_NUM = get_max_page_num(VOIDESHIP, CITY)

output_path = os.path.join(os.path.dirname(__file__), '..', 'csv_data/temp', f'otodom_{CITY}.csv')
output_path = os.path.abspath(output_path)
items_dict = scrap_multiple_pages(VOIDESHIP, CITY, MAX_PAGE_NUM)

save_items_to_csv(items_dict, output_path)