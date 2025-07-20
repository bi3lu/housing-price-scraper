# -*- coding: utf-8 -*-
"""
Description:

Author: Jakub Bielecki
Created: 20-07-2025
"""


import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from xgboost import XGBRegressor


def load_data(city: str, path: str):
    df = pd.read_csv(f'{path}/{city}.csv')
    return df


def split_data(df: pd.DataFrame):
    X = df.drop('price', axis=1)
    y = df['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return (X_train, X_test, y_train, y_test)


def train_model(X_train, y_train):
    model = XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=6,
        random_state=42,
        n_jobs=-1,
        tree_method='hist',
        enable_categorical=False
    )
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mae)
    return {
        'R2': r2,
        'MAE': mae,
        'RMSE': rmse
    }


def save_model_report(metrics: dict, path: str = 'xgb_model_report.txt'):
    with open(path, 'w') as f:
        for k, v in metrics.items():
            f.write(f'{k}: {v:.4f}\n')
    return None


def save_model(model, path: str = 'xgb_model.joblib'):
    joblib.dump(model, path)
    return None


# entry point:
PATH = '../../csv_data/processed'
CITY = 'opole'


df = load_data(CITY, PATH)
X_train, X_test, y_train, y_test = split_data(df)
model = train_model(X_train, y_train)
metrics = evaluate_model(model, X_test, y_test)


save_model_report(metrics)
save_model(model)