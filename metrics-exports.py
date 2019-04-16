import json
import os
from pyzabbix import ZabbixAPI
import re
import requests
import sys
import time


if len(sys.argv) < 4 or len(sys.argv) > 4:
    print "Usage: <hostname> <item key> <metric type(int)>"
    exit()



server = 'http://<zabbix-server>/api_jsonrpc.php'
user = '<username>'
password = '<password>'

z = ZabbixAPI(server, user=user, password=password)



host=sys.argv[1]

item_apiresult = z.item.get(
    host=host,
    output = [
            'itemid',
            'name',
            'lastvalue',
            'lastclock',
            'key_'
    ]

)


json_raw = json.dumps(item_apiresult)
jsonn = json.loads(json_raw)



for elem in range (0, len(jsonn)):

    name = jsonn[elem]['name']
    key = jsonn[elem]['key_']
    itemid = jsonn[elem]['itemid']

    if key == sys.argv[2]:
        apiresult = z.history.get(
            history=sys.argv[3],
            itemids=itemid,
            time_from='<epoch start time(int)>',
            time_till='<epoch end time(int)>',
            output='extend'
        )

        apiresult.insert(0,{'hostname': host})
        apiresult.insert(1,{'metric_key': sys.argv[2]})



        print json.dumps(apiresult)  

    else:
        pass



