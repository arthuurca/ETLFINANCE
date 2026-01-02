import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

db_User = 'admin'
db_pass = 'admin'
db_host = 'localhost'
db_port = '5432'
db_name = 'finance_dw'

database_Url = f"postgresql+psycopg2://{db_User}:{db_pass}@{db_host}:{db_port}/{db_name}"

def loadData():
    engine = create_engine(database_Url)

    query = "SELECT * FROM stock_prices"
    df = pd.read_sql(query, engine)
    return df

st.set_page_config(page_title="Finance Dashboard", layout = "wide")

st.title("Finance Dashboard")
st.markdown("This dashboard reads data from our **PostgreSQL Data Warehouse**.")

try:
    with st.spinner("Loading data from database..."):
        df = loadData()
    
    df['date'] = pd.to_datetime(df['date'])

    st.sidebar.header("Filters")
    listaTickers = df['ticker'].unique()
    selectedTicker = st.sidebar.selectbox("Select a Ticker:", listaTickers)

    dfFiltered = df[df['ticker'] == selectedTicker]

    dfFiltered = dfFiltered.sort_values(by='date')

    col1, col2, col3 = st.columns(3)
    latestPrice = dfFiltered['close'].iloc[-1]
    minPrice = dfFiltered['close'].min()
    maxPrice = dfFiltered['close'].max()

    col1.metric("Latest close price", f"R$ {latestPrice:.2f}")
    col2.metric("Lowest price(1Y)", f"R$ {minPrice:.2f}")
    col3.metric("Highest price(1Y)", f"R${maxPrice:.2f}")

    st.subheader(f"Price history: {selectedTicker}")
    st.line_chart(dfFiltered.set_index('date')['close'])

    with st.expander("See raw data"):
        st.dataframe(dfFiltered.sort_values(by='date', ascending = False))

except Exception as e:
    st.error(f"Error conecting to database: {e}")
    st.write("Make sure Docker is running and the ETL pipeline has been executed!")