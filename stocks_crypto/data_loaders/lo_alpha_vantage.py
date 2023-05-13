import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from mage_ai.data_preparation.shared.secrets import get_secret_value




@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    KEY = get_secret_value('alphaVantageKey')
    print(KEY)
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=KEY'
    response = requests.get(url)
    data = response.json()
    print(data)
    return 


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
    assert isinstance(output, pd.DataFrame)