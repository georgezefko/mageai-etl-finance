if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test
from mage_ai.data_preparation.shared.secrets import get_secret_value
from unittest.mock import patch, MagicMock
import io
import requests


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
        url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={i}&apikey={KEY}"
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
