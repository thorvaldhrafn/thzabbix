import json
import requests
import sys

from functions import url, authtock, headers, hostget, screeninfo, screeniteminfo, graphinfo_id, graphinfo


def screenresize(screen_id, vpos):
    screen_res_param = dict(jsonrpc="2.0", method="screen.update", params=dict(screenid=screen_id, vsize=vpos), auth=authtock, id=1)
    screenres = requests.post(url, data=json.dumps(screen_res_param), headers=headers)
    return screenres


def add_items(**add_item_param):
    add_item_param = dict(add_item_param)
    add_item_req = requests.post(url, data=json.dumps(add_item_param), headers=headers)
    return add_item_req

hostname = sys.argv[1]
screen_name = "All Servers"

host_id = hostget("host", hostname).json()["result"][0]["hostid"]

screeninfo_json = screeninfo(screen_name).json()["result"][0]

vpos = int(screeninfo_json["vsize"])
hlen = int(screeninfo_json["hsize"])
screen_id = int(screeninfo_json["screenid"])

vpreppos = vpos-1

screen_vsize = vpos+1

get_prow_req = screeniteminfo(screen_id, "", vpreppos).json()["result"]

hpos = 0
lst_fadd = list()
while hpos < hlen:
    get_pitem_req = get_prow_req[hpos]
    graph_name = graphinfo_id(get_pitem_req["resourceid"]).json()["result"][0]["name"]
    try:
        graph_id = graphinfo(host_id, graph_name).json()["result"][0]["graphid"]
        graphitem_id = graphinfo("", graph_id).json()["result"]
        add_item_param = dict(jsonrpc="2.0", method="screenitem.create",
                              params=dict(screenid=screen_id, resourcetype="0", resourceid=graph_id, x=hpos, y=vpos, height=get_pitem_req["height"], width=get_pitem_req["width"], rowspan=get_pitem_req["rowspan"], colspan=get_pitem_req["colspan"], max_columns=get_pitem_req["max_columns"]),
                              auth=authtock, id=1)
        lst_fadd.append(add_item_param)
    except IndexError:
        pass
    hpos += 1

screenresize(screen_id, screen_vsize)

for i in lst_fadd:
    print(i)
    print(add_items(**i).json())
