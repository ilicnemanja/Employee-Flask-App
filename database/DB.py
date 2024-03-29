import mysql.connector as con
from mysql.connector import errorcode


class DB:

    DATABASE = None

    @staticmethod
    def connect() -> con.MySQLConnection:
        if DB.DATABASE is None:
            try:
                DB.DATABASE = con.connect(
                    host="127.0.0.1",
                    port=3306,
                    user="root",
                    password="1234",
                    database="employees",
                )
            except con.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your username or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print(err)

        return DB.DATABASE

    @staticmethod
    def create_table(query_string: str):
        db = DB.connect()
        c = db.cursor(dictionary=True)
        c.execute(query_string)
        db.commit()

    @staticmethod
    def insert_into_query(query_string: str, parameters: tuple):
        db = DB.connect()
        c = db.cursor(dictionary=True)
        c.execute(query_string, parameters)
        db.commit()

    @staticmethod
    def delete_query(table_name: str, condition: str, data: any):
        db = DB.connect()
        c = db.cursor(dictionary=True)
        c.execute(f"DELETE FROM {table_name} WHERE {condition} = %s", (data,))
        db.commit()

    @staticmethod
    def update_query(query_string: str, data: any):
        db = DB.connect()
        c = db.cursor(dictionary=True)
        c.execute(query_string, data)
        db.commit()

    @staticmethod
    def select_query(query_string: str, parameters: tuple = None):
        db = DB.connect()
        c = db.cursor(dictionary=True)

        c.execute(query_string, parameters)
        results = c.fetchall()
        return results
