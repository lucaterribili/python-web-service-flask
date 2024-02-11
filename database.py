import os
import pymysql
from dotenv import load_dotenv

load_dotenv()


class BasicORM:
    def __init__(self):
        # Initialize database connection using environment variables
        self.connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            db=os.getenv('DB_DATABASE'),
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None):
        # Execute a query and return the results
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def commit(self):
        # Commit the current transaction
        self.connection.commit()

    def close(self):
        # Close the database connection
        self.cursor.close()
        self.connection.close()
