import json
import requests
import os
import yaml
import sys
import subprocess
import re



def conf_get(conf_file):
    conf_param = dict()
    with open(conf_file) as conf:
        for line in conf:
            if line[0] != "#":
                line = line.rstrip('\n').split('=')
                conf_param[line[0]] = line[1]
    return conf_param


def hostget(param, param1):
    paramslst = dict(output="extend")
    paramsfilter = dict()
    paramsfilter[param] = param1
    paramslst["filter"] = paramsfilter
    hostget = dict(jsonrpc="2.0", method="host.get", params=paramslst,
                   auth=authtock, id=1)
    return requests.post(url, data=json.dumps(hostget), headers=headers)


def hgroupget(param, param1):
    paramslst = dict(output="extend")
    paramsfilter = dict()
    paramsfilter[param] = param1
    paramslst["filter"] = paramsfilter
    hostget = dict(jsonrpc="2.0", method="hostgroup.get", params=paramslst,
                   auth=authtock, id=1)
    return requests.post(url, data=json.dumps(hostget), headers=headers)


def templateget(param, param1):
    paramslst = dict(output="extend")
    paramsfilter = dict()
    paramsfilter[param] = param1
    paramslst["filter"] = paramsfilter
    hostget = dict(jsonrpc="2.0", method="template.get", params=paramslst,
                   auth=authtock, id=1)
    return requests.post(url, data=json.dumps(hostget), headers=headers)


def graphinfo(hostid, graph_name):
    paramslst = dict(output="extend")
    paramslst["hostids"] = hostid
    paramslst["filter"] = dict(name=graph_name)
    graphgetall = dict(jsonrpc="2.0", method="graph.get", params=paramslst,
                       auth=authtock, id=1)
    return requests.post(url, data=json.dumps(graphgetall), headers=headers)


def graphinfo_id(graphid):
    paramslst = dict(output="extend")
    paramslst["filter"] = dict(graphid=graphid)
    graphgetall = dict(jsonrpc="2.0", method="graph.get", params=paramslst,
                       auth=authtock, id=1)
    return requests.post(url, data=json.dumps(graphgetall), headers=headers)


def screeninfo(screenname):
    paramslst = dict(output="extend")
    paramslst["filter"] = dict(name=screenname)
    screengetall = dict(jsonrpc="2.0", method="screen.get", params=paramslst,
                        auth=authtock, id=1)
    return requests.post(url, data=json.dumps(screengetall), headers=headers)


def screeniteminfo(screen_id, hpos, vprevpos):
    paramslst = dict(output="extend")
    paramslst["screenids"] = screen_id
    paramslst["filter"] = dict(x=hpos, y=vprevpos)
    screenitemgetall = dict(jsonrpc="2.0", method="screenitem.get", params=paramslst,
                            auth=authtock, id=1)
    return requests.post(url, data=json.dumps(screenitemgetall), headers=headers)


def shell_comm(sh_comm):
    return os.system(sh_comm)


def shell_stdout(sh_comm):
    return os.popen(sh_comm).read()


def ansvarinfo(hostname, ansvar):
    var_sring = "var=" + ansvar
    param = ['ansible', '-o', '-m', 'debug'] + [hostname] + ['-a'] + [var_sring]
    value = subprocess.check_output(param)
    value = re.sub('^.*\{', '{', value, count=1)
    return json.loads(value)[ansvar]


def shell_stdout(sh_comm):
    return os.popen(sh_comm).read()

access_param = conf_get(os.path.dirname(sys.argv[0]) + "/access.conf")

user = access_param["user"]
passwd = access_param["passwd"]
url = access_param["url"]

authdata = {"jsonrpc": "2.0", "method": "user.login", "params": {"user": user, "password": passwd}, "id": "1"}
headers = {'content-type': 'application/json-rpc'}

auth_req = requests.post(url, data=json.dumps(authdata), headers=headers)

authtock = auth_req.json()["result"]
