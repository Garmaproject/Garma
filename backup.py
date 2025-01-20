import os
import subprocess
from datetime import datetime
import getpass
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def backup_database(host, database, user, password=None):
    """
    Performs a backup of the specified PostgreSQL database.
    
    Args:
        host (str): The database host.
        database (str): The name of the database to back up.
        user (str): The database user.
        password (str, optional): The password for the database user. If not provided, it will be securely requested.
    
    Raises:
        Exception: For any errors that occur during the backup process.
    """
    try:
        if password is None:
            password = getpass.getpass(prompt=f"Enter password for user {user}: ")
        
        # Create a timestamped filename for the backup
        filename = f"{database}_{datetime.now().strftime('%Y%m%d%H%M%S')}.backup"
        # Define the full path to save the backup file
        backup_folder = r"C:\Programming\artmet\DatabaseBackups"
        filepath = os.path.join(backup_folder, filename)
        
        # Ensure the directory exists
        os.makedirs(backup_folder, exist_ok=True)
        
        # Command to perform the backup in backup format
        command = [
            r"C:\Program Files\PostgreSQL\12\bin\pg_dump",
            "-h", host,
            "-U", user,
            "-d", database,
            "-F", "c",
            "-f", filepath
        ]
        
        # Set the environment variable for the password
        os.environ["PGPASSWORD"] = password
        
        # Execute the command
        subprocess.run(command, check=True)
        logging.info(f"Backup successfully completed at {filepath}")
    
    except subprocess.CalledProcessError as e:
        logging.error(f"Error performing backup: {e}")
    
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    
    finally:
        # Remove the environment variable for security
        if "PGPASSWORD" in os.environ:
            del os.environ["PGPASSWORD"]

# backup_database("localhost", "my_database", "my_user")
