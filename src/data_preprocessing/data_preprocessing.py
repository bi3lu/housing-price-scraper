# -*- coding: utf-8 -*-
"""
Description:

Author: Jakub Bielecki
Created: 19-07-2025
"""


import pandas as pd
import numpy as np


def load_data(city: str, path: str):
    df = pd.read_csv(f'{path}/{city}.csv')
    df = df.drop(['title', 'url', 'city'], axis=1)
    return df


def preprocess_types(df: pd.DataFrame):
    df['rent'] = df['rent'].replace('none', np.nan)
    df['rent'] = pd.to_numeric(df['rent'], errors='coerce')
    df['rooms'] = pd.to_numeric(df['rooms'], errors='coerce')
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df.dropna(subset=['price'])
    df['price'] = df['price'].astype('int32')
    return df


def encode_address(df: pd.DataFrame):
    address_mean = df.groupby('address')['price'].mean()
    df['address_encoded'] = df['address'].map(address_mean)
    return df.drop(['address'], axis=1)


def encode_categoricals(df: pd.DataFrame):
    categorical_cols = ['district', 'floor_no', 'heating_info', 'building_type']
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    return df


# entry point:
CITY = 'opole'
PATH = '../csv_data/processed'


df = load_data(CITY, PATH)
df = preprocess_types(df)
df = encode_address(df)
df = encode_categoricals(df)