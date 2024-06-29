# Navigate to the directory where we will create our virtual environment
# Create the environment
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
# Table names:
public."Lithic_CAI_Gallery_Lower_La_Garma"

#public."Constructive_Elements_Lower_Gallery_La_Garma"
#public."Bone Tool CAI Lower Gallery La Garma"
#public."Displaced Elements Lower Gallery La Garma"
#public."Estratigraphic Units CAI Lower Gallery La Garma"
#public."Fauna CAI Lower Gallery La Garma"
#public."Malacofauna CAI Lower La Garma"
#public."Natural Elements CAI Lower Gallery La Garma"
#public."Samples CAI Lower Gallery La Garma"



'''Resumen de los Scripts
db_connection.py: Maneja la conexión a la base de datos.

connect_to_db(): Conecta a la base de datos utilizando credenciales de las variables de entorno.
close_db_connection(connection): Cierra la conexión a la base de datos.
monitordb.py: Monitorea varios aspectos de la base de datos.

monitor_database(connection): Monitorea métricas como tamaño de la base de datos, conexiones activas, buffers compartidos, ratio de aciertos en caché y estadísticas de índices.
backup.py: Realiza backups de la base de datos.

backup_database(host, database, user, password=None): Realiza un backup de la base de datos especificada.
exc.py: Exporta datos de una tabla a un archivo Excel.

fetch_all_data_from_table(connection, table_name): Obtiene todos los datos de una tabla y los guarda en un archivo Excel.
get_table_names(connection): Obtiene los nombres de todas las tablas en la base de datos (ahora movido a utils.py).
query.py: Ejecuta consultas personalizadas en la base de datos.

execute_query(connection, query): Ejecuta una consulta SQL y retorna el resultado como un DataFrame.
query_database(connection): Permite al usuario crear y ejecutar consultas SQL personalizadas.
Mapsdis.py: Genera un mapa de distribución basado en filtros y columnas definidos por el usuario.

generate_distribution_map(connection): Genera y opcionalmente guarda un mapa de distribución.
Kernelmap.py: Genera un mapa de densidad de kernel basado en geometrías y opcionalmente incluye una capa de fondo.

generate_density_map(table_name, connection, column_name, background_table=None): Genera un mapa de densidad de kernel con una capa de fondo opcional.
utils.py: Contiene funciones auxiliares que se usan en varios módulos.

get_table_names(connection): Obtiene los nombres de todas las tablas en la base de datos.
get_column_names(connection, table_name): Obtiene los nombres de todas las columnas en una tabla específica.
main.py: Contiene el menú principal y maneja la lógica para ejecutar las diferentes funcionalidades de la aplicación.

main_menu(connection): Muestra un menú con opciones para realizar diversas tareas en la base de datos.'''







'''Para convertir tu aplicación en un ejecutable, puedes utilizar herramientas como PyInstaller, que empaquetan tu aplicación Python en un solo archivo ejecutable que puede ejecutarse en cualquier sistema que no tenga Python instalado. Aquí tienes una guía paso a paso para lograrlo:

Paso 1: Instalar PyInstaller
Primero, necesitas instalar PyInstaller. Puedes hacerlo usando pip:


pip install pyinstaller



Paso 2: Crear el Ejecutable
Navega al directorio de tu proyecto y ejecuta el siguiente comando para crear un ejecutable de tu aplicación principal (main.py):

bash
Copiar código
pyinstaller --onefile --name my_application main.py



Paso 3: Incluir Archivos Adicionales
Si tu aplicación necesita incluir archivos adicionales (como imágenes, archivos de configuración, etc.), puedes especificar estos archivos usando el argumento --add-data. La sintaxis depende de tu sistema operativo.

En Windows:

pyinstaller --onefile --name my_application --add-data "path\to\file;destination\path" main.py


pyinstaller --onefile --name my_application --add-data "garma.png;." --add-data "config.json;." main.py'''
