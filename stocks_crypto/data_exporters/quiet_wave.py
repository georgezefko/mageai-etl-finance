if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
import duckdb
import sqlalchemy


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
    # Specify your data exporting logic here
    print(args)
    # to start an in-memory database
    con = duckdb.connect(database="finance")

    # create a new table from the contents of a DataFrame
    con.execute("CREATE TABLE IF NOT EXISTS main.daily_adjusted AS SELECT * FROM data")

    # Create a temporary table with your DataFrame
    con.execute("CREATE TEMPORARY TABLE temp_daily_adjusted AS SELECT * FROM df_table")

    con.execute(
        "INSERT INTO main.test_df_table SELECT * FROM temp_daily_adjusted WHERE (Symbol,Timeseries) NOT IN (SELECT Symbol, Timeseries FROM main.daily_adjusted)"
    )
    # con.execute("SELECT * FROM main.test_df_table")
    print(con.fetchall())
    con.close()
