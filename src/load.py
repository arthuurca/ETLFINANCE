import pandas as pd
import os
import glob
from sqlalchemy import create_engine, text

processedPath = "data/processed"

db_User = 'admin'
db_pass = 'admin'
db_host = 'localhost'
db_port = '5432'
db_name = 'finance_dw'

database_Url = f"postgresql+psycopg2://{db_User}:{db_pass}@{db_host}:{db_port}/{db_name}"

def loadData():
    print("Starting data load to PostgreSQL...")

    files = glob.glob(f"{processedPath}/*.parquet")
    if not files:
        print("No processed files found. Run transform.py first!")
        return

    latestFile = sorted(files)[-1]
    print(f"Reading file for loading: {latestFile}")
    df = pd.read_parquet(latestFile)

    engine = create_engine(database_Url)

    try:
        df.to_sql('stock_prices', con=engine, if_exists='replace', index=False)

        print("Succes! Data loaded into table 'stock_prices'.")

        with engine.connect() as connection:
            result = connection.execute(text("SELECT count(*) FROM stock_prices"))
            count = result.fetchone()[0]
            print(f"Total rows in database: {count}")
    except Exception as e:
        print(f"Error loading data: {e}")


if __name__ == "__main__":
    loadData()