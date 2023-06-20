if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd


def metrics(df):
    # Calculate the Free Cash Flow
    df["freeCashFlow"] = df["operatingCashflow"] - df["capitalExpenditures"]

    # Calculate the Net Cash Flow
    df["netCashFlow"] = (
        df["operatingCashflow"]
        + df["cashflowFromInvestment"]
        + df["cashflowFromFinancing"]
    )

    # Calculate Operating Cash Flow to Net Income Ratio
    df["operatingCashflowToNetIncome"] = df["operatingCashflow"] / df["netIncome"]

    # Calculate Dividend Payout Ratio
    df["dividendPayoutRatio"] = df["dividendPayout"] / df["netIncome"]

    return df


def change_types(df):

    # List of columns to convert
    columns_to_convert = [
        "reportedCurrency",
        "operatingCashflow",
        "paymentsForOperatingActivities",
        "proceedsFromOperatingActivities",
        "changeInOperatingLiabilities",
        "changeInOperatingAssets",
        "depreciationDepletionAndAmortization",
        "capitalExpenditures",
        "changeInReceivables",
        "changeInInventory",
        "profitLoss",
        "cashflowFromInvestment",
        "cashflowFromFinancing",
        "proceedsFromRepaymentsOfShortTermDebt",
        "paymentsForRepurchaseOfCommonStock",
        "paymentsForRepurchaseOfEquity",
        "paymentsForRepurchaseOfPreferredStock",
        "dividendPayout",
        "dividendPayoutCommonStock",
        "dividendPayoutPreferredStock",
        "proceedsFromIssuanceOfCommonStock",
        "proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet",
        "proceedsFromIssuanceOfPreferredStock",
        "proceedsFromRepurchaseOfEquity",
        "proceedsFromSaleOfTreasuryStock",
        "changeInCashAndCashEquivalents",
        "changeInExchangeRate",
        "netIncome",
    ]

    # Convert them using astype
    for column in columns_to_convert:
        # Some values might be 'None' or other non-numeric strings, handle these cases with errors='coerce'
        df[column] = pd.to_numeric(df[column], errors="coerce")
    df["fiscalDateEnding"] = pd.to_datetime(df["fiscalDateEnding"])
    return df


@transformer
def transform(data, *args, **kwargs):

    dfs = []
    for data in data:

        # Check if 'annualReports' key exists in data
        if "annualReports" not in data:
            continue  # Skip this dictionary if key does not exist

        # Convert the annual reports data to a DataFrame
        df = pd.DataFrame(data["annualReports"])

        # Adding symbol to the DataFrame
        df["symbol"] = data["symbol"]

        # Append the DataFrame to the list
        dfs.append(df)

    # Concatenate all DataFrames in the list into a single DataFrame
    merged = pd.concat(dfs, ignore_index=True)

    types = change_types(merged)

    transformed = metrics(types)

    return transformed


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
