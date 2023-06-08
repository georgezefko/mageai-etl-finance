if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


import pandas as pd


def metrics(df):
    df["grossMargin"] = df["grossProfit"] / df["totalRevenue"]
    df["operatingMargin"] = df["operatingIncome"] / df["totalRevenue"]
    df["netProfitMargin"] = df["netIncome"] / df["totalRevenue"]
    df["rdIntensity"] = df["researchAndDevelopment"] / df["totalRevenue"]
    df["interestCoverageRatio"] = df["ebit"] / df["interestAndDebtExpense"]
    return df


def change_types(df):

    # List of columns to convert
    columns_to_convert = [
        "grossProfit",
        "totalRevenue",
        "costOfRevenue",
        "costofGoodsAndServicesSold",
        "operatingIncome",
        "sellingGeneralAndAdministrative",
        "researchAndDevelopment",
        "operatingExpenses",
        "netInterestIncome",
        "interestIncome",
        "interestExpense",
        "nonInterestIncome",
        "otherNonOperatingIncome",
        "depreciation",
        "depreciationAndAmortization",
        "incomeBeforeTax",
        "incomeTaxExpense",
        "interestAndDebtExpense",
        "netIncomeFromContinuingOperations",
        "comprehensiveIncomeNetOfTax",
        "ebit",
        "ebitda",
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
    assert output is not None, "The output is undefined"
    assert isinstance(output, pd.DataFrame)
    assert len(output.columns) == 32
    assert len(output["symbol"].unique()) == 5


@test
def test_change_types(output, *args) -> None:
    expected_types = {
        "fiscalDateEnding": "datetime64[ns]",
        "reportedCurrency": "object",
        "grossProfit": "int64",
        "totalRevenue": "int64",
        "costOfRevenue": "int64",
        "costofGoodsAndServicesSold": "int64",
        "operatingIncome": "int64",
        "sellingGeneralAndAdministrative": "int64",
        "researchAndDevelopment": "int64",
        "operatingExpenses": "int64",
        "netInterestIncome": "int64",
        "interestIncome": "int64",
        "interestExpense": "int64",
        "nonInterestIncome": "float64",
        "otherNonOperatingIncome": "int64",
        "depreciation": "int64",
        "depreciationAndAmortization": "int64",
        "incomeBeforeTax": "int64",
        "incomeTaxExpense": "int64",
        "interestAndDebtExpense": "int64",
        "netIncomeFromContinuingOperations": "int64",
        "comprehensiveIncomeNetOfTax": "int64",
        "ebit": "int64",
        "ebitda": "int64",
        "netIncome": "int64",
        "symbol": "object",
        "grossMargin": "float64",
        "operatingMargin": "float64",
        "netProfitMargin": "float64",
        "rdIntensity": "float64",
        "interestCoverageRatio": "float64",
    }

    # Check data types for each column
    for column, expected_type in expected_types.items():
        assert (
            output[column].dtypes == expected_type
        ), f"Unexpected data type for {column}"
