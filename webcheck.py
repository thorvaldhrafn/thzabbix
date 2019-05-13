import json
import requests

from functions import url, authtock, headers, templateget, hostget, hgroupget, anshlist, ansvarinfo


def hostint(param, param1):
    paramslst = dict(output="extend")
    paramsfilter = dict()
    paramsfilter[param] = param1
    paramslst["filter"] = paramsfilter
    hostget = dict(jsonrpc="2.0", method="hostinterface.get", params=paramslst,
                   auth=authtock, id=1)
    return requests.post(url, data=json.dumps(hostget), headers=headers)


# group_id = hgroupget("name", "VPS linux servers").json()["result"][0]["groupid"]

# zcount = 0
# while zcount < len(hostget("groupid", group_id).json()["result"]):
#     print(hostget("groupid", group_id).json()["result"][zcount]["hostid"])
#     zcount += 1

# print(hostget("groupid", group_id).json()["result"][1])

# paramslst={ "filter": dict(groupids=["Zabbix server", "Linux server"])}
# hostget = dict(jsonrpc="2.0", method="host.get", params=paramslst, auth=authtock, id=1)
# print(requests.post(url, data=json.dumps(hostget), headers=headers).json())

# print(hostint("hostid", "10107").json())

for i in anshlist("all"):
    h_ip = ansvarinfo(i, "ansible_host")
    ifinfo = hostint("ip", h_ip).json()["result"]
    if ifinfo:
        print(ifinfo)
    else:
        print("Host", i, "not in zabbix")
