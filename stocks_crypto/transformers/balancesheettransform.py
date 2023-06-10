if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


import pandas as pd


def metrics(df):
    df["currentRatio"] = df["totalCurrentAssets"] / df["totalCurrentLiabilities"]
    df["quickRatio"] = (
        df["cashAndCashEquivalentsAtCarryingValue"]
        + df["shortTermInvestments"]
        + df["currentNetReceivables"]
    ) / df["totalCurrentLiabilities"]
    df["debtEquityRatio"] = df["totalLiabilities"] / df["totalShareholderEquity"]
    df["longTermDebtEquityRatio"] = df["longTermDebt"] / df["totalShareholderEquity"]
    return df


def change_types(df):

    # List of columns to convert
    columns_to_convert = [
        "totalAssets",
        "totalCurrentAssets",
        "cashAndCashEquivalentsAtCarryingValue",
        "cashAndShortTermInvestments",
        "inventory",
        "currentNetReceivables",
        "totalNonCurrentAssets",
        "propertyPlantEquipment",
        "accumulatedDepreciationAmortizationPPE",
        "intangibleAssets",
        "intangibleAssetsExcludingGoodwill",
        "goodwill",
        "investments",
        "longTermInvestments",
        "shortTermInvestments",
        "otherCurrentAssets",
        "otherNonCurrentAssets",
        "totalLiabilities",
        "totalCurrentLiabilities",
        "currentAccountsPayable",
        "deferredRevenue",
        "currentDebt",
        "shortTermDebt",
        "totalNonCurrentLiabilities",
        "capitalLeaseObligations",
        "longTermDebt",
        "currentLongTermDebt",
        "longTermDebtNoncurrent",
        "shortLongTermDebtTotal",
        "otherCurrentLiabilities",
        "otherNonCurrentLiabilities",
        "totalShareholderEquity",
        "treasuryStock",
        "retainedEarnings",
        "commonStock",
        "commonStockSharesOutstanding",
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

    assert output is not None, "The output is undefined"
    assert isinstance(output, pd.DataFrame)
    assert len(output.columns) == 43
    assert len(output["symbol"].unique()) == 5


@test
def test_change_types(output, *args) -> None:
    expected_types = {
        "fiscalDateEnding": "datetime64[ns]",
        "reportedCurrency": "object",
        "totalAssets": "int64",
        "totalCurrentAssets": "int64",
        "cashAndCashEquivalentsAtCarryingValue": "int64",
        "cashAndShortTermInvestments": "int64",
        "inventory": "int64",
        "currentNetReceivables": "int64",
        "totalNonCurrentAssets": "int64",
        "propertyPlantEquipment": "int64",
        "accumulatedDepreciationAmortizationPPE": "float64",
        "intangibleAssets": "float64",
        "intangibleAssetsExcludingGoodwill": "float64",
        "goodwill": "float64",
        "investments": "float64",
        "longTermInvestments": "float64",
        "shortTermInvestments": "float64",
        "otherCurrentAssets": "float64",
        "otherNonCurrentAssets": "float64",
        "totalLiabilities": "int64",
        "totalCurrentLiabilities": "int64",
        "currentAccountsPayable": "int64",
        "deferredRevenue": "int64",
        "currentDebt": "float64",
        "shortTermDebt": "int64",
        "totalNonCurrentLiabilities": "int64",
        "capitalLeaseObligations": "float64",
        "longTermDebt": "int64",
        "currentLongTermDebt": "int64",
        "longTermDebtNoncurrent": "float64",
        "shortLongTermDebtTotal": "int64",
        "otherCurrentLiabilities": "int64",
        "otherNonCurrentLiabilities": "int64",
        "totalShareholderEquity": "int64",
        "treasuryStock": "float64",
        "retainedEarnings": "int64",
        "commonStock": "int64",
        "commonStockSharesOutstanding": "int64",
    }

    # Check data types for each column
    for column, expected_type in expected_types.items():
        assert (
            output[column].dtypes == expected_type
        ), f"Unexpected data type for {column}"
