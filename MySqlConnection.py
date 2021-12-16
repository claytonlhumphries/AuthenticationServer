import sys
import mysql.connector
import pymysql.cursors
import Logger
import rsa
from cryptography.fernet import Fernet



class DatabaseConnection:

    db_name = ""
    db = None
    db_cursor = None
    database_name_list = []
    database_table_list = []

    key = b'fHdqLrNrYHkExfUBmX0YZMgBe8HYXelp0eQ9Z04P-_U='
    fernet = Fernet(key)

    def encrypt(self, data):
        """
        Use to encrypt a string
        :param data: string to encrypt
        :type data: str
        :rtype: str
        """
        data = self.fernet.encrypt(data.encode())
        return data.decode()

    def decrypt(self, data):
        """
        Use to encrypt a string
        :param data: string to decrypt
        :type data: str
        :rtype: str
        """
        data = self.fernet.decrypt(data.encode())
        return data.decode()

    def start_database_connect(self, database_name, user_name, password):
        """
        Connects a database and returns database and cursor objects.
        :param database_name: database name
        :type database_name: str
        :param user_name: username
        :type user_name: str
        :param password: password
        :type password: str
        """
        try:
            self.db = pymysql.connect(host='localhost',
                                      user=user_name,
                                      password=password,
                                      database=database_name,
                                      cursorclass=pymysql.cursors.DictCursor)

            self.db_cursor = self.db.cursor()
            self.db_cursor.execute("SET SESSION optimizer_switch = 'index_merge_intersection=off'")

        except Exception as e:
            Logger.Log(e.args, 2, "Database Connection")

    def auth_decision(self, json_dict):

        user_name = json_dict["ROUTER"]["Authentication"]["user_name"]
        password = json_dict["ROUTER"]["Authentication"]["password"]
        user_id = json_dict["ROUTER"]["Authentication"]["user_id"]

        user_details = self.select_column_names_per_user_from_table("user_authentication", ["user_name", "password"],
                                                                    user_id)

        if user_name == self.decrypt(user_details[0]['user_name']) and password == self.decrypt(user_details[0]['password']):
            json_dict["ROUTER"]["Authentication"]["is_auth"] = True

        else:
            json_dict["ROUTER"]["Authentication"]["is_auth"] = False

        return json_dict

    def app_approval_decision(self, json_dict):
        if json_dict["ROUTER"]["Authentication"]["is_auth"] is True or \
                json_dict["ROUTER"]["Authentication"]["is_auth"] == "true":

            user_id = json_dict["ROUTER"]["Authentication"]["user_id"]
            user_details = self.select_column_names_per_user_from_table("user_authentication",
                                                                        ["qual_features"], user_id)
            requested_app = json_dict["ROUTER"]["Apps"]["request_app"]
            features = user_details[0]['qual_features']

            if requested_app in features:
                json_dict["ROUTER"]["Apps"]["request_app_approval"] = True

            else:
                json_dict["ROUTER"]["Apps"]["request_app_approval"] = False

        return json_dict
    def close_database_connection(self):
        """"
        Closes the database connection
        """
        self.db.close()

    def list_databases(self):
        """
        Get a list of databases
        """
        self.database_name_list = []
        self.db_cursor.execute("SHOW DATABASES")

        for x in self.db_cursor:
            y = str(x)  #Convert object to string to strip out misc characters
            self.database_name_list.append(y[2:-3])

    def create_database(self, database_name):
        """
        Creates the database
        :param database_name: table name
        :type database_name: str
        """
        try:
            self.db_cursor.execute("CREATE DATABASE " + database_name)

        except mysql.connector.errors.DatabaseError as e:
            print(e.args)

        self.list_databases()
        self.list_database_tables()

    def list_database_tables(self):
        """
        Get a list of databases
        """
        self.database_table_list = []
        self.db_cursor.execute("SHOW TABLES")

        for x in self.db_cursor:
            y = str(x)  #Convert object to string to strip out misc characters
            self.database_table_list.append(y[2:-3])

    def create_table(self, table_name, column_names):
        """
        Creates table
        :param table_name: table name
        :type table_name: str
        :param column_names: column name and data type (Keys: name, data_type)
        :type column_names: dict
        """
        sql = ""
        column_length = len(column_names)
        x = 1

        for key, value in column_names.items():
            if x == 1:
                sql = "CREATE TABLE " + table_name + " (id INT AUTO_INCREMENT PRIMARY KEY, " + \
                                       key + " " + value

            elif x != column_length:
                sql = sql + ", " + key + " " + value

            else:
                sql = sql + ", " + key + " " + value + ")"

            x += 1

        self.db_cursor.execute(sql)
        self.list_database_tables()

    def drop_database_table(self, table_name):
        """
        Drops table from database
        :param table_name: table name
        :type table_name: str
        """
        self.db_cursor.execute("DROP TABLE " + table_name)
        self.list_database_tables()

    def get_table_column_names(self, table_name):
        """
        Get names of column in database table
        :param table_name: table name
        :type table_name: str
        :rtype: list
        """
        column_name_list = []

        self.db_cursor.execute("desc " + table_name)
        for column in self.db_cursor.fetchall():
            column_name_list.append(column[0])

        return column_name_list

    def insert_data(self, table_name, columns, values):
        """
        Insert data into table
        :param table_name: table_name
        :type table_name: str
        :param columns: column_name
        :type columns: list
        :param values: column_value
        :type values: list[tuple]
        """
        column_length = len(columns)
        column_string = ""
        value_string = ""

        x = 1
        for item in columns:

            if x == 1:
                column_string = "INSERT INTO " + self.db_name + "." + table_name + " (" + item + ", "

            elif x != column_length:
                column_string = column_string + item + ", "

            elif x == column_length:
                column_string = column_string + item + ") "

            x += 1

        y = 1
        for item in range(column_length):

            if y == 1:
                value_string = "VALUES (%s, "

            elif y != column_length:
                value_string = value_string + "%s, "

            elif y == column_length:
                value_string = value_string + "%s)"

            y += 1

        sql = column_string + value_string
        self.db_cursor.executemany(sql, values)
        self.db.commit()

        print(self.db_cursor.rowcount, "row was inserted.")

    def update_record(self, table_name, user_id, column_name, column_value):
        """
        Update row based on user_id
        :param table_name: table name
        :type table_name: str
        :param user_id: user id
        :type user_id: int
        :param column_name: column name
        :type column_name: str
        :param column_value: column value
        :type column_value: str
        """
        if column_name == 'password' or column_name == "user_name":
            column_value = self.encrypt(column_name)

        sql = "UPDATE " + table_name + " SET " + column_name + " = " + column_value + " WHERE ID = " + str(user_id)

        self.db_cursor.execute(sql)
        self.db.commit()

        print(self.db_cursor.rowcount, "record(s) affected")

    def select_all_from_table(self, table_name, limit=None):
        """
        Update row based on user_id
        :param table_name: table name
        :type table_name: str
        :param limit: record limit amount
        :type limit: int
        :rtype: dict[dict]
        """
        return_dict = {}
        sql = "SELECT * FROM " + table_name

        if limit is not None:
            sql = sql + " LIMIT " + str(limit)

        self.db_cursor.execute(sql)

        results = self.db_cursor.fetchall()
        for x in range(len(results)):
            return_dict[x] = results[x]

        return return_dict

    def select_columns_from_table(self, table_name, column_name, limit=None):
        """
        Update row based on user_id
        :param table_name: table name
        :type table_name: str
        :param column_name: column name
        :type column_name: list
        :param limit: record limit amount
        :type limit: int
        :rtype: list[tuples]
        """
        sql = ""
        x = 1

        for name in column_name:

            if x == 1:
                sql = "Select " + name + ","

            elif x != len(column_name):
                sql = sql + " " + name + ","

            elif x == len(column_name):
                sql = sql + " " + name + " FROM " + table_name

                if limit is not None:
                    sql = sql + " LIMIT " + str(limit)

            x += 1

        self.db_cursor.execute(sql)
        return self.db_cursor.fetchall()

    def select_record_from_table(self, table_name, user_id):
        """
        Returns all data of user
        :param table_name: table name
        :type table_name: str
        :param user_id: user id
        :type user_id: int
        :rtype: list[tuples]
        """
        sql = "SELECT * FROM " + table_name + " WHERE ID = " + str(user_id)
        self.db_cursor.execute(sql)

        return self.db_cursor.fetchall()

    def select_column_names_per_user_from_table(self, table_name, column_name, user_id):
        """
        Returns all data of user
        :param table_name: table name
        :type table_name: str
        :param column_name: column name
        :type column_name: list
        :param user_id: user id
        :type user_id: int
        :rtype: list[tuples]
        """
        sql = ""
        x = 1

        for name in column_name:

            if len(column_name) == 1:
                sql = "Select " + name + " FROM " + table_name + " WHERE iduser = " + str(user_id)

            elif x == 1:
                sql = "Select " + name + ","

            elif x != len(column_name):
                sql = sql + " " + name + ","

            elif x == len(column_name):
                sql = sql + " " + name + " FROM " + table_name + " WHERE iduser = " + str(user_id)

            x += 1

        self.db_cursor.execute(sql)
        return self.db_cursor.fetchall()

    def create_sql_statement(self, statement, needs_commit=False):
        """
        Create your own sql statement
        :param needs_commit: True or False
        :type   needs_commit: bool
        :param statement: sql statement
        :rtype: ?
        """
        sql = statement
        self.db_cursor.execute(sql)

        if needs_commit:
            self.db.commit()

        else:
            return self.db_cursor.fetchall()

    def delete_record(self, table_name, user_id):
        """
        Delete user from table
        :param table_name: table name
        :type table_name: str
        :param user_id: user id
        :type user_id: int
        """
        sql = "DELETE FROM " + table_name + " WHERE ID = " + str(user_id)
        self.db_cursor.execute(sql)
        self.db.commit()

        print(self.db_cursor.rowcount, "record(s) deleted")
