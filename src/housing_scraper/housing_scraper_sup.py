# -*- coding: utf-8 -*-
"""
housing_scarper_sup.py

This script loads housing advertisement data from a CSV file and enriches it by scraping
additional details from Otodom offer pages. The enriched data includes floor number,
heating type, building type, and rent amount. The final dataset is saved to a new CSV file.

Author: Jakub Bielecki
Created: 17-07-2025
"""


import pandas as pd
import requests
import json
from bs4 import BeautifulSoup


HEADERS = { "User-Agent": "Mozilla/5.0" }


def load_input_data(city: str) -> pd.DataFrame:
    """
    Load housing advertisement data from a CSV file for the specified city.

    Parameters:
        city (str): Name of the city (used in the CSV file name).

    Returns:
        pd.DataFrame: A DataFrame containing the loaded data with reset index.
    """
    df = pd.read_csv(f'../csv_data/temp/otodom_{city}.csv')
    return df.reset_index(drop=True)


def get_json_data_from_url(url: str):
    """
    Fetch and parse the JSON data embedded in the HTML of an advertisement page.

    Parameters:
        url (str): The URL of the Otodom advertisement.

    Returns:
        dict: Parsed JSON object containing the advertisement data.
    """
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find('script', id="__NEXT_DATA__", type="application/json")
    json_data = json.loads(script_tag.string)
    
    return json_data


def get_target_info(json_data: any, prop_name: str):
    """
    Extract a specific property value from the advertisement JSON data.

    Parameters:
        json_data (dict): JSON data of the advertisement.
        prop_name (str): Name of the property to extract (e.g., 'Floor_no').

    Returns:
        str: The value of the requested property, or 'none' if not available.
    """
    try:
        value = json_data['target'][f'{prop_name}']
        if isinstance(value, list) and len(value) == 1:
            return str(value[0])
        return str(value)
    except:
        return 'none'


def extract_ad_details(url: str) -> dict:
    """
    Extract detailed information from a single advertisement page.

    Parameters:
        url (str): The URL of the Otodom advertisement.

    Returns:
        dict: A dictionary containing extracted fields: floor number, heating, building type, and rent.
    """
    json_data = get_json_data_from_url(url)['props']['pageProps']['ad']
    return {
        'floor_no': get_target_info(json_data, 'Floor_no'),
        'heating_info': get_target_info(json_data, 'Heating'),
        'building_type': get_target_info(json_data, 'Building_type'),
        'rent': get_target_info(json_data, 'Rent'),
    }


def enrich_with_details(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich the original DataFrame with additional details extracted from advertisement pages.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing a 'url' column.

    Returns:
        pd.DataFrame: The enriched DataFrame with additional columns for ad details.
    """
    detail_rows = []
    for url in df['url']:
        detail_rows.append(extract_ad_details(url))
    details_df = pd.DataFrame(detail_rows)
    return pd.concat([df.reset_index(drop=True), details_df], axis=1)


# Entry point for processing
CITY = 'opole'

df = load_input_data(CITY)
enriched_df = enrich_with_details(df)
enriched_df.to_csv(f'../csv_data/raw/{CITY}.csv', index=False)