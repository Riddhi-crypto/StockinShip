import mysql.connector


class DatabaseManager:

    def __init__(self):

        self.connection = None
        self.cursor = None

    def connect(self):

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root@1234",
            database="stockship_db"
        )

        self.cursor = self.connection.cursor()

    def close_connection(self):

        if self.connection:
            self.cursor.close()
            self.connection.close()