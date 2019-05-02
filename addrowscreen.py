import json
import requests
import sys

sys.path.append("./")

from functions import url, authtock, headers, hostget, screeninfo, screeniteminfo, graphinfo_id, graphinfo

hostname = sys.argv[1]

host_id = hostget("host", hostname).json()["result"][0]["hostid"]

screeninfo_json = screeninfo("All Servers").json()["result"][0]

vpos = int(screeninfo_json["vsize"])
hlen = int(screeninfo_json["hsize"])
screen_id = int(screeninfo_json["screenid"])

vpreppos = vpos-1

screen_vsize = vpos+1

get_prow_req = screeniteminfo(screen_id, "", vpreppos).json()["result"]

screen_res_param = dict(jsonrpc="2.0", method="screen.update", params=dict(screenid=screen_id, vsize=screen_vsize), auth=authtock, id=1)
screenresget = requests.post(url, data=json.dumps(screen_res_param), headers=headers)

print(screenresget.json())

hpos = 0
while hpos < hlen:
    vpreppos = vpos-1
    get_pitem_req = get_prow_req[hpos]
    iheight = get_pitem_req["height"]
    iwidth = get_pitem_req["width"]
    irowspan = get_pitem_req["rowspan"]
    icolspan = get_pitem_req["colspan"]
    imax_columns = get_pitem_req["max_columns"]
    presource_id = get_pitem_req["resourceid"]
    graph_name = graphinfo_id(presource_id).json()["result"][0]["name"]
    graph_id = graphinfo(host_id, graph_name).json()["result"][0]["graphid"]
    graphitem_id = graphinfo("", graph_id).json()["result"]
    add_item_param = dict(jsonrpc="2.0", method="screenitem.create",
                          params=dict(screenid=screen_id, resourcetype="0", resourceid=graph_id, x=hpos, y=vpos, height=iheight, width=iwidth, rowspan=irowspan, colspan=icolspan, max_columns=imax_columns),
                          auth=authtock, id=1)
    add_item_req = requests.post(url, data=json.dumps(add_item_param), headers=headers)
    print(add_item_req.json())
    hpos += 1
