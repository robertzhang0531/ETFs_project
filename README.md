# ETF Data Retrieval and Management System

## Project Overview

This project develops a Python-based system for dynamically retrieving, validating, and managing a comprehensive list of US ETF tickers and their details using the IEX Cloud API. The system stores the data in a JSON file, ensuring easy access and update capabilities, and features a web dashboard for interactive data visualization.

## Codebase Structure

```bash
< PROJECT ROOT >
   |
   |-- data/                                # Data storage directory
   |    |-- etf_json/                       # Stores ETF information in JSON format
   |    |    |-- etf_data.json              # JSON file containing ETF tickers and details
   |    |
   |    |-- etf_csvs/                       # Stores downloaded ETF price data in CSV format
   |         |-- <ticker>_prices.csv        # CSV files for each ETF's price data
   |
   |-- scripts/                             # Directory for Python scripts
   |    |-- ticker_retrieval.py             # Script for retrieving and saving ETF tickers
   |    |-- price_download.py               # Script for downloading ETF price data
   |
   |-- templates/                           # HTML templates for the web dashboard
   |    |-- index.html                      # Main template for displaying the dashboard
   |
   |-- app.py                               # Flask application for serving the web dashboard
   |
   |-- README.md                            # Project documentation and setup instructions
   |
   |-- ************************************************************************
```


- **Scripts**:
  - `ticker_retrieval.py`: Contains the `ETFDataRetriever` class responsible for fetching ETF tickers from the IEX Cloud API, validating the retrieved data, and saving it as JSON.
  - `price_download.py`: Utilizes `yfinance` to download and save historical price data for the ETFs into CSV files. It integrates with `ticker_retrieval.py` to dynamically determine available ETFs.

- **Data**:
  - `/data/etf_json/`: Directory where the JSON file containing ETF tickers and basic information is saved.
  - `/data/etf_csvs/`: Directory for storing the downloaded CSV files with ETF price data.

- **Web Dashboard** (`app.py`):
  - A Flask application that serves a web dashboard, allowing users to select an ETF and visualize its price data. It dynamically loads available ETFs and their historical price data for interactive exploration.

- **Templates**:
  - `index.html`: The HTML template for the web dashboard, featuring form inputs for ETF selection and checkboxes for choosing which data points (e.g., Open, High, Low, Close, Volume) to display.

## Function Descriptions

### `ticker_retrieval.py`

- **`ETFDataRetriever` Class**: Interacts with the IEX Cloud API to fetch and process ETF ticker information.
  - `__init__(self, api_key)`: Initializes the instance with an IEX Cloud API key.
  - `fetch_etf_tickers(self)`: Retrieves a list of ETF tickers, filtering and validating the data to include only relevant ETF information.
  - `save_etf_data_to_json(self, etf_data, file_path='etf_data.json')`: Saves the fetched ETF data as a JSON file at the specified path.
  - `validate_etf_data(self, etf_data)`: Ensures that essential information is present in the ETF data.
  - `validate_and_update_etf_data(self, file_path='etf_data.json')`: Retrieves, validates, and updates the ETF data in local JSON storage.

### `price_download.py`

- **`download_price_data(tickers, start_date, end_date)`**: Downloads historical price data for specified ETF tickers within a given date range using `yfinance`.
  - `tickers`: List of ETF ticker symbols.
  - `start_date`: Start date for data retrieval in `'YYYY-MM-DD'` format.
  - `end_date`: End date for data retrieval in `'YYYY-MM-DD'` format.
  
- **`get_user_date_input(prompt)`**: Prompts the user for a date, ensuring it matches the expected `'YYYY-MM-DD'` format.

### Web Dashboard (`app.py`)

- **`load_etf_info()`**: Dynamically loads available ETF tickers and their corresponding CSV file paths based on the `data/etf_csvs/` directory content.
- **`index()`**: The main view function for the Flask application. It processes form submissions, generates interactive charts with Plotly based on user-selected data points, and renders the dashboard page.

## Example Working Pipeline

1. **Setting Up**: Ensure Python and required packages are installed (Flask, Pandas, Plotly, and yfinance).
2. **Running the Scripts**:
   - Run `python ticker_retrieval.py` to fetch and save the latest list of ETF tickers as JSON.
   - Run `python price_download.py` to download historical price data for these ETFs and save them as CSVs.
3. **Launching the Web Dashboard**:
   - Execute `python app.py` to start the Flask server.
   - Open a web browser and navigate to `http://127.0.0.1:5000/` to access the dashboard.
   - Select an ETF and data points to visualize the historical price data interactively.
