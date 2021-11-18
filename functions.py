import json
import requests
import os
import sys


class ZabbReq(object):
    def __init__(self, creds):
        self.headers = {'content-type': 'application/json-rpc'}
        self.url = creds["url"]
        self.authdata = dict(jsonrpc="2.0", method="user.login",
                             params=dict(user=creds["user"], password=creds["passwd"]), id="1")
        self.authtock = requests.post(self.url, data=json.dumps(self.authdata), headers=self.headers).json()["result"]
        self.basedata = dict(jsonrpc="2.0", auth=self.authtock, id=1)

    def req_post(self, req_data):
        full_data = self.basedata.copy()
        full_data["method"] = req_data["method"]
        full_data["params"] = req_data["data"]
        return requests.post(self.url, data=json.dumps(full_data), headers=self.headers).json()

    def hostidbyip(self, host_ip):
        find_data = dict(filter=dict(ip=host_ip))
        res_req = self.req_post(dict(data=find_data, method="hostinterface.get"))["result"]
        if len(res_req) > 0:
            host_id = res_req[0]["hostid"]
            return host_id
        else:
            print("Host not found")
            return False

    def hostipbyid(self, host_id):
        find_data = dict(filter=dict(hostid=host_id))
        res_req = self.req_post(dict(data=find_data, method="hostinterface.get"))["result"]
        host_ip = res_req[0]["ip"]
        return host_ip

    def lf_data(self, method_get, param, param1):
        paramslst = dict(output="extend")
        paramsfilter = dict()
        paramsfilter[param] = param1
        if method_get == "host":
            method_rst = "host.get"
        elif method_get == "hostgroup":
            method_rst = "hostgroup.get"
        elif method_get == "template":
            method_rst = "template.get"
        elif method_get == "hostinterface":
            method_rst = "hostinterface.get"
        elif method_get == "httptest":
            paramslst = dict(output="extend", selectSteps="extend", selectTags="extend")
            method_rst = "httptest.get"
        else:
            return False
        paramslst["filter"] = paramsfilter
        host_get = dict(method=method_rst, data=paramslst)
        return self.req_post(host_get)["result"]

    def addhost(self, hcreatedata):
        addhost_get = dict(method="host.create", data=hcreatedata)
        return self.req_post(addhost_get)

    def hostslist(self):
        paramslst = dict(output="extend")
        hosts_get = dict(method="host.get", data=paramslst)
        hosts_get_data = self.req_post(hosts_get)["result"]
        return hosts_get_data

    def hostsidlist(self):
        full_data_lst = self.hostslist()
        res_lst = list()
        for i in full_data_lst:
            res_lst.append(i["hostid"])
        return res_lst


# def conf_get(conf_file):
#     conf_param = dict()
#     with open(conf_file) as conf:
#         for line in conf:
#             if line[0] != "#":
#                 line = line.rstrip('\n').split('=')
#                 conf_param[line[0]] = line[1]
#     return conf_param
#
#
# def hostget(param, param1):
#     paramslst = dict(output="extend")
#     paramsfilter = dict()
#     paramsfilter[param] = param1
#     paramslst["filter"] = paramsfilter
#     host_get = dict(jsonrpc="2.0", method="host.get", params=paramslst, auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(host_get), headers=headers)
#
#
# def hgroupget(param, param1):
#     paramslst = dict(output="extend")
#     paramsfilter = dict()
#     paramsfilter[param] = param1
#     paramslst["filter"] = paramsfilter
#     host_get = dict(jsonrpc="2.0", method="hostgroup.get", params=paramslst, auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(host_get), headers=headers)
#
#
# def templateget(param, param1):
#     paramslst = dict(output="extend")
#     paramsfilter = dict()
#     paramsfilter[param] = param1
#     paramslst["filter"] = paramsfilter
#     host_get = dict(jsonrpc="2.0", method="template.get", params=paramslst, auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(host_get), headers=headers)
#
#
# def hostint(param, param1):
#     paramslst = dict(output="extend")
#     paramsfilter = dict()
#     paramsfilter[param] = param1
#     paramslst["filter"] = paramsfilter
#     host_get = dict(jsonrpc="2.0", method="hostinterface.get", params=paramslst, auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(host_get), headers=headers)
#
#
# def hostidbyip(host_ip):
#     if len(hostint("ip", host_ip).json()["result"]) > 0:
#         host_id = hostint("ip", host_ip).json()["result"][0]["hostid"]
#         return host_id
#     else:
#         print("Host not found")
#         return False
#
#
# def httptestget(param, param1):
#     paramslst = dict(output="extend", selectSteps="extend")
#     paramsfilter = dict()
#     paramsfilter[param] = param1
#     paramslst["filter"] = paramsfilter
#     httptest_get = dict(jsonrpc="2.0", method="httptest.get", params=paramslst, auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(httptest_get), headers=headers)
#
#
# def addhost(hcreatedata):
#     addhost_get = dict(jsonrpc="2.0", method="host.create", params=hcreatedata, auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(addhost_get), headers=headers)
#
#
# access_param = conf_get(os.path.dirname(sys.argv[0]) + "/access.conf")
#
# user = access_param["user"]
# passwd = access_param["passwd"]
# url = access_param["url"]
#
# authdata = {"jsonrpc": "2.0", "method": "user.login", "params": {"user": user, "password": passwd}, "id": "1"}
# headers = {'content-type': 'application/json-rpc'}
#
# auth_req = requests.post(url, data=json.dumps(authdata), headers=headers)
#
# authtock = auth_req.json()["result"]
