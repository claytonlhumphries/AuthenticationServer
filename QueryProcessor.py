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

    def __init__(self):
        try:
            mc0.start_database_connect('city', 'tadmin', '67yuhjnm')
            mc1.start_database_connect('city', 'tadmin', '67yuhjnm')
            mc2.start_database_connect('city', 'tadmin', '67yuhjnm')
            mc3.start_database_connect('city', 'tadmin', '67yuhjnm')
            mc4.start_database_connect('city', 'tadmin', '67yuhjnm')
            mc5.start_database_connect('city', 'tadmin', '67yuhjnm')
            mc6.start_database_connect('city', 'tadmin', '67yuhjnm')
            mc7.start_database_connect('city', 'tadmin', '67yuhjnm')
            mc8.start_database_connect('city', 'tadmin', '67yuhjnm')
            mc9.start_database_connect('city', 'tadmin', '67yuhjnm')
            mc10.start_database_connect('city', 'tadmin', '67yuhjnm')

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
        while_loop_count = 1

        while return_value == "(0, '')" or return_value == {}:
            try:
                task_value = json_inbound['task']

                if task_value == 'rtv-all-usr':
                    return_value = cd.select_all_from_table(json_inbound['tabl'])

                elif task_value == 'rtv-all-dbs-tbl':
                    return_value = cd.list_databases()

                elif task_value == 'crt-dbs-tbl':
                    return_value = cd.create_table(json_inbound['tabl'], json_inbound['vrb1'])

                elif task_value == 'rtv-col-nms':
                    return_value = cd.get_table_column_names(json_inbound['tabl'])

                elif task_value == 'ins-dbs-tbl':
                    return_value = cd.insert_data(json_inbound['tabl'], json_inbound['vrb1'], json_inbound['vrb1'])

                elif task_value == 'upd-tbl-rcd':
                    return_value = cd.update_record(json_inbound['tabl'], json_inbound['vrb1'], json_inbound['vrb2'],
                                                    json_inbound['vrb3'])

                elif task_value == 'rtv-usr-col':
                    return_value = cd.select_column_names_per_user_from_table(json_inbound['tabl'], json_inbound['vrb1'],
                                                                              json_inbound['vrb2'])

                elif task_value == 'crt-sql-rcd':
                    return_value = cd.create_sql_statement(json_inbound['tabl'], json_inbound['vrb1'])

                elif task_value == 'dlt-tbl-rcd':
                    return_value = cd.delete_record(json_inbound['tabl'], json_inbound['vrb1'])

                elif while_loop_count == 5:
                    Logger.Log("Invalid Query", 2, "Query Processor")
                    return {'ERROR': 'Invalid Query'}

                if while_loop_count > 1:
                    Logger.Log(while_loop_count, 3, "Query Processor Loops")

                while_loop_count += 1

            except Exception as e:
                Logger.Log("Exception: " + str(e.args), 2, "Query Processor")

        return return_value

