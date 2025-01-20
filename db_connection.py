from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_to_db():
    """
    Attempts to connect to the database using the credentials from environment variables.
    Returns the connection if successful; otherwise, returns None.
    """
    logging.info("Trying to connect to the database...")
    try:
        DATABASE_URL = f'postgresql://{os.getenv("DB_USER", "postgres")}:{os.getenv("DB_PASSWORD", "csfecscom")}@{os.getenv("DB_HOST", "localhost")}/{os.getenv("DB_NAME", "postgres")}'
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()
        logging.info("Connected to the database")
        return engine.connect()
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
    return None

def close_db_connection(connection):
    """
    Closes the database connection if it exists.
    """
    if connection:
        connection.close()
        logging.info("Connection closed")
