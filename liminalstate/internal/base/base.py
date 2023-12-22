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

    def get_single(self, key: str, value: str, database: str, table_name: str):
        """
        Get a single entry from the database.

        Args:
            key (str): The database column.
            value (str): The value to search for.
            table_name (str): The table name.

        Returns:
            RowType: Database row.
        """

        connection = return_mysql_connection(
            self.parser["DB"]["db_host"],
            self.parser["DB"]["db_username"],
            self.parser["DB"]["db_password"],
            database,
        )

        if table_name != "item_template" and table_name != "creature_template":
            raise Exception("Invalid table name. Please use either player or world.")

        try:
            cursor = connection.cursor(dictionary=True)
            query = f"SELECT * FROM {table_name} WHERE {key} = %s LIMIT 1"
            cursor.execute(query, (value,))
            result = cursor.fetchone()
            return result
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

    def update_single_field(
        self,
        search_key: str,
        search_value: str,
        update_key: str,
        update_value: str,
        database: str,
        table_name: str,
    ):
        """
        Update a single entry in the database.

        Args:
            search_key (str): The column used to identify the row to update.
            search_value (str): The value used to search for the row.
            update_key (str): The column to update.
            update_value (str): The new value to set.
            database (str): The database name.
            table_name (str): The table name.

        Returns:
            bool: True if the row was updated, False otherwise.
        """

        connection = return_mysql_connection(
            self.parser["DB"]["db_host"],
            self.parser["DB"]["db_username"],
            self.parser["DB"]["db_password"],
            database,
        )

        if table_name not in ["item_template", "creature_template"]:
            raise Exception("Invalid table name. Please use either player or world.")

        try:
            cursor = connection.cursor()
            query = f"UPDATE {table_name} SET {update_key} = %s WHERE {search_key} = %s"
            cursor.execute(query, (update_value, search_value))
            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error pushing change to database: {e}")
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()
