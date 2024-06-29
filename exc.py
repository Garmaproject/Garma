import os
import pandas as pd
import logging
import re
from utils import get_table_names  # Importar desde utils.py

logging.basicConfig(level=logging.INFO, format='%(asctime=s - %(levelname=s - %(message=s')

# Resto del código sin cambios



def fetch_all_data_from_table(connection, table_name):
    """
    Fetches all data from a specified table and writes it to an Excel file.
    
    Args:
        connection: The database connection object.
        table_name: The name of the table to fetch data from.
    
    Raises:
        ValueError: If the table name is not valid.
        Exception: For any other errors that occur during the process.
    """
    try:
        # Sanitize the table name to avoid SQL injection
        table_name_sanitized = re.sub(r'[^A-Za-z0-9_ ]', '', table_name)

        # Crear un DataFrame de pandas con los datos de la consulta SQL
        df = pd.read_sql(f'SELECT * FROM "{table_name_sanitized}"', connection)
        
        # Crear la carpeta 'Tables' si no existe
        if not os.path.exists('Tables'):
            os.makedirs('Tables')
        
        # Definir el nombre del archivo Excel
        # Modificar el nombre de la tabla para crear un nombre de archivo válido
        safe_table_name = table_name.replace('.', '_').replace('"', '').replace(' ', '_')
        excel_path = os.path.join('Tables', f"{safe_table_name}.xlsx")
        
        # Escribir el DataFrame en un archivo Excel
        df.to_excel(excel_path, index=False, engine='openpyxl')
        
        logging.info(f"Data processed. File '{excel_path}' successfully created.")
    except ValueError as ve:
        logging.error(f"Error: {ve}")
    except pd.io.sql.DatabaseError as de:
        logging.error(f"Database error: {de}")
    except Exception as e:
        logging.error(f"Error fetching data from table {table_name} and writing to Excel: {e}")


# Ejemplo de uso:
# connection = connect_to_db()
# if connection:
#     fetch_all_data_from_table(connection, 'nombre_de_tu_tabla')
#     close_db_connection(connection)
