import io

import pandas as pd
import requests

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test
from mage_ai.data_preparation.shared.secrets import get_secret_value
from unittest.mock import patch, MagicMock


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    dfs = []
    stocks = ["IBM", "AAPL", "AMZN", "NVDA", "TSLA"]

    KEY = get_secret_value("alphaVantageKey")
    for i in stocks:
        print(i)
        url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={i}&apikey={KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        dfs.append(data)
    return dfs


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"


@test
def test_symbols(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    # List of expected symbols
    expected_symbols = ["IBM", "AAPL", "AMZN", "NVDA", "TSLA"]

    # Check for presence and consistency of symbols
    for data in output:
        if isinstance(data, str):
            print("Data is a string, not a JSON object")
            continue
        assert "symbol" in data, f"Missing symbol in one of the JSON objects: {data}"
        assert (
            data["symbol"] in expected_symbols
        ), f"Inconsistent symbol: {data['symbol']}"
