# -*- coding: utf-8 -*-
"""
Description:

Author: Jakub Bielecki
Created: 20-07-2025
"""


import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor


def load_data(city: str, path: str):
    df = pd.read_csv(f'{path}/{city}.csv')
    return df


def split_data(df: pd.DataFrame):
    X = df.drop('price', axis=1)
    y = df['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return (X_train, X_test, y_train, y_test)


def train_model(x_train, y_train):
    model = XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=6,
        random_state=42,
        n_jobs=-1,
        tree_method='hist',
        enable_categorical=False
    )
    model.fit(x_train, y_train)
    return model


# entry point:
PATH = '../csv_data/processed'
CITY = 'opole'


df = load_data(CITY, PATH)
X_train, X_test, y_train, y_test = split_data(df)
model = train_model(X_train, y_train)