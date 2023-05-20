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
    # print(data.head)
    # to start an in-memory database
    # con = duckdb.connect(database="finance")
    con = duckdb.connect(database="finance.duckdb", read_only=False)

    # create a new table from the contents of a DataFrame
    con.execute("CREATE TABLE IF NOT EXISTS main.daily_adjusted AS SELECT * FROM data")

    # Load the current data from the table
    current_data = con.execute("SELECT * FROM main.daily_adjusted").fetch_df()

    # Assuming 'data' is your new DataFrame
    # Filter out rows in data that already exist in current_data
    unique_rows = data[
        ~data.set_index(["Symbol", "TimeSeries"]).index.isin(
            current_data.set_index(["Symbol", "TimeSeries"]).index
        )
    ]

    # Insert unique_rows into the table
    con.register("unique_rows", unique_rows)
    con.execute("INSERT INTO main.daily_adjusted SELECT * FROM unique_rows")

    con.execute("SELECT Symbol,count(*) FROM main.daily_adjusted group by 1")
    print(con.fetchall())
    con.close()
