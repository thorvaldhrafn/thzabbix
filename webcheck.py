import json
import requests

from functions import url, authtock, headers, hostget, hgroupget, anshlist, ansvarinfo, ansshell


def hostint(param, param1):
    paramslst = dict(output="extend")
    paramsfilter = dict()
    paramsfilter[param] = param1
    paramslst["filter"] = paramsfilter
    hostget = dict(jsonrpc="2.0", method="hostinterface.get", params=paramslst,
                   auth=authtock, id=1)
    return requests.post(url, data=json.dumps(hostget), headers=headers)


def histidbyip(host_ip):
    host_id = hostint("ip", host_ip).json()["result"][0]["hostid"]
    return host_id


def httptestget(param, param1):
    paramslst = dict(output="extend", selectSteps="extend")
    paramsfilter = dict()
    paramsfilter[param] = param1
    paramslst["filter"] = paramsfilter
    hostget = dict(jsonrpc="2.0", method="httptest.get", params=paramslst,
                   auth=authtock, id=1)
    return requests.post(url, data=json.dumps(hostget), headers=headers)

def httptrigadd(**papams):
    paramslst = dict(papams)
    httptestget = dict(jsonrpc="2.0", method="trigger.create", params=paramslst,
                       auth=authtock, id=1)
    return requests.post(url, data=json.dumps(httptestget), headers=headers)


# def httptrigadd(**papams):
#     paramslst = dict(papams)
#     httptestget = dict(jsonrpc="2.0", method="trigger.create", params=paramslst,
#                        auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(httptestget), headers=headers)


groupname = "VPS linux servers"
group_id = hgroupget("name", groupname).json()["result"][0]["groupid"]

# print(group_id)

# zcount = 0
# while zcount < len(hostget("groupid", group_id).json()["result"]):
#     print(hostget("groupid", group_id).json()["result"][zcount]["hostid"])
#     zcount += 1

ip_test = "192.237.188.201"
test_id = histidbyip(ip_test)
# for i in httptestget("hostid", test_id).json()["result"]:
#     # print(i["httptestid"])
#     httptestid = i["httptestid"]
#     for j in httptestget("httptestid", httptestid).json()["result"][0]["steps"]:
#         http_scen = j["name"]
#         trig_desr = str("Web scenario \"" + http_scen + " failed: {ITEM.VALUE}")
#         trig_expr = str(
#             "{host:web.test.error[" + http_scen + "].strlen()}>0 and {host:web.test.fail[" + http_scen + "].last()}>0")
#         print(trig_desr)
#         print(trig_expr)

trig_param = dict()
trig_param["description"] = "4"
trig_param["description"] = str("Web scenario \"home.antivirus-lab.com failed: {ITEM.VALUE}")
trig_param["expression"] = str("{antivirus-lab.com:web.test.error[home.antivirus-lab.com].strlen()}>0 and {antivirus-lab.com:web.test.fail[home.antivirus-lab.com].last()}>0")
print(httptrigadd(**trig_param).json())

# def httptrigadd(**papams):
#     paramslst = dict(papams)
#     httptestget = dict(jsonrpc="2.0", method="trigger.create", params=paramslst,
#                        auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(httptestget), headers=headers)
#
# http_scen = "test"
# trig_desr = str("Web scenario \"" + http_scen + " failed: {ITEM.VALUE}")
# trig_expr = str("{host:web.test.error[" + http_scen + "].strlen()}>0 and {host:web.test.fail[" + http_scen + "].last()}>0")

    # "method": "trigger.create",
    # "params": [
    #     {
    #         "description": "Processor load is too high on {HOST.NAME}",
    #         "expression": "{Linux server:system.cpu.load[percpu,avg1].last()}>5",


# print(hostget("groupid", group_id).json()["result"][1])

# paramslst={ "filter": dict(groupids=["Zabbix server", "Linux server"])}
# hostget = dict(jsonrpc="2.0", method="host.get", params=paramslst, auth=authtock, id=1)
# print(requests.post(url, data=json.dumps(hostget), headers=headers).json())

# print(hostint("hostid", "10107").json())

# ans_hlist = anshlist("all")
# ans_hlist_ips = dict()
# for hst in ans_hlist:
#     ans_hlist_ips[hst] = ansvarinfo(hst, "ansible_host")
#
# for anshst, h_ip in ans_hlist_ips.iteritems():
#     shell_comm = "bash /usr/local/thscripts/bin/ths-list-domains.sh"
#     result = ansshell(shell_comm, anshst)
#     if isinstance(result,(list,)):
#         print(result)
#     else:
#         print(h_ip, ansshell(shell_comm, anshst))
#
# print("End")

# shell_comm = "bash /usr/local/thscripts/bin/ths-check-domain.sh"
# print(ansshell(shell_comm, "gridinsoft.com"))


# for i in ans_hlist:
#     h_ip = ansvarinfo(i, "ansible_host")
#     ifinfo = hostint("ip", h_ip).json()["result"]
#     if ifinfo:
#         print(ifinfo)
#     else:
#         print("Host", i, "not in zabbix")

# hquan = len((hostget("groupid", "group_id")).json()["result"])
# hpos = 0
#
# while hpos < hquan:
#     hpos_hostid = hostget("groupid", "group_id").json()["result"][hpos]["hostid"]
#     hpos_hostip = hostint("hostid", hpos_hostid).json()["result"][0]["ip"]
#     for anshst, h_ip in ans_hlist_ips.iteritems():
#         if h_ip == hpos_hostip:
#             break
#     else:
#         hname = hostget("hostid", hpos_hostid).json()["result"][0]["name"]
#         print(hname, hpos_hostip, "not found")
#     hpos += 1
