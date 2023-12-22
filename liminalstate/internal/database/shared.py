import mysql.connector

import logging 

logger = logging.getLogger(__name__)
import mysql.connector
from mysql.connector import Error

def return_mysql_connection(host: str, user: str, password: str, database: str) -> mysql.connector.connection.MySQLConnection:
    """
    Return a MySQL connection object.

    Args:
        host (str): The host IP address or domain name.
        user (str): The username for the database.
        password (str): The password for the database.
        database (str): The database name.

    Returns:
        MySQLConnection: The MySQL connection object.
    """

    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return connection
    except Error as e:
        logger.error(f"Error while connecting to MySQL: {e}")
        return None

