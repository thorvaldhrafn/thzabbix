import json
import requests

from functions import headers, url, authtock, hostidbyip


class HTTPtest(object):
    def __init__(self):
        self.delay = str("3m")
        self.timeout = str("30s")
        self.follow_redirects = str("0")

    def _addparam(self, add_params):
        try:
            add_params["delay"]
        except KeyError:
            add_params["delay"] = self.delay
        try:
            add_params["timeout"]
        except KeyError:
            add_params["timeout"] = self.timeout
        try:
            add_params["follow_redirects"]
        except KeyError:
            add_params["follow_redirects"] = self.follow_redirects
        return add_params

    def httptest_addlist(self, add_params):
        add_params = self._addparam(add_params)
        host_id = hostidbyip(add_params["host_ip"])
        full_params = {"hostid": host_id, "delay": add_params["delay"], "name": add_params["name"], "retries": str("3")}
        steps_dict = {"name": add_params["domain"], "url": add_params["url"], "follow_redirects": add_params["follow_redirects"], "timeout": add_params["timeout"], "status_codes": add_params["status_codes"], "no": str("1")}
        steps_list = list()
        steps_list.append(steps_dict)
        full_params["steps"] = steps_list
        return full_params

    def httptest_updlist(self, upd_params):
        upd_params = self._addparam(upd_params)
        full_params = {"httptestid": upd_params["httptestid"], "delay": upd_params["test_delay"]}
        steps_dict = {"follow_redirects": upd_params["follow_redirects"], "name": upd_params["name"], "url": upd_params["url"], "timeout": upd_params["timeout"], "status_codes": upd_params["status_codes"], "no": str("1")}
        steps_list = list()
        steps_list.append(steps_dict)
        full_params["steps"] = steps_list
        return full_params


    def httptestdel(self, httptestid):
        paramslst = {"httptestid": httptestid}
        httptestdel = dict(jsonrpc="2.0", method="httptest.delete", params=paramslst,
                       auth=authtock, id=1)
        return requests.post(url, data=json.dumps(httptestdel), headers=headers)

    def httptestadd(self, add_params):
        paramslst = self.httptest_addlist(add_params)
        httptestget = dict(jsonrpc="2.0", method="httptest.create", params=paramslst,
                       auth=authtock, id=1)
        return requests.post(url, data=json.dumps(httptestget), headers=headers)

    def httptestupd(self, upd_params):
        paramslst = self.httptest_updlist(upd_params)
        httptestget = dict(jsonrpc="2.0", method="httptest.update", params=paramslst,
                       auth=authtock, id=1)
        return requests.post(url, data=json.dumps(httptestget), headers=headers)
