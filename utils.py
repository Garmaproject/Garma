import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname=s - %(message)s')

def get_table_names(connection):
    try:
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        df = pd.read_sql(query, connection)
        table_names = df['table_name'].tolist()
        return table_names
    except Exception as e:
        logging.error(f"Error fetching table names: {e}")
        return []

def get_column_names(connection, table_name):
    try:
        query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
        df = pd.read_sql(query, connection)
        column_names = df['column_name'].tolist()
        return column_names
    except Exception as e:
        logging.error(f"Error fetching column names: {e}")
        return []
