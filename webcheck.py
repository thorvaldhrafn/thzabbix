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


groupname = "VPS linux servers"
group_id = hgroupget("name", groupname).json()["result"][0]["groupid"]

# zcount = 0
# while zcount < len(hostget("groupid", group_id).json()["result"]):
#     print(hostget("groupid", group_id).json()["result"][zcount]["hostid"])
#     zcount += 1

# print(hostget("groupid", group_id).json()["result"][1])

# paramslst={ "filter": dict(groupids=["Zabbix server", "Linux server"])}
# hostget = dict(jsonrpc="2.0", method="host.get", params=paramslst, auth=authtock, id=1)
# print(requests.post(url, data=json.dumps(hostget), headers=headers).json())

# print(hostint("hostid", "10107").json())

ans_hlist = anshlist("all")
ans_hlist_ips = dict()
for hst in ans_hlist:
    ans_hlist_ips["hst"] = ansvarinfo(hst, "ansible_host")

# for i in ans_hlist:
#     h_ip = ansvarinfo(i, "ansible_host")
#     ifinfo = hostint("ip", h_ip).json()["result"]
#     if ifinfo:
#         print(ifinfo)
#     else:
#         print("Host", i, "not in zabbix")

hquan = len((hostget("groupid", "group_id")).json()["result"])
hpos = 0

for anshst, h_ip in ans_hlist_ips.iteritems():
    print(anshst, h_ip)

# while hpos < hquan:
#     hpos_hostid = hostget("groupid", "group_id").json()["result"][hpos]["hostid"]
#     hpos_hostip = hostint("hostid", hpos_hostid).json()["result"][0]["ip"]
#     for anshst, h_ip in ans_hlist_ips.iteritems():
#         print(anshst, h_ip)
#         if h_ip == hpos_hostip:
#             print(anshst)
#             continue
#         else:
#             hname = hostget("hostid", hpos_hostid).json()["result"][0]["name"]
#             print(hname, "not found")
#     hpos += 1
