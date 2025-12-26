import yfinance as yf
import pandas as pd
import os
from datetime import datetime

tickers = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'WEGE3.SA']

def dataExtract():
    print(f"[{datetime.now()}] Iniciando extração dos dados...")

    dados = yf.download(tickers, period="1y", interval="1d", group_by='ticker')

    dados = dados.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index() 
    #transforma para que seja 1 linha por data e ticker para não ficar no formato estranho recebido pelo yfinance

    dados.columns.name= None

    outputPath = "data/raw"
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    todayDate = datetime.now().strftime("%Y-%m-%d")
    fileName = f"{outputPath}/stockPrices_{todayDate}.parquet"
    
    dados.to_parquet(fileName)

    print(f"[{datetime.now()}] Sucesso! Arquivo salvo em: {fileName}")
    print(f"Amostra dos dados:\n{dados.head()}")

if __name__ == "__main__":
    dataExtract()