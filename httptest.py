import json
import requests

from .functions import hostidbyip


class HTTPtest(object):
    def __init__(self, creds):
        self.authdata = dict(jsonrpc="2.0", method="user.login", params=dict(user=creds["user"], password=creds["passwd"]), id="1")
        self.headers = {'content-type': 'application/json-rpc'}
        self.url = creds["url"]
        self.authtock = requests.post(self.url, data=json.dumps(self.authdata), headers=self.headers).json()["result"]
        self.basedata = dict(jsonrpc="2.0", auth=self.authtock, id=1)
        self.delay = str("3m")
        self.timeout = str("30s")
        self.follow_redirects = 0

    def _req_post(self, req_data):
        return requests.post(self.url, data=json.dumps(req_data), headers=self.headers)

    def _addparam(self, **add_params):
        if not add_params.get("delay"):
            add_params["delay"] = self.delay
        if not add_params.get("timeout"):
            add_params["timeout"] = self.delay
        if not add_params.get("follow_redirects"):
            add_params["follow_redirects"] = self.follow_redirects
        return add_params

    def _httptest_addlist(self, **add_params):
        add_params = self._addparam(**add_params)
        steps_dict = dict(name=add_params["name"], url=add_params.pop("url"), follow_redirects=add_params.pop("follow_redirects"), timeout=add_params.pop("timeout"), status_codes=add_params.pop("status_codes"), no=str("1"))
        steps_list = list()
        steps_list.append(steps_dict)
        add_params["hostid"] = hostidbyip(add_params.pop("host_ip"))
        add_params["steps"] = steps_list
        return add_params

    def _httptest_updlist(self, **upd_params):
        upd_params = self._addparam(**upd_params)
        full_params = dict(httptestid=upd_params.pop("httptestid"), delay=upd_params.pop("delay"))
        steps_dict = upd_params
        steps_dict["no"] = str("1")
        steps_list = list()
        steps_list.append(steps_dict)
        full_params["steps"] = steps_list
        return full_params

    def _httptestdel(self, httptestid):
        paramslst = dict(httptestid=httptestid)
        full_data = self.basedata.copy()
        full_data["params"] = paramslst
        full_data["method"] = "httptest.delete"
        return self._req_post(full_data)

    def _trigg_add(self, name, host):
        trigg_descr = str("Web scenario " + name + " failed: {ITEM.VALUE}")
        trigg_expr = str("{" + host + ":web.test.error[" + name + "].strlen()}>0 and {" + host + ":web.test.fail[" + name + "].last()}>0")
        paramslst = dict(description=trigg_descr, expression=trigg_expr, priority=4)
        full_data = self.basedata.copy()
        full_data["params"] = paramslst
        full_data["method"] = "trigger.create"
        return self._req_post(full_data)

    def _httptestfull(self, params, method):
        host_id = hostidbyip(params["host_ip"])
        hostname = self.hostget(dict(hostid=host_id))["name"]
        check_name = params["name"]
        if method == "httptest.create":
            paramslst = self._httptest_addlist(**params)
        elif method == "httptest.update":
            del params["host_ip"]
            paramslst = self._httptest_updlist(**params)
        else:
            return False
        test_add_data = self.basedata.copy()
        test_add_data["params"] = paramslst
        test_add_data["method"] = method
        httptestret = self._req_post(test_add_data).json()
        triggadd_ret = self._trigg_add(check_name, hostname).json()
        result = list()
        result.append(httptestret)
        result.append(triggadd_ret)
        return result

    def httptestdel(self, del_params):
        httptestid = del_params["httptestid"]
        del_data = self._httptestdel(httptestid)
        return del_data

    def httptestadd(self, add_params):
        method = "httptest.create"
        return self._httptestfull(add_params, method)

    def httptestupd(self, upd_params):
        method = "httptest.update"
        return self._httptestfull(upd_params, method)

    def hostget(self, params):
        paramslst = dict(output="extend")
        paramslst["filter"] = params
        full_data = self.basedata.copy()
        full_data["params"] = paramslst
        full_data["method"] = "host.get"
        return self._req_post(full_data).json()["result"][0]
