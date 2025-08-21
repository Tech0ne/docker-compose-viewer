import random
import sys
from itertools import combinations

import yaml


def get_nodes_and_links(file):
    try:
        data = yaml.safe_load(file)
    except Exception as e:
        print(f"[ERROR] Could not read compose file: {e}", file=sys.stderr)
        return (False, [], [])
    networks = data.get("networks")
    networks = list(networks.keys()) if networks else []

    services = data.get("services")
    services = {
        k: {
            "action": "image" if v.get("image") else "build",
            "image": v.get("image") or v.get("build"),
            "networks": v.get("networks") or [],
            "dependencies": v.get("depends_on") or [],
            "outbound": (
                True
                if (v.get("ports") or str(v.get("network_mode")) == "host")
                else False
            ),
        }
        for k, v in (services.items() if services else [])
    }

    if len(networks):
        network_groups = {network: [] for network in networks}
        for node, nets in services.items():
            for network in nets.get("networks"):
                if network in network_groups:
                    network_groups[network].append(node)
    else:
        network_groups = {"all": list(services.keys())}

    connections = set()
    for network, members in network_groups.items():
        for node1, node2 in combinations(members, 2):
            if not (node2, node1) in connections:
                connections.add((node1, node2))

    nodes = []
    for node_name in services.keys():
        nodes.append(
            {
                "id": len(nodes),
                "name": node_name,
                services[node_name].get("action"): services[node_name].get("image"),
                "color": "#E4E8C1",
            }
        )
    links = []
    for link in connections:
        links.append(
            {
                "source": list(services.keys()).index(link[0]),
                "target": list(services.keys()).index(link[1]),
                "curvature": 0,
                "particles": 0,
                "color": "#0f83d0",
            }
        )

    for node, infos in services.items():
        for dep in infos.get("dependencies") or []:
            links.append(
                {
                    "source": list(services.keys()).index(node),
                    "target": list(services.keys()).index(dep),
                    "curvature": random.randint(30, 40) / 100,
                    "particles": 3,
                    "color": "#00797d",
                }
            )

    if any([node.get("outbound") for node in services.values()]):
        nodes.append(
            {
                "id": -1,
                "name": "External",
                "color": "#e60000",
            }
        )
        for node in filter((lambda node: node[1].get("outbound")), services.items()):
            links.append(
                {
                    "source": -1,
                    "target": list(services.keys()).index(node[0]),
                    "curvature": 0,
                    "particles": 3,
                    "color": "#b32300",
                }
            )

    return (
        True,
        nodes,
        links,
    )
