import json
import requests

from functions import url, authtock, headers, templateget, hostget

host_tmplt = newhost_spec[hostname]["zabbix_host_tmplt"]

def drule(param,param1):
    paramslst = dict(output="extend", selectDChecks="extend")
    paramsfilter = dict()
    paramsfilter[param] = param1
    paramslst["filter"] = paramsfilter
    hostget = dict(jsonrpc="2.0", method="discoveryrule.get", params=paramslst,
                   auth=authtock, id=1)
    return requests.post(url, data=json.dumps(hostget), headers=headers)

host_id = hostget("host", hostname).json()["result"][0]["hostid"]

drulefull = drule("x","y").json()["result"][0].keys()

for i in drulefull:
    print(i)

# count = len(drulefull)
# zcount = 0
#
# while zcount < count:
#     host_id = drulefull[zcount]["hostid"]
#     hostname = hostget("hostid",host_id).json()["result"]
#     if not hostname:
#         print(host_id)
#     else:
#         print(hostname[0]["host"])
#     zcount += 1

