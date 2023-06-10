if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


import pandas as pd
from unittest.mock import patch
import requests


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    dfs = []
    for data in data:
        # Convert the time series data to a DataFrame
        df = pd.DataFrame(data["Time Series (Daily)"]).T

        # Convert index to datetime
        df.index = pd.to_datetime(df.index)
        df = df.reset_index()
        # Rename columns for clarity
        df.columns = [
            "index",
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
                "index",
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

        df.rename(
            columns={
                "index": "Timeseries",
                "2. Symbol": "Symbol",
                "3. Last Refreshed": "LastRefreshed",
                "5. Time Zone": "Timezone",
            },
            inplace=True,
        )
        dfs.append(df)
    transformed = pd.concat(dfs)

    # print(transformed.head())
    return transformed


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
    assert isinstance(output, pd.DataFrame)
    assert len(output.columns) == 12


@test
def test_load_data_api(mock_requests, **kwargs):
    # Mock a successful API response
    @patch("requests.get")
    def _test():
        mock_responses = [
            {
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
        ]

        mock_requests.return_value.json.return_value = mock_responses

        # Call the function and check the result
        result = load_data_from_api(**kwargs)
        assert isinstance(result, pd.DataFrame)
        assert result.iloc[0]["Symbol"] == "IBM"
        assert result.iloc[0]["Timezone"] == "US/Eastern"
        assert result.iloc[0]["open"] == 121.41
        assert result.iloc[0]["close"] == 122.84
