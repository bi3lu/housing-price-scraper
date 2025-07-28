# -*- coding: utf-8 -*-
"""
xboost_model.py

This script trains an XGBoost regression model to predict real estate prices based on
processed housing data. It handles loading data, splitting into training and test sets,
model training, evaluation, and saving both the trained model and evaluation report.

Author: Jakub Bielecki
Created: 20-07-2025
"""


import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from xgboost import XGBRegressor


def load_data(city: str, path: str) -> pd.DataFrame:
    """
    Loads processed housing data from a CSV file.

    Parameters:
        city (str): Name of the city (used in filename).
        path (str): Directory containing the processed CSV.

    Returns:
        pd.DataFrame: DataFrame containing features and target variable.
    """
    df = pd.read_csv(f'{path}/{city}.csv')
    return df


def split_data(df: pd.DataFrame):
    """
    Splits data into features (X) and target (y), then into train and test sets.

    Parameters:
        df (pd.DataFrame): Input DataFrame containing 'price' as target.

    Returns:
        Tuple: X_train, X_test, y_train, y_test.
    """
    X = df.drop('price', axis=1)
    y = df['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return (X_train, X_test, y_train, y_test)


def train_model(X_train, y_train) -> XGBRegressor:
    """
    Trains an XGBoost regression model using training data.

    Parameters:
        X_train (pd.DataFrame): Training features.
        y_train (pd.Series): Training target values.

    Returns:
        XGBRegressor: Trained XGBoost model.
    """
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


def evaluate_model(model, X_test, y_test) -> dict:
    """
    Evaluates the model's performance using R², MAE, and RMSE.

    Parameters:
        model (XGBRegressor): Trained model.
        X_test (pd.DataFrame): Test features.
        y_test (pd.Series): True target values.

    Returns:
        dict: Dictionary containing R², MAE, and RMSE scores.
    """
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
    """
    Saves model evaluation metrics to a text file.

    Parameters:
        metrics (dict): Dictionary of model performance metrics.
        path (str): Output file path for the report.
    """
    with open(path, 'w') as f:
        for k, v in metrics.items():
            f.write(f'{k}: {v:.4f}\n')
    return None


def save_model(model, path: str = 'xgb_model.joblib'):
    """
    Saves the trained XGBoost model to a file using joblib.

    Parameters:
        model (XGBRegressor): Trained model.
        path (str): Output file path for the model file.
    """
    joblib.dump(model, path)
    return None


# Entry point for processing
PATH = '../../csv_data/processed'
CITY = 'opole'

df = load_data(CITY, PATH)
X_train, X_test, y_train, y_test = split_data(df)
model = train_model(X_train, y_train)
metrics = evaluate_model(model, X_test, y_test)

save_model_report(metrics)
save_model(model)