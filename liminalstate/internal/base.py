from liminalstate.internal.database.shared import return_mysql_connection

import configparser, logging

logger = logging.getLogger(__name__)

class LiminalBase:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.parser = configparser.ConfigParser()
        self.parser.read(config_path)

        try: 
            self.world = self.parser["DB"]["world_database"]
            self.player = self.parser["DB"]["player_database"]
        except Exception as e:
            logger.error(f"Error: {e}")

        self.connection = return_mysql_connection(
            self.parser["mysql"]["host"],
            self.parser["mysql"]["user"],
            self.parser["mysql"]["password"],
            self.parser["mysql"]["database"],
        )

        if self.connection is None:
            raise Exception("Could not connect to database. Check server or configuration settings.")

    def get_single(self, key: str, value: str, table_name: str):
        """
        Get a single entry from the database.

        Args:
            key (str): The database column.
            value (str): The value to search for.
            table_name (str): The table name.

        Returns:
            RowType: Database row. 
        """

        if table_name != "player" or table_name != "world":
            raise Exception("Invalid table name. Please use either player or world.")

        try:
            cursor = self.connection.cursor(dictionary=True)
            query = f"SELECT * FROM {table_name} WHERE {key} = %s LIMIT 1"
            cursor.execute(query, (value,))
            result = cursor.fetchone()
            return result
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            cursor.close()

    
