import json
import requests
import sys
import os

from functions import url, authtock, headers, hgroupget, templateget, inventory_pars, shell_stdout, host_specs

filedir = os.path.dirname(sys.argv[0])
sys.path.append(filedir)

inv_path = sys.argv[1]
hostname = sys.argv[2]

inventory_list = inventory_pars(inv_path)

newhost_specs = host_specs(inventory_list, hostname)

host_ip = newhost_specs["ansible_host"]
host_port = newhost_specs["zabbix_port"]
host_group = newhost_specs["zabbix_host_group"]
host_tmplt = newhost_specs["zabbix_host_tmplt"]
host_tls = newhost_specs["zabbix_tls"]

if host_tls:
    inv_str = '--inventory=\"' + inv_path + '\"'
    psk_get = 'ansible ' + inv_str + ' -b -m shell -a \"cat /etc/zabbix/zabbix_agentd.conf | grep TLSPSKIdentity\" ' + hostname + ' | grep TLSPSKIdentity | awk -F"=" \'{ print $2 }\''
    psk_identity = os.popen(psk_get).read().rstrip()
    psk_get_key = 'ansible ' + inv_str + ' -b -m shell -a "cat /etc/zabbix/zabbix_agentd.psk" ' + hostname + " | tail -1"
    psk_key = shell_stdout(psk_get_key).rstrip()
    tlsconnect = "2"
    tlsaccept = "2"
else:
    psk_identity = ""
    psk_key = ""
    tlsconnect = "1"
    tlsaccept = "1"

group_id = hgroupget("name", host_group).json()["result"][0]["groupid"]
template_id = templateget("host", host_tmplt).json()["result"][0]["templateid"]

hostcreate = dict(jsonrpc="2.0", method="host.create", params=dict(host=hostname, tls_connect=tlsconnect,
                                                                   tls_accept=tlsaccept, tls_psk_identity=psk_identity,
                                                                   tls_psk=psk_key,
                                                                   interfaces=[
                                                                       dict(type=1, main=1, useip=1,
                                                                            ip=host_ip, dns="", port=host_port)
                                                                   ], groups=[
        dict(groupid=group_id)
    ], templates=[
        dict(templateid=template_id)
    ]), auth=authtock, id=1)

hostcreate_req = requests.post(url, data=json.dumps(hostcreate), headers=headers)

print(hostcreate_req.json())
