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
CITY = 'opole'


pre_df = pd.read_csv(f'../csv_data/temp/otodom_{CITY}.csv')
pre_df.reset_index()

urls_list = []

for i, row in pre_df.iterrows():
    urls_list.append(row['url'])


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


floor_no_info_list = []
heating_info_list = []
building_type_info_list = []
rent_info_list = []


for url in urls_list:
    json_data = get_json_data_from_url(url)['props']['pageProps']['ad']
    floor_no_info_list.append(get_target_info(json_data, 'Floor_no'))
    heating_info_list.append(get_target_info(json_data, 'Heating'))
    building_type_info_list.append(get_target_info(json_data, 'Building_type'))
    rent_info_list.append(get_target_info(json_data, 'Rent'))


temp_df = pd.DataFrame(
    {
        'floor_no': floor_no_info_list,
        'heating_info': heating_info_list,
        'building_type': building_type_info_list,
        'rent': rent_info_list
    }
)

df = pd.concat([pre_df, temp_df], axis=1)
df.to_csv(f'../csv_data/raw/{CITY}.csv')