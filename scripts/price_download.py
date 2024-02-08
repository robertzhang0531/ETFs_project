import yfinance as yf
import time
import datetime
import pandas as pd
import os
from ticker_retrieval import get_etf_ticker_symbols

def download_price_data(tickers, start_date, end_date):
    """
    Downloads daily price data for given ETF tickers within the specified date range.

    Parameters:
    - tickers (list of str): List of ETF ticker symbols.
    - start_date (str): Start date for the data in 'YYYY-MM-DD' format.
    - end_date (str): End date for the data in 'YYYY-MM-DD' format.

    Returns:
    - dict: A dictionary with ticker symbols as keys and downloaded data as values.
    """
    data = {}
    for ticker in tickers:
        try:
            df = yf.download(ticker, start=start_date, end=end_date)
            data[ticker] = df
        except Exception as e:
            print(f"Error downloading data for {ticker}: {e}")
            time.sleep(10)
    return data

def get_user_date_input(prompt):
    """Prompts the user for a date input and validates the format, normalizing it to YYYY-MM-DD."""
    while True:
        date_str = input(prompt)
        try:
            valid_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            
            normalized_date_str = valid_date.strftime('%Y-%m-%d')
            return normalized_date_str
        except ValueError:
            try:
                valid_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                normalized_date_str = valid_date.strftime('%Y-%m-%d')
                return normalized_date_str
            except ValueError:
                # If a ValueError is raised, inform the user and prompt again
                print("Invalid date format. Please use YYYY-MM-DD format.")

def main():
    api_key = 'REPLACE WITH YOUR API KEY'
    tickers = get_etf_ticker_symbols(api_key)  # Dynamically fetch ticker symbols using ticker retrieval script
    start_date = get_user_date_input("Enter the start date (YYYY-MM-DD): ")
    end_date = get_user_date_input("Enter the end date (YYYY-MM-DD): ")
    print(f"Start Date: {start_date}, End Date: {end_date}")
    etf_data = download_price_data(tickers, start_date, end_date)
    
    base_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'etf_csvs')
    os.makedirs(base_path, exist_ok=True)
    
    # Process and save each ETF's DataFrame to a CSV file
    for ticker, df in etf_data.items():
        if not df.empty:
            csv_filename = f"{ticker}_prices_{start_date}_to_{end_date}.csv"
            csv_path = os.path.join(base_path, csv_filename)
            df.to_csv(csv_path, index=True)
            print(f"Saved data for {ticker} to {csv_path}")
        else:
            print(f"No data to save for {ticker}.")

if __name__ == "__main__":
    main()
