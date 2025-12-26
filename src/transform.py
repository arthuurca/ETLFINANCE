import pandas as pd
import glob
import os

rawPath = "data/raw"
processedPath = "data/processed"

def transformData():
    print("Starting data transformation...")

    rawFiles = glob.glob(f"{rawPath}/*.parquet")

    if not rawFiles:
        print(f"No files found in {rawPath}. Please run extract.py first!")
        return
    
    latestFile = sorted(rawFiles)[-1]
    print(f"Reading file: {latestFile}")

    df = pd.read_parquet(latestFile)

    # Stardinization; turning Yahoo finance names to sql friendly names

    df.rename(columns={
            'Date': 'date',
            'Ticker': 'ticker',
            'Close': 'close',
            'High': 'high',
            'Low': 'low',
            'Open': 'open',
            'Volume': 'volume'
        }, inplace=True)
    

    df['date'] = pd.to_datetime(df['date'])

    df.dropna(inplace=True)

    if not os.path.exists(processedPath):
        os.makedirs(processedPath)

    fileName = os.path.basename(latestFile)
    targetPath = f"{processedPath}/{fileName}"

    df.to_parquet(targetPath)
    print(f"Success! Clean data saved to: {targetPath}")
    print(df.head())

if __name__ == "__main__":
    transformData()
        