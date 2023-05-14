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
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&outputsize=full&apikey=KEY'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    # Convert the time series data to a DataFrame
    df = pd.DataFrame(data["Time Series (Daily)"]).T

    # Convert index to datetime
    df.index = pd.to_datetime(df.index)

    # Rename columns for clarity
    df.columns = ['open', 'high', 'low', 'close', 'volume','adjusted close','dividend amount','split coefficient']

    # Convert the data type of each column to float or integer as appropriate
    df = df.astype({'open': 'float', 'high': 'float', 'low': 'float', 'close': 'float', 'volume': 'int','adjusted close':'float','dividend amount':'float','split coefficient':'float'})

    # Adding metadata to the DataFrame
    for key, value in data["Meta Data"].items():
        df[key] = value
    
    df.info()
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
    assert isinstance(output, pd.DataFrame)
