# -*- coding: utf-8 -*-
"""
Description:

Author: Jakub Bielecki
Created: 17-07-2025
"""


import pandas as pd
import requests
import json
from bs4 import BeautifulSoup


HEADERS = { "User-Agent": "Mozilla/5.0" }


def load_input_data(city: str) -> pd.DataFrame:
    df = pd.read_csv(f'../csv_data/temp/otodom_{city}.csv')
    return df.reset_index(drop=True)


def get_json_data_from_url(url: str):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find('script', id="__NEXT_DATA__", type="application/json")
    json_data = json.loads(script_tag.string)
    
    return json_data


def get_target_info(json_data: any, prop_name: str):
    try:
        value = json_data['target'][f'{prop_name}']
        if isinstance(value, list) and len(value) == 1:
            return str(value[0])
        return str(value)
    except:
        return 'none'


def extract_ad_details(url: str) -> dict:
    json_data = get_json_data_from_url(url)['props']['pageProps']['ad']
    return {
        'floor_no': get_target_info(json_data, 'Floor_no'),
        'heating_info': get_target_info(json_data, 'Heating'),
        'building_type': get_target_info(json_data, 'Building_type'),
        'rent': get_target_info(json_data, 'Rent'),
    }


def enrich_with_details(df: pd.DataFrame) -> pd.DataFrame:
    detail_rows = []
    for url in df['url']:
        detail_rows.append(extract_ad_details(url))
    details_df = pd.DataFrame(detail_rows)
    return pd.concat([df.reset_index(drop=True), details_df], axis=1)


# entry point:
CITY = 'opole'


df = load_input_data(CITY)
enriched_df = enrich_with_details(df)
enriched_df.to_csv(f'../csv_data/raw/{CITY}.csv', index=False)