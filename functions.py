import json
import requests


class ZabbReq:
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

    def host_tmplt_list(self, hostid):
        search_data = dict(method="host.get", data=dict(selectParentTemplates=list("templateid"), hostids=hostid))
        result_data = self.req_post(search_data)["result"][0]['parentTemplates']
        templt_lst = list()
        for i in result_data:
            templt_lst.append(i['templateid'])
        return templt_lst

    def host_tmplt_upd(self, hostid, tmplt_lst):
        hupdttedata = dict(hostid=hostid)
        tmplt_lst=list(dict.fromkeys(tmplt_lst))
        hupdttedata["templates"] = tmplt_lst
        updtmplt_req = dict(method="host.update", data=hupdttedata)
        return self.req_post(updtmplt_req)

    def host_tmplt_add(self, hostid, tmplt_id):
        tmplts_list = self.host_tmplt_list(hostid)
        full_list = tmplts_list.append(tmplt_id)
        print(full_list)
        return self.host_tmplt_upd(hostid, full_list)

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