import json
import requests
import os
import sys
import subprocess
import re


class zabbReq(object):
    def __init__(self, creds):
        self.headers = {'content-type': 'application/json-rpc'}
        self.url = creds["url"]
        self.authdata = dict(jsonrpc="2.0", method="user.login",
                             params=dict(user=creds["user"], password=creds["passwd"]), id="1")
        self.authtock = requests.post(self.url, data=json.dumps(self.authdata), headers=self.headers)
        print(self.authtock.status_code)
        # self.authtock = requests.post(self.url, data=json.dumps(self.authdata), headers=self.headers).json()["result"]
        self.basedata = dict(jsonrpc="2.0", auth=self.authtock, id=1)

    # def req_post(self, req_data):
    #     full_data = self.basedata.copy()
    #     full_data["method"] = req_data["method"]
    #     full_data["params"] = req_data["data"]
    #     return requests.post(self.url, data=json.dumps(full_data), headers=self.headers).json()
    #
    # def hostidbyip(self, host_ip):
    #     find_data = dict(filter=dict(ip=host_ip))
    #     res_req = self.req_post(dict(data=find_data, method="hostinterface.get"))["result"]
    #     if len(res_req) > 0:
    #         host_id =res_req[0]["hostid"]
    #         return host_id
    #     else:
    #         print("Host not found")
    #         return False


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
#     hostget = dict(jsonrpc="2.0", method="host.get", params=paramslst,
#                    auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(hostget), headers=headers)
#
#
# def hgroupget(param, param1):
#     paramslst = dict(output="extend")
#     paramsfilter = dict()
#     paramsfilter[param] = param1
#     paramslst["filter"] = paramsfilter
#     hostget = dict(jsonrpc="2.0", method="hostgroup.get", params=paramslst,
#                    auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(hostget), headers=headers)
#
#
# def trigget(**params):
#     paramslst = params
#     hostget = dict(jsonrpc="2.0", method="trigger.get", params=paramslst,
#                    auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(hostget), headers=headers)
#
#
# def templateget(param, param1):
#     paramslst = dict(output="extend")
#     paramsfilter = dict()
#     paramsfilter[param] = param1
#     paramslst["filter"] = paramsfilter
#     hostget = dict(jsonrpc="2.0", method="template.get", params=paramslst,
#                    auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(hostget), headers=headers)
#
#
# def graphinfo(hostid, graph_name):
#     paramslst = dict(output="extend")
#     paramslst["hostids"] = hostid
#     paramslst["filter"] = dict(name=graph_name)
#     graphgetall = dict(jsonrpc="2.0", method="graph.get", params=paramslst,
#                        auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(graphgetall), headers=headers)
#
#
# def graphinfo_id(graphid):
#     paramslst = dict(output="extend")
#     paramslst["filter"] = dict(graphid=graphid)
#     graphgetall = dict(jsonrpc="2.0", method="graph.get", params=paramslst,
#                        auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(graphgetall), headers=headers)
#
#
# def screeninfo(screenname):
#     paramslst = dict(output="extend")
#     paramslst["filter"] = dict(name=screenname)
#     screengetall = dict(jsonrpc="2.0", method="screen.get", params=paramslst,
#                         auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(screengetall), headers=headers)
#
#
# def screeniteminfo(screen_id, hpos, vprevpos):
#     paramslst = dict(output="extend")
#     paramslst["screenids"] = screen_id
#     paramslst["filter"] = dict(x=hpos, y=vprevpos)
#     screenitemgetall = dict(jsonrpc="2.0", method="screenitem.get", params=paramslst,
#                             auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(screenitemgetall), headers=headers)
#
#
# def shell_comm(sh_comm):
#     return os.system(sh_comm)
#
#
# def shell_stdout(sh_comm):
#     return os.popen(sh_comm).read()
#
#
# def ansvarinfo(hostname, ansvar):
#     var_sring = "var=" + ansvar
#     param = ['ansible', '-o', '-m', 'debug'] + [hostname] + ['-a'] + [var_sring]
#     value = subprocess.check_output(param)
#     value = re.sub('^.*\{', '{', value, count=1)
#     return json.loads(value)[ansvar]
#
#
# def anshlist(list):
#     param = ['ansible', '--list-hosts'] + [list]
#     value = subprocess.check_output(param)
#     value = value.replace("\n", " ")
#     value = re.sub("^.*hosts \(.*\):", "", value, count=1)
#     value = re.sub("^ +", "", value)
#     value = re.sub(" +$", "", value)
#     value = re.sub(" +", " ", value)
#     value = value.split(" ")
#     return value
#
#
# def ansshell(comm, hst):
#     param = ['ansible', '-b', "-o", "-m", "shell", "-a"] + [comm] + [hst]
#     try:
#         value = subprocess.check_output(param)
#         value = re.sub('^.+stdout\) +', '', value, count=1)
#         value = re.sub('\n +\n', '\n', value, count=1)
#         value = value.rstrip('\n')
#     except subprocess.CalledProcessError, e:
#         error_lst = ['Error']
#         error_lst = error_lst.append(e.output)
#         return error_lst
#     return value
#
#
# def hostint(param, param1):
#     paramslst = dict(output="extend")
#     paramsfilter = dict()
#     paramsfilter[param] = param1
#     paramslst["filter"] = paramsfilter
#     hostget = dict(jsonrpc="2.0", method="hostinterface.get", params=paramslst,
#                    auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(hostget), headers=headers)
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
#     httptestget = dict(jsonrpc="2.0", method="httptest.get", params=paramslst,
#                    auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(httptestget), headers=headers)
#
#
# def httptestdel(httptestid):
#     paramslst = dict()
#     paramslst["httptestid"] = httptestid
#     httptestdel = dict(jsonrpc="2.0", method="httptest.delete", params=paramslst,
#                    auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(httptestdel), headers=headers)
#
#
# def httptestadd(**papams):
#     paramslst = dict(papams)
#     httptestget = dict(jsonrpc="2.0", method="httptest.create", params=paramslst,
#                    auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(httptestget), headers=headers)
#
#
# def httptestupd(**papams):
#     paramslst = dict(papams)
#     httptestget = dict(jsonrpc="2.0", method="httptest.update", params=paramslst,
#                    auth=authtock, id=1)
#     return requests.post(url, data=json.dumps(httptestget), headers=headers)
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
