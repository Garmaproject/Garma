import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from db_connection import connect_to_db, close_db_connection
from exc import fetch_all_data_from_table
from backup import backup_database
from monitordb import monitor_database
from Mapsdis import generate_distribution_map
from query import execute_query, query_database
from utils import get_table_names, get_column_names
from Kernelmap import generate_density_map

def main_menu(connection):
    while True:
        print("\nOptions:")
        print("1 - Export data to excel file")
        print("2 - Perform Backup")
        print("3 - Monitor Database")
        print("4 - Query the database")
        print("5 - Generate Density Map")
        print("6 - Generate Distribution Map")
        print("7 - Close the database and exit")
        
        action = input("Choose an option (1/2/3/4/5/6/7): ").strip()

        if action == "1":
            table_names = get_table_names(connection)
            if table_names:
                print("Available tables:")
                for table in table_names:
                    print(f"- {table}")
                table_name = input("Enter the table name to fetch data: ").strip()
                if table_name in table_names:
                    fetch_all_data_from_table(connection, table_name)
                else:
                    print("Invalid table name.")
            else:
                print("No tables found.")
        elif action == "2":
            host = input("Enter the database host: ").strip()
            database = input("Enter the database name: ").strip()
            user = input("Enter the database user: ").strip()
            password = input("Enter the password: ").strip()
            if all([host, database, user, password]):
                backup_database(host, database, user, password)
            else:
                print("All fields are required for backup.")
        elif action == "3":
            monitor_database(connection)
        elif action == "4":
            query_database(connection)
        elif action == "5":
            table_names = get_table_names(connection)
            if table_names:
                print("Available tables:")
                for table in table_names:
                    print(f"- {table}")
                table_name = input("Enter the polygon table name: ").strip()
                if table_name in table_names:
                    column_names = get_column_names(connection, table_name)
                    if column_names:
                        print("Available columns:")
                        for column in column_names:
                            print(f"- {column}")
                        column_name = input("Enter the column name for density: ").strip()
                        if column_name in column_names:
                            add_background = input("Do you want to add a background layer? (y/n): ").strip().lower()
                            if add_background == 'y':
                                background_table = input("Enter the background polygon table name: ").strip()
                                generate_density_map(table_name, connection, column_name, background_table)
                            elif add_background == 'n':
                                generate_density_map(table_name, connection, column_name)
                            else:
                                print("Unrecognized option, please try again.")
                        else:
                            print("Invalid column name.")
                    else:
                        print("No columns found.")
                else:
                    print("Invalid table name.")
            else:
                print("No tables found.")
        elif action == "6":
            generate_distribution_map(connection)
        elif action == "7":
            close_db_connection(connection)
            print("Database connection closed. Exiting the application.")
            break
        else:
            print("Unrecognized option, please try again.")

if __name__ == "__main__":
    connection = connect_to_db()
    if connection:
        main_menu(connection)
    else:
        print("Failed to connect to the database.")
