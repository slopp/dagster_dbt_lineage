import duckdb

def load_raw():
    query = "CREATE TABLE raw AS SELECT * FROM \'seed.csv\';"
    con = duckdb.connect(database = "dbt_project/source.duckdb", read_only = False)
    con.execute(query)


if __name__ == "__main__":
    load_raw()