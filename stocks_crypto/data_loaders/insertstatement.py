if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    engine = create_engine(
        "duckdb:///stockapp.duckdb",
        connect_args={"read_only": False, "config": {"memory_limit": "1gb"}},
    )

    # Select all data from the table
    query = f"SELECT * FROM financialState"
    data = pd.read_sql_query(query, con=engine)

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
