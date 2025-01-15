import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import logging
from utils import get_table_names, get_column_names
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname=s - %(message=s')

def generate_distribution_map(connection):
    """
    Generates a distribution map based on user-defined filters and columns.
    
    Args:
        connection: Database connection object.
    """
    try:
        table_names = get_table_names(connection)
        if not table_names:
            print("No tables found.")
            return
        
        print("Available tables:")
        for table in table_names:
            print(f"- {table}")

        table_name = input("Enter the table name for the map: ").strip()
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

        column_name = input("Enter the column name for distribution: ").strip()
        if column_name not in column_names:
            print("Invalid column name.")
            return

        # Get additional filters
        filters = {}
        while True:
            filter_column = input("Enter a column name to filter by (or press Enter to finish): ").strip()
            if not filter_column:
                break
            if filter_column not in column_names:
                print("Invalid column name.")
                continue
            filter_value = input(f"Enter the value to filter by for column '{filter_column}': ").strip()
            if filter_column not in filters:
                filters[filter_column] = []
            filters[filter_column].append(filter_value)

        # Build the SQL query with the filters
        filter_query_parts = []
        for filter_column, values in filters.items():
            column_conditions = [f'"{filter_column}" = \'{value}\'' for value in values]
            filter_query_parts.append(f"({' OR '.join(column_conditions)})")

        filter_query = " AND ".join(filter_query_parts)
        query = f'SELECT * FROM "{table_name}" WHERE "{column_name}" IS NOT NULL'
        if filter_query:
            query += f" AND {filter_query}"

        gdf = gpd.read_postgis(query, connection, geom_col='geom')

        if not gdf.empty:
            ax = gdf.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
            plt.title('Distribution Map')
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')

            save_option = input("Do you want to save the map as a PNG file? (y/n): ").strip().lower()
            if save_option == 'y':
                figures_dir = os.path.join(os.getcwd(), 'figures')
                if not os.path.exists(figures_dir):
                    os.makedirs(figures_dir, exist_ok=True)
                output_file = input("Enter the output file name (with .png extension): ").strip()
                if output_file.endswith('.png'):
                    output_path = os.path.join(figures_dir, output_file)
                    plt.savefig(output_path)
                    print(f"Map saved to {output_path}")
                else:
                    print("Output file must have a .png extension.")
            plt.show()
        else:
            print("No results found or error executing the query.")
    except Exception as e:
        logging.error(f"Error generating distribution map: {e}")


# connection = connect_to_db()
# if connection:
#     generate_distribution_map(connection)
#     close_db_connection(connection)
