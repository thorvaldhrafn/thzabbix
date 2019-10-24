import json
import requests

from functions import headers, url, authtock, hostidbyip, hostget


class HTTPtest(object):
    def __init__(self):
        self.delay = str("3m")
        self.timeout = str("30s")
        self.follow_redirects = str("0")

    def _addparam(self, add_params):
        if not add_params.get("delay"):
            add_params["delay"] = self.delay
        if not add_params.get("timeout"):
            add_params["timeout"] = self.delay
        if not add_params.get("follow_redirects"):
            add_params["follow_redirects"] = self.delay
        return add_params

    def httptest_addlist(self, add_params):
        add_params = self._addparam(add_params)
        steps_dict = {"name": add_params["domain"], "url": add_params.pop("url"), "follow_redirects": add_params.pop("follow_redirects"), "timeout": add_params.pop("timeout"), "status_codes": add_params.pop("status_codes"), "no": str("1")}
        steps_list = list()
        steps_list.append(steps_dict)
        add_params["hostid"] = hostidbyip(add_params.pop("host_ip"))
        add_params["steps"] = steps_list
        return add_params

    def httptest_updlist(self, upd_params):
        upd_params = self._addparam(upd_params)
        full_params = dict(httptestid=upd_params.pop("httptestid"), delay=upd_params.pop("delay"))
        steps_dict = upd_params
        steps_dict["no"] = str("1")
        steps_list = list()
        steps_list.append(steps_dict)
        full_params["steps"] = steps_list
        return full_params

    def httptestdel(self, httptestid):
        paramslst = dict(httptestid=httptestid)
        httptestdel = dict(jsonrpc="2.0", method="httptest.delete", params=paramslst,
                       auth=authtock, id=1)
        return requests.post(url, data=json.dumps(httptestdel), headers=headers)

    def _httptestadd(self, paramslst):
        httptestget = dict(jsonrpc="2.0", method="httptest.create", params=paramslst,
                       auth=authtock, id=1)
        return requests.post(url, data=json.dumps(httptestget), headers=headers)

    def httptestupd(self, upd_params):
        paramslst = self.httptest_updlist(upd_params)
        httptestupd = dict(jsonrpc="2.0", method="httptest.update", params=paramslst,
                       auth=authtock, id=1)
        return requests.post(url, data=json.dumps(httptestupd), headers=headers)

    def trigg_add(self, name, host):
        trigg_descr = str("Web scenario " + name + " failed: {ITEM.VALUE}")
        trigg_expr = str("{" + host + ":web.test.error[" + name + "].strlen()}>0 and {" + host + ":web.test.fail[" + name + "].last()}>0")
        paramslst = dict(description=trigg_descr, expression=trigg_expr)
        triggadd = dict(jsonrpc="2.0", method="trigger.create", params=paramslst,
                       auth=authtock, id=1)
        return requests.post(url, data=json.dumps(triggadd), headers=headers)

    def httptestadd(self, add_params):
        hostname = hostget("hostid", hostidbyip(add_params["host_ip"]))
        check_name = add_params["name"]
        paramslst = self.httptest_addlist(add_params)
        httptestret = self._httptestadd(paramslst).json()
        triggadd_ret = self.trigg_add(check_name, hostname).json()
        result = list()
        result.append(httptestret)
        result.append(triggadd_ret)
        return result
