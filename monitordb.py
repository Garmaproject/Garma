import logging
from sqlalchemy import text

# Configurar el logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_database(connection):
    """
    Monitors the database by checking various metrics and prints the results.
    
    Args:
        connection: The database connection object.
    """
    try:
        # Check the disk space used by the database
        result = connection.execute(text("SELECT pg_size_pretty(pg_database_size(current_database()))"))
        size = result.scalar()
        print(f"Database size: {size}")

        # Check the number of active connections
        result = connection.execute(text("SELECT count(*) FROM pg_stat_activity WHERE state = 'active'"))
        connections = result.scalar()
        print(f"Active connections: {connections}")

        # Check shared buffer usage
        result = connection.execute(text("SHOW shared_buffers"))
        shared_buffers = result.scalar()
        print(f"Shared buffers: {shared_buffers}")

        # Check cache hit ratio
        result = connection.execute(text("SELECT sum(heap_blks_read) as heap_read, sum(heap_blks_hit) as heap_hit, (sum(heap_blks_hit) - sum(heap_blks_read)) / sum(heap_blks_hit) as ratio FROM pg_statio_user_tables"))
        result = result.fetchone()
        cache_hit_ratio = result[2]  # Accedemos al tercer valor de la tupla
        print(f"Cache hit ratio: {cache_hit_ratio:.2f}")

        # Check indexes with high read/write ratios
        result = connection.execute(text("SELECT relname, indexrelname, idx_scan, idx_tup_read, idx_tup_fetch FROM pg_stat_user_indexes ORDER BY idx_scan DESC LIMIT 5"))
        indexes = result.fetchall()
        for index in indexes:
            print(f"Index {index[1]} on table {index[0]}: Scan count = {index[2]}, Tuple read = {index[3]}, Tuple fetch = {index[4]}")

    except Exception as e:
        logging.error(f"Unexpected error while monitoring the database: {e}")

# Función de prueba comentada para evitar ejecuciones no deseadas.
# connection = connect_to_db()
# if connection:
#     monitor_database(connection)
#     close_db_connection(connection)
