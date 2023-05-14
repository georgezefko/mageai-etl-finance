import io
from unittest.mock import patch

import pandas as pd
import requests

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test
from mage_ai.data_preparation.shared.secrets import get_secret_value


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    KEY = get_secret_value("alphaVantageKey")
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&outputsize=full&apikey=KEY"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    # Convert the time series data to a DataFrame
    df = pd.DataFrame(data["Time Series (Daily)"]).T

    # Convert index to datetime
    df.index = pd.to_datetime(df.index)

    # Rename columns for clarity
    df.columns = [
        "open",
        "high",
        "low",
        "close",
        "adjusted close",
        "volume",
        "dividend amount",
        "split coefficient",
    ]

    # Convert the data type of each column to float or integer as appropriate
    df = df.astype(
        {
            "open": "float",
            "high": "float",
            "low": "float",
            "close": "float",
            "adjusted close": "float",
            "volume": "int",
            "dividend amount": "float",
            "split coefficient": "float",
        }
    )

    # Adding metadata to the DataFrame
    for key, value in data["Meta Data"].items():
        df[key] = value

    # return df information
    df = df[
        [
            "2. Symbol",
            "open",
            "high",
            "low",
            "close",
            "adjusted close",
            "volume",
            "dividend amount",
            "split coefficient",
            "3. Last Refreshed",
            "5. Time Zone",
        ]
    ]
    # df = df.reset_index()
    df.rename(
        columns={
            "2. Symbol": "Symbol",
            "3. Last Refreshed": "LastRefreshed",
            "5. Time Zone": "Timezone",
        },
        inplace=True,
    )

    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
    assert isinstance(output, pd.DataFrame)
    assert len(output.columns) == 11


@test
@patch("requests.get")
def test_load_data_api(output, mock_requests, **kwargs):
    # Mock a successful API response
    mock_response = {
        "Meta Data": {
            "1. Information": "Daily Time Series with Splits and Dividend Events",
            "2. Symbol": "IBM",
            "3. Last Refreshed": "2023-05-12",
            "4. Output Size": "Compact",
            "5. Time Zone": "US/Eastern",
        },
        "Time Series (Daily)": {
            "2023-05-12": {
                "1. open": "121.41",
                "2. high": "122.86",
                "3. low": "121.11",
                "4. close": "122.84",
                "5. adjusted close": "122.84",
                "6. volume": "4564825",
                "7. dividend amount": "0.0000",
                "8. split coefficient": "1.0",
            }
        },
    }

    mock_requests.return_value.json.return_value = mock_response

    # Call the function and check the result
    result = load_data_from_api(**kwargs)
    assert isinstance(result, pd.DataFrame)
    assert result.iloc[0]["Symbol"] == "IBM"
    assert result.iloc[0]["Timezone"] == "US/Eastern"
    assert result.iloc[0]["open"] == 121.41
    assert result.iloc[0]["close"] == 122.84
