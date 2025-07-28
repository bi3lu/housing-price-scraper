# -*- coding: utf-8 -*-
"""
data_preprocessing.py

This script performs preprocessing of real estate data collected from Otodom.
It loads raw data, converts data types, handles missing values, encodes categorical 
features, and saves the processed dataset for modeling or further analysis.

Author: Jakub Bielecki
Created: 19-07-2025
"""


import pandas as pd
import numpy as np


def load_data(city: str, path: str) -> pd.DataFrame:
    """
    Loads a CSV file containing raw housing data for a given city.

    Parameters:
        city (str): The name of the city (used to locate the file).
        path (str): Path to the folder containing the raw data file.

    Returns:
        pd.DataFrame: DataFrame with selected columns after dropping irrelevant ones.
    """
    df = pd.read_csv(f'{path}/{city}.csv')
    df = df.drop(['title', 'url', 'city'], axis=1)
    return df


def preprocess_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts relevant columns to numeric types and drops rows with missing price values.

    Parameters:
        df (pd.DataFrame): Input DataFrame with raw data.

    Returns:
        pd.DataFrame: Cleaned DataFrame with correct types and no missing prices.
    """
    df['rent'] = df['rent'].replace('none', np.nan)
    df['rent'] = pd.to_numeric(df['rent'], errors='coerce')
    df['rooms'] = pd.to_numeric(df['rooms'], errors='coerce')
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df.dropna(subset=['price'])
    df['price'] = df['price'].astype('int32')
    return df


def encode_address(df: pd.DataFrame) -> pd.DataFrame:
    """
    Encodes the 'address' column based on average property prices per address.

    Parameters:
        df (pd.DataFrame): DataFrame with 'address' and 'price' columns.

    Returns:
        pd.DataFrame: DataFrame with 'address' replaced by its encoded value.
    """
    address_mean = df.groupby('address')['price'].mean()
    df['address_encoded'] = df['address'].map(address_mean)
    return df.drop(['address'], axis=1)


def encode_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    """
    One-hot encodes selected categorical columns.

    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with categorical variables one-hot encoded.
    """
    categorical_cols = ['district', 'floor_no', 'heating_info', 'building_type']
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    return df


def handle_rent_missing(df: pd.DataFrame, method='nan') -> pd.DataFrame:
    """
    Handles missing values in the 'rent' column using different strategies.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        method (str): Strategy for handling missing values:
                      'median', 'zero', 'drop', or 'nan' (default: 'nan').

    Returns:
        pd.DataFrame: DataFrame with missing 'rent' values handled.
    """
    if method == 'median':
        df['rent'] = df['rent'].fillna(df['rent'].median())
    elif method == 'zero':
        df['rent'] = df['rent'].fillna(0)
    elif method == 'drop':
        df = df.dropna(subset=['rent'])
    elif method == 'nan':
        pass
    return df


def save_data(df: pd.DataFrame, city: str, path: str):
    """
    Saves the processed DataFrame to a CSV file.

    Parameters:
        df (pd.DataFrame): The processed DataFrame.
        city (str): Name of the city (used in the filename).
        path (str): Directory where the file will be saved.
    """
    df.to_csv(f'{path}/{city}.csv', index=False)


# Entry point for processing
CITY = 'opole'
RAW_PATH = '../csv_data/raw'
PROCESSED_PATH = '../csv_data/processed'

df = load_data(CITY, RAW_PATH)
df = preprocess_types(df)
df = encode_address(df)
df = encode_categoricals(df)
df = handle_rent_missing(df)
save_data(df, CITY, PROCESSED_PATH)