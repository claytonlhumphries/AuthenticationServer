import json

import MySqlConnection
import QueryProcessor
import AuthenticationAppServer
dc = MySqlConnection.DatabaseConnection()
qp = QueryProcessor.ReturnQuery("authenticationdb", "tadmin", "67yuhjnm")
cs = AuthenticationAppServer.ComServer()

json_dict = {
    'SQL': {'task': 'param', 'dbs_name': 'param', 'tbl_name': 'param', 'vrbl1': 'param', 'vrbl2': 'param',
            'vrbl3': 'param'},
    'ROUTER': {'Authentication': {'user_name': 'chump', 'password': 'qwerty', 'user_id': '1', 'is_auth': None},
               'Authorization': {'qual_features': 'param', 'access_level': 'param', 'app_approval': 'param'},
               'Apps': {'request_app': 'param', 'request_app_approval': 'param', 'dest_app': 'param'}}}

#qp.sql_decision_tree(json.dumps(json_dict))
#dc.start_database_connect("Authentication Server", "tadmin", "67yuhjnm")
cs.server_init("localhost", 1500)
