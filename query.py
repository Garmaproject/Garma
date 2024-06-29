import pandas as pd
import logging
from utils import get_table_names, get_column_names  # Importar desde utils.py

logging.basicConfig(level=logging.INFO, format='%(asctime=s - %(levelname=s - %(message=s')

# Resto del código sin cambios



def execute_query(connection, query):
    """
    Executes the given SQL query on the database and returns the result as a DataFrame.
    
    Args:
        connection: The database connection object.
        query (str): The SQL query to execute.
    
    Returns:
        pd.DataFrame: The query results.
    """
    try:
        df = pd.read_sql(query, connection)
        return df
    except Exception as e:
        logging.error(f"Error executing query: {e}")
        return None

def query_database(connection):
    """
    Allows the user to create and execute custom SQL queries based on available tables and columns.
    
    Args:
        connection: The database connection object.
    """
    table_names = get_table_names(connection)
    if not table_names:
        print("No tables found.")
        return
    
    print("Available tables:")
    for table in table_names:
        print(f"- {table}")

    table_name = input("Enter the table name for the query: ").strip()
    if table_name not in table_names:
        print("Invalid table name.")
        return

    column_names = get_column_names(connection, table_name)
    if not column_names:
        print("No columns found.")
        return

    print("Available columns:")
    for column in column_names:
        print(f"- {column}")

    filters = {}
    while True:
        column_name = input("Enter a column name to filter by (or press Enter to finish): ").strip()
        if not column_name:
            break
        if column_name not in column_names:
            print("Invalid column name.")
            continue
        value = input(f"Enter the value to filter by for column '{column_name}': ").strip()
        if column_name not in filters:
            filters[column_name] = []
        filters[column_name].append(value)

    filter_query_parts = []
    for column_name, values in filters.items():
        column_conditions = [f'"{column_name}" = \'{value}\'' for value in values]
        filter_query_parts.append(f"({' OR '.join(column_conditions)})")

    filter_query = " AND ".join(filter_query_parts)
    query = f'SELECT * FROM "{table_name}"'
    if filter_query:
        query += f" WHERE {filter_query}"
    
    print(f"Executing query: {query}")
    df = execute_query(connection, query)
    if df is not None and not df.empty:
        print(df)
        save_as_excel = input("Do you want to save the results to an Excel file? (y/n): ").strip().lower()
        if save_as_excel == 'y':
            output_file = input("Enter the output file name (with .xlsx extension): ").strip()
            if output_file.endswith('.xlsx'):
                df.to_excel(output_file, index=False)
                print(f"Results saved to {output_file}")
            else:
                print("Output file must have a .xlsx extension.")
    else:
        print("No results found or error executing the query.")
