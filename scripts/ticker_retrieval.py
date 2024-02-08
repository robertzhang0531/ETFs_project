import yfinance as yf
import time
import requests
import json
import os

class ETFDataRetriever:
    """
    A class for retrieving, validating, and saving ETF data using the IEX Cloud API.
    """

    def __init__(self, api_key):
        """
        Initializes the ETFDataRetriever with an IEX Cloud API key.
        
        Parameters:
        - api_key (str): The API key for accessing IEX Cloud.
        """
        self.api_key = api_key

    def fetch_etf_tickers(self):
        """
        Fetches a list of ETF tickers from IEX Cloud.

        Returns:
        - list: A list of dictionaries, each containing ETF ticker information.
        """
        url = "https://cloud.iexapis.com/stable/ref-data/symbols"
        params = {"token": self.api_key}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if not data:  # Validate non-empty response
                print("No data retrieved from the API.")
                return []
            
            # Validate expected data structure
            if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
                print("Unexpected data format received.")
                return []

            # Filter for ETFs and validate presence of 'symbol'
            etf_tickers = [item for item in data if item.get('type') == 'et' and 'symbol' in item]
            return etf_tickers
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            return []

    @staticmethod
    def save_etf_data_to_json(etf_data, file_path='etf_data.json'):
        """
        Saves ETF data to a JSON file.

        Parameters:
        - etf_data (list): A list of dictionaries containing ETF information.
        - file_path (str): The name of the JSON file where data will be stored.
        """
        base_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'etfs_json')
        full_file_path = os.path.join(base_path, file_path)
        
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
        
        # Write the ETF data to the specified JSON file
        with open(full_file_path, 'w') as file:
            json.dump(etf_data, file, indent=4)

    @staticmethod
    def validate_etf_data(etf_data):
        """
        Validates the ETF data for completeness and correctness.

        Parameters:
        - etf_data (list): A list of dictionaries containing ETF information.

        Returns:
        - list: A validated list of ETF data.
        """
        validated_data = [item for item in etf_data if 'symbol' in item and 'name' in item]
        return validated_data

    def validate_and_update_etf_data(self, file_name='etf_data.json'):
        """
        Updates the ETF data JSON file with the latest information.

        Parameters:
        - file_path (str): Path to the JSON file where data is stored.
        """
        base_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'etfs_json')
        full_file_path = os.path.join(base_path, file_name)
        
        new_data = self.fetch_etf_tickers()
        new_data = self.validate_etf_data(new_data)
        
        try:
            if os.path.exists(full_file_path):
                with open(full_file_path) as file:
                    existing_data = json.load(file)
            else:
                existing_data = []
        except json.JSONDecodeError:
            existing_data = []

        updated_data = {item['symbol']: item for item in existing_data + new_data}
        self.save_etf_data_to_json(list(updated_data.values()), full_file_path)

def get_etf_ticker_symbols(api_key, file_name='etf_data.json'):
    etf_retriever = ETFDataRetriever(api_key)
    base_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'etfs_json')
    full_file_path = os.path.join(base_path, file_name)
    
    etf_retriever.validate_and_update_etf_data(full_file_path)
    
    with open(full_file_path, 'r') as file:
        etf_data = json.load(file)
    return [etf['symbol'] for etf in etf_data]


def main():
    api_key = 'REPLACE WITH YOUR API KEY'
    etf_retriever = ETFDataRetriever(api_key)
    try:
        etf_retriever.validate_and_update_etf_data()
        tickers = get_etf_ticker_symbols(api_key)
        print(tickers)
        print("ETF data retrieved and saved successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(10)
        etf_retriever.validate_and_update_etf_data()

if __name__ == "__main__":
    main()
