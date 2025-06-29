# Housing Price Scraper – Otodom

A simple Python script to scrape apartment sale listings from [otodom.pl](https://www.otodom.pl), for a selected **voivodeship** (region) and **city** in Poland.  
The results are saved to a CSV file for further analysis or storage.

---

## Requirements

- Python 3.7 or higher
- Python packages:
  - `requests`
  - `beautifulsoup4`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## How to Run

From the `src/` directory:

```bash
python housing_scrapper/housing_scrapper.py
```

The script will fetch listings for the configured location and save them to:

```
csv_data/otodom_<city>.csv
```

---

## Features

- Automatically detects the total number of listing pages.
- Handles missing values (e.g., hidden prices or incomplete addresses).
- Removes duplicate listings by ID.
- Extracts key information:
  - Title, price, area, number of rooms
  - City, street address, district
  - Listing URL

---

## Author

Jakub Bielecki