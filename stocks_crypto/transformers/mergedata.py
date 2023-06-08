if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd


@transformer
def transform(df_state, df_daily, *args, **kwargs):
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

    # Set 'Timeseries' as the index
    df_daily.set_index("Timeseries", inplace=True)

    # Resample to annual frequency, taking the last observation in each year
    df_daily = df_daily.resample("Y").last()

    # Add 'Year' column
    df_daily["Year"] = df_daily.index.year

    # Add 'Year' column
    df_state["Year"] = df_state["fiscalDateEnding"].dt.year

    # Specify the necessary columns for the financial data and the stocks data
    financial_columns = [
        "symbol",
        "Year",
        "totalRevenue",
        "grossProfit",
        "operatingIncome",
        "netIncome",
        "researchAndDevelopment",
    ]

    stock_columns = ["Symbol", "Year", "adjusted close", "volume"]

    # Filter out the necessary columns
    df_state = df_state[financial_columns]
    df_daily = df_daily[stock_columns]

    # Merge on 'symbol'/'Symbol' and 'Year'
    merged_data = pd.merge(
        df_state,
        df_daily,
        left_on=["symbol", "Year"],
        right_on=["Symbol", "Year"],
        how="inner",
    )

    # Drop redundant 'Symbol' column
    merged_data = merged_data.drop("Symbol", axis=1)
    return merged_data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
    assert len(output["symbol"].unique()) == 5
