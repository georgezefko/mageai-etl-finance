if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, func
from sqlalchemy import inspect
import pandas as pd


@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """

    engine = create_engine(
        "duckdb:///stockapp.duckdb",
        connect_args={"read_only": False, "config": {"memory_limit": "1gb"}},
    )

    Session = sessionmaker(bind=engine)
    session = Session()

    metadata = MetaData()

    inspector = inspect(engine)
    # If the table doesn't exist, create it
    if not "daily_adjusted" in inspector.get_table_names():
        data.to_sql("daily_adjusted", engine)

    # Reflect the table
    daily_adjusted = Table("daily_adjusted", metadata, autoload_with=engine)

    # Print database URL
    print(f"Database URL: {engine.url}")

    # Print table names
    print(f"Table Names: {inspector.get_table_names()}")

    # Print schema of the table 'daily_adjusted'
    print(f"Schema of 'daily_adjusted': {inspector.get_columns('daily_adjusted')}")

    # Load the current data from the table
    stmt = select([daily_adjusted])
    current_data = pd.read_sql_query(stmt, con=engine)

    # Print first five rows
    print(f"First five rows: \n{current_data.head()}")

    # Filter out rows in data that already exist in current_data

    unique_rows = data[
        ~data.set_index(["Symbol", "Timeseries"]).index.isin(
            current_data.set_index(["Symbol", "Timeseries"]).index
        )
    ]

    print(f"Unique rows are:{len(unique_rows)}")
    # Assuming the 'index' column is not necessary, let's drop it
    current_data = current_data.drop(columns=["index"])

    # Insert unique_rows into the table
    unique_rows.to_sql("daily_adjusted", con=engine, if_exists="append", index=False)

    # Group by symbol
    stmt = select([daily_adjusted.c.Symbol, func.count()]).group_by(
        daily_adjusted.c.Symbol
    )
    results = session.execute(stmt).fetchall()

    print(results)

    session.commit()
    session.close()
