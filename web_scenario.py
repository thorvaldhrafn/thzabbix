import json
import requests

from functions import url, authtock, headers, hostget, hgroupget, anshlist, ansvarinfo, ansshell, hostint, histidbyip, httptestget, httptestdel



ip_test = "192.237.188.201"
test_id = histidbyip(ip_test)
url_test = "http://bind.antivirus-lab.com/"
url_code = "200"

for i in httptestget("hostid", test_id).json()["result"]:
    print(i["httptestid"])
    httptestid = i["httptestid"]
    for j in httptestget("httptestid", httptestid).json()["result"][0]["steps"]:
        print(j["url"], j["status_codes"])

# print(httptestdel("8"))
