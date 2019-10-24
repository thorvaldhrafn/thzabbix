import json
import requests

from functions import headers, url, authtock, hostidbyip


class HTTPtest(object):
    def __init__(self):
        self.test_delay = str("3m")
        self.test_timeout = str("30s")
        self.test_redir = str("0")

    def _addparam(self, add_params):
        try:
            add_params["test_delay"]
        except KeyError:
            add_params["test_delay"] = self.test_delay
        try:
            add_params["test_timeout"]
        except KeyError:
            add_params["test_timeout"] = self.test_timeout
        try:
            add_params["test_redir"]
        except KeyError:
            add_params["test_redir"] = self.test_redir
        return add_params

    def httptest_addlist(self, add_params):
        add_params = self._addparam(add_params)
        host_id = hostidbyip(add_params["host_ip"])
        full_params = {"hostid": host_id, "delay": add_params["test_delay"], "name": add_params["domain"], "retries": str("3")}
        steps_dict = {"name": add_params["domain"], "url": add_params["url"], "follow_redirects": add_params["test_redir"], "timeout": add_params["test_timeout"], "status_codes": add_params["test_code"], "no": str("1")}
        steps_list = list()
        steps_list.append(steps_dict)
        full_params["steps"] = steps_list
        return full_params

    def httptest_updlist(self, upd_params):
        upd_params = self._addparam(upd_params)
        full_params = {"httptestid": upd_params["httptestid"], "delay": upd_params["test_delay"]}
        steps_dict = {"follow_redirects": upd_params["test_redir"], "name": upd_params["domain"], "url": upd_params["url"], "timeout": upd_params["test_timeout"], "status_codes": upd_params["code"], "no": str("1")}
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
