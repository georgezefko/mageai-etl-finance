if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd


@transformer
def transform(df_state, df_daily, df_balance, *args, **kwargs):
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

    df_daily["dividend_yield"] = df_daily["dividend amount"] / df_daily["close"]
    # Set 'Timeseries' as the index
    df_daily.set_index("Timeseries", inplace=True)

    df_daily["Year"] = df_daily.index.year
    # Resample to annual frequency, taking the last observation in each year
    df_daily = (
        df_daily.groupby(["Year", "Symbol"])
        .agg(
            {
                "open": "mean",
                "high": "mean",
                "low": "mean",
                "close": "mean",
                "adjusted close": "mean",
                "volume": "sum",  # Usually, we sum volumes over periods rather than average
                "dividend amount": "sum",  # You might also want to sum dividends
                "dividend_yield": "sum",
                "split coefficient": "last",  # You might want to keep the last known split coefficient
            }
        )
        .reset_index()
    )

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
        "grossMargin",
        "operatingMargin",
        "netProfitMargin",
        "rdIntensity",
        "interestCoverageRatio",
    ]

    stock_columns = [
        "Symbol",
        "Year",
        "open",
        "high",
        "low",
        "close",
        "adjusted close",
        "volume",  # Usually, we sum volumes over periods rather than average
        "dividend amount",  # You might also want to sum dividends
        "split coefficient",
        "dividend_yield",
    ]

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

    # Add 'Year' column
    df_balance["Year"] = df_balance["fiscalDateEnding"].dt.year

    balance_columns = [
        "symbol",
        "Year",
        "currentRatio",
        "quickRatio",
        "debtEquityRatio",
        "longTermDebtEquityRatio",
    ]
    df_balance = df_balance[balance_columns]

    merged_data = pd.merge(
        merged_data,
        df_balance,
        left_on=["symbol", "Year"],
        right_on=["symbol", "Year"],
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

    assert len(output["symbol"].unique()) == 4
