import socket
import sys
import json
import time

while True:
    json_dict = {
        'SQL': {'task': 'param', 'dbs_name': 'param', 'tbl_name': 'param', 'vrbl1': 'param', 'vrbl2': 'param',
                'vrbl3': 'param'},
        'ROUTER': {'Authentication': {'user_name': 'chump', 'password': 'qwerty', 'user_id': '1', 'is_auth': None},
                   'Authorization': {'qual_features': 'param', 'access_level': 'param', 'app_approval': None},
                   'Apps': {'request_app': 'stripe', 'request_app_approval': None, 'dest_app': 'param'}}}
    #jsonResult = {"first": "You're", "second": "Awesome!"}
    json_dict = json.dumps(json_dict)

    try:
        sock = socket.socket()
    except socket.error as err:
        print('Socket error because of %s' % err)

    port = 1500
    address = "localhost"

    try:
        s = sock.connect((address, port))
        sock.settimeout(5)
        #time.sleep(1)
        sock.send(json_dict.encode('utf-8'))
        #sock.listen(1)
        while True:
            print(sock.recv(500))
            break
    except socket.timeout as e:
        print(e.args)
        pass

    #print(jsonResult, 'was sent!')

    #sock.close()
    time.sleep(1)
