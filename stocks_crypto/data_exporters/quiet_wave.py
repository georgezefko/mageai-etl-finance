if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
import duckdb


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

    # to start an in-memory database
    con = duckdb.connect(database="finance")
    # to use a database file (shared between processes)
    con = duckdb.connect(database="finance.duckdb", read_only=False)

    # create a new table from the contents of a DataFrame
    # con.execute('CREATE TABLE IF NOT EXISTS main.test_df_table AS SELECT * FROM data')
    con.execute("CREATE TABLE items(item VARCHAR, value DECIMAL(10,2), count INTEGER)")
    # insert into an existing table from the contents of a DataFrame
    # con.execute('INSERT INTO test_df_table SELECT * FROM data')
    # retrieve the items again
    con.execute("SELECT * FROM main.test_df_table")
    print(con.fetchall())
    con.close()
