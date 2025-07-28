# Housing Scraper – Otodom

A modular Python pipeline to **scrape**, **enrich**, **preprocess**, and **train a model** on apartment sale listings from [otodom.pl](https://www.otodom.pl), for a selected **voivodeship** (region) and **city** in Poland.

The pipeline extracts data, processes features, and trains an XGBoost regression model to predict apartment prices.

---

## Requirements

- Python 3.7 or higher
- Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Project structure

src/
├── data_preprocessing/
│   ├── data_preprocessing.py     # Data cleaning and encoding
├── housing_scraper/              # Web scraping scripts
│   ├── housing_scraper_sup.py    # Enrichment of raw data with details
│   ├── housing_scraper.py        # Main scraper
├── model/
│   ├── xgboost_model/
│   |  ├── xgboost_model.py       # XGBoost model training and evaluation
├── requirements.txt

---

## How to run

### 1. Scrape data from otodom
```bash
python housing_scraper/housing_scraper.py
```

This saves listings to:
```bash
csv_data/temp/otodom_<city>.csv
```

### 2. Enrich scraped data with extra details
```bash
python housing_scraper/housing_scraper_sup.py
```

This outputs:
```bash
csv_data/raw/<city>.csv
```

### 3. Preprocess the data
```bash
python data_preprocessing.py
```

Processed data is saved to:
```bash
csv_data/processed/<city>.csv
```

### 4. Train the model
```bash
python xboost_model.py
```

Generates:
- `xgb_model.joblib` (saved model)
- `xgb_model_report.txt` (R², MAE, RMSE)

---

## Features
- Automatically detects the number of listing pages (pagination).
- Handles missing values (rent, price, rooms, etc.).
- Encodes categorical features (floor, heating, building type, district, etc.).
- Trains XGBoost regression model to predict apartment prices.
- Saves model and evaluation report.

---

## Author
*Jakub Bielecki*