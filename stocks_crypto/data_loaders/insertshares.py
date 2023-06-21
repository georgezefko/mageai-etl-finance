if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, func
from sqlalchemy import inspect
import pandas as pd


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
    Session = sessionmaker(bind=engine)
    session = Session()

    metadata = MetaData()

    inspector = inspect(engine)

    # Print database URL
    print(f"Database URL: {engine.url}")

    # Print table names
    print(f"Table Names: {inspector.get_table_names()}")
    # Select all data from the table
    query = f"SELECT * FROM adjustD"
    data = pd.read_sql_query(query, con=engine)

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
