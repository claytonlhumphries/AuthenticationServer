import json
import MySqlConnection
import Logger
mc0 = MySqlConnection.DatabaseConnection()
mc1 = MySqlConnection.DatabaseConnection()
mc2 = MySqlConnection.DatabaseConnection()
mc3 = MySqlConnection.DatabaseConnection()
mc4 = MySqlConnection.DatabaseConnection()
mc5 = MySqlConnection.DatabaseConnection()
mc6 = MySqlConnection.DatabaseConnection()
mc7 = MySqlConnection.DatabaseConnection()
mc8 = MySqlConnection.DatabaseConnection()
mc9 = MySqlConnection.DatabaseConnection()
mc10 = MySqlConnection.DatabaseConnection()


class ReturnQuery:

    rcv_json_object = {}
    mc00 = 0
    mc01 = 1
    mc02 = 1
    mc03 = 1
    mc04 = 1
    mc05 = 1
    mc06 = 1
    mc07 = 1
    mc08 = 1
    mc09 = 1
    mc010 = 1

    def __init__(self, database_name, user_name, password):
        try:
            mc0.start_database_connect(database_name, user_name, password)
            mc1.start_database_connect(database_name, user_name, password)
            mc2.start_database_connect(database_name, user_name, password)
            mc3.start_database_connect(database_name, user_name, password)
            mc4.start_database_connect(database_name, user_name, password)
            mc5.start_database_connect(database_name, user_name, password)
            mc6.start_database_connect(database_name, user_name, password)
            mc7.start_database_connect(database_name, user_name, password)
            mc8.start_database_connect(database_name, user_name, password)
            mc9.start_database_connect(database_name, user_name, password)
            mc10.start_database_connect(database_name, user_name, password)

        except Exception as e:
            Logger.Log(e.args, 2, "Query Processor Connections")

    def reconnect_to_server(self):

        self.socket_connection_decision().db.ping(reconnect=True)

    def socket_connection_decision(self):

        lowest_connections = min([self.mc00, self.mc01, self.mc02, self.mc03, self.mc04, self.mc05, self.mc06,
                                  self.mc07, self.mc08, self.mc09, self.mc010])

        if lowest_connections == self.mc00:
            #print("Connection: 0")
            self.mc00 += 1
            return mc0

        elif lowest_connections == self.mc01:
            #print("Connection: 1")
            self.mc01 += 1
            return mc1

        elif lowest_connections == self.mc02:
            #print("Connection: 2")
            self.mc02 += 1
            return mc2

        elif lowest_connections == self.mc03:
            #print("Connection: 3")
            self.mc03 += 1
            return mc3

        elif lowest_connections == self.mc04:
            #print("Connection: 4")
            self.mc04 += 1
            return mc4

        elif lowest_connections == self.mc05:
            #print("Connection: 5")
            self.mc05 += 1
            return mc5

        elif lowest_connections == self.mc06:
            #print("Connection: 6")
            self.mc06 += 1
            return mc6

        elif lowest_connections == self.mc07:
            #print("Connection: 7")
            self.mc07 += 1
            return mc7

        elif lowest_connections == self.mc08:
            #print("Connection: 8")
            self.mc08 += 1
            return mc8

        elif lowest_connections == self.mc09:
            #print("Connection: 9")
            self.mc09 += 1
            return mc9

        else:
            #print("Connection: 10")
            self.mc010 += 1
            return mc10

    def sql_decision_tree(self, json_file):

        cd = self.socket_connection_decision()
        json_inbound = json.loads(json_file)
        return_value = {}
        while_loop_count = 0

        while return_value == "(0, '')" or return_value == {}:
            try:
                while_loop_count += 1
                is_auth = json_inbound["ROUTER"]["Authentication"]["is_auth"]

                if while_loop_count > 1:
                    Logger.Log(while_loop_count, 3, "Query Processor Loops")

                if while_loop_count == 5:
                    break

                if is_auth is None or is_auth == "null":
                    return_value = cd.auth_decision(json_inbound)

                elif not is_auth or is_auth == "False" or is_auth or is_auth == "True":
                    return_value = json_inbound

            except Exception as e:
                Logger.Log("Exception: " + str(e.args), 2, "Auth App: Query Processor")

                if 1054 in e.args:
                    Logger.Log("Exception: " + str(e.args), 2, "Auth App: Query Processor")
                    return {'error': 'Unknown column password in field list'}

        return return_value

