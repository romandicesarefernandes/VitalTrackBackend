"""
Database initialization and utility module.
"""

from motor import motor_asyncio

from vitaltrack import config


class DatabaseManager:
    """
    Manages connections to a MongoDB database using asynchronous operations.

    Attributes:
        client: The MongoDB client instance used to connect to a MongoDB
            cluster.
        db: The MongoDB database instance selected after connecting
            to the cluster.
    """

    client: motor_asyncio.AsyncIOMotorClient = None
    db: motor_asyncio.AsyncIOMotorDatabase = None

    def connect_to_cluster(self, url: str, db_name: str | None = None):
        """
        Connect to a MongoDB cluster.

        Args:
            url: The connection URL for the MongoDB cluster.
            db_name: An database name to select after connecting. Optional.
        """
        self.client = motor_asyncio.AsyncIOMotorClient(
            url,
            minPoolSize=config.MIN_CONNECTIONS_COUNT,
            maxPoolSize=config.MAX_CONNECTIONS_COUNT,
            uuidRepresentation="standard",
        )
        if db_name:
            self.db = self.client[db_name]

    def close_cluster_connection(self):
        """
        Close the connection to the MongoDB cluster.

        This method closes the MongoDB client, releasing any associated
            resources.
        """
        self.client.close()

    def connect_to_database(self, db_name: str):
        """
        Select a database within the connected MongoDB cluster.

        Args:
            db_name: The name of the database to select.
        """
        self.db = self.client[db_name]


async def get_database_manager() -> DatabaseManager:
    """
     Retrieve the global instance of the `DatabaseManager`.

    Returns:
        Client connection to Mongo.
    """

    return global_db_manager


global_db_manager = DatabaseManager()
