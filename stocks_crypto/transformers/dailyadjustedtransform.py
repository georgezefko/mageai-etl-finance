if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


import pandas as pd


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

        df.rename(
            columns={
                "2. Symbol": "Symbol",
                "3. Last Refreshed": "LastRefreshed",
                "5. Time Zone": "Timezone",
            },
            inplace=True,
        )
        dfs.append(df)
    transformed = pd.concat(dfs)
    return transformed


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
    assert isinstance(output, pd.DataFrame)
    assert len(output.columns) == 11

    assert len(output.Symbol.unique()) == 4


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
