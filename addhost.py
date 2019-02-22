import json
import requests


from functions import url, authtock, headers, hgroupget, templateget, shell_comm, newhost_spec, hostname

host_ip = newhost_spec[hostname]["ansible_host"]
host_port = newhost_spec[hostname]["zabbix_port"]
host_group = newhost_spec[hostname]["zabbix_host_group"]
host_tmplt = newhost_spec[hostname]["zabbix_host_tmplt"]

host_tls = newhost_spec[hostname]["zabbix_tls"]

if host_tls:
    psk_get = 'ansible -b -m shell -a "cat /etc/zabbix/zabbix_agentd.conf | grep TLSPSKIdentity" ' + hostname + ' | grep TLSPSKIdentity | awk -F"=" \'{ print $2 }\''
    psk_identity = shell_comm(psk_get)
    psk_get_key = 'ansible -b -m shell -a "cat /etc/zabbix/zabbix_agentd.psk" ' + hostname
    psk_key = shell_comm(psk_get_key)
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
