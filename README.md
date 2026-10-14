# Universal Converter

A lightweight Flask web application for converting currencies, cryptocurrencies, time zones, temperatures, cooking volumes, lengths, and weights.

## Features

- Live currency and cryptocurrency exchange rates cached for 10 minutes
- Time zone conversion supporting flexible time formats (e.g., 3:23 PM, 15:23) and offset differences
- Temperature conversion with an interactive map to select and lookup live local temperatures
- Baking volume, length, and weight conversions
- Quick unit swapper and one-click result copy utilities

## Run locally

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py