# Navigate to the directory where we will create our virtual environment (in the console: cd to the folder)
# Create the venvironment
> python -m venv DatabasePSQL-env
# Activate it
> DatabasePSQL-env\Scripts\activate

> (deactivate) #To deactivate
# Install necessary libraries. This can be adapted according to our needs and functionalities that we develop for our tool
> pip install psycopg2
> pip install SQLAlchemy

> pip install pandas
> pip install geopandas
> pip install matplotlib
> pip install openpyxl
> pip install scikit-learn

# With everything correctly installed, we proceed to execute our tool
> python runquery.py

# Once we enter, we just have to execute the actions that interest us
# For example, Table names:
public."Lithic_CAI_Gallery_Lower_La_Garma"
#(Examples)
#public."Constructive_Elements_Lower_Gallery_La_Garma"
#public."Bone_Tool_CAI_Lower_Gallery_La_Garma"
#public."Displaced_Elements_Lower_Gallery_La_Garma"
#public."Estratigraphic_Units_CAI_Lower_Gallery_La_Garma"
#public."Fauna_CAI_Lower_Gallery_La_Garma"
#public."Malacofauna_CAI_Lower_La_Garma"
#public."Natural_Elements_CAI_Lower_Gallery_La_Garma"
#public."Samples_CAI_Lower_Gallery_La_Garma"



# Summary of the Scripts
#db_connection.py: Handles database connections.
connect_to_db(): Connects to the database using credentials from environment variables.
close_db_connection(connection): Closes the database connection.

#monitordb.py: Monitors various aspects of the database.
monitor_database(connection): Monitors metrics such as database size, active connections, shared buffers, cache hit ratio, and index statistics.

#backup.py: Performs database backups.
backup_database(host, database, user, password=None): Performs a backup of the specified database.

#exc.py: Exports table data to an Excel file.
fetch_all_data_from_table(connection, table_name): Retrieves all data from a table and saves it to an Excel file.
get_table_names(connection): Retrieves the names of all tables in the database (now moved to `utils.py`).

#query.py: Executes custom queries on the database.
execute_query(connection, query): Executes an SQL query and returns the result as a DataFrame.
query_database(connection): Allows users to create and execute custom SQL queries.

#Mapsdis.py: Generates a distribution map based on user-defined filters and columns.
generate_distribution_map(connection): Generates and optionally saves a distribution map.

#Kernelmap.py: Generates a kernel density map based on geometries and optionally includes a background layer.
generate_density_map(table_name, connection, column_name, background_table=None)*: Generates a kernel density map with an optional background layer.

#utils.py: Contains utility functions used across multiple modules.
get_table_names(connection): Retrieves the names of all tables in the database.
get_column_names(connection, table_name): Retrieves the names of all columns in a specific table.

#main.py: Contains the main menu and manages the logic for executing the application's various functionalities.
main_menu(connection): Displays a menu with options to perform various tasks on the database.



# Creating an Executable for Your Python Application
#To turn your application into an executable, you can use tools like **PyInstaller**, which package your Python application into a single executable file that can run on any system without requiring Python to be installed. 
#Here’s a step-by-step guide to achieve this:

## Step 1: Install PyInstaller
#First, you need to install PyInstaller. You can do this using `pip`:
pip install pyinstaller

##Step 2: Create the Executable
Navigate to your project directory and run the following command to create an executable for your main application file (main.py):
pyinstaller --onefile --name my_application main.py
                                                                                        
#Step 3: Include Additional Files
If your application requires additional files (such as images, configuration files, etc.), you can specify these files using the --add-data argument. The syntax depends on your operating system.

On Windows:

pyinstaller --onefile --name my_application --add-data "path\to\file;destination\path" main.py

#( Example) pyinstaller --onefile --name my_application --add-data "garma.png;." --add-data "config.json;." main.py

                                                                                        
