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
    for field in ["services", "networks"]:
        if data.get(field) is None:
            print(
                f"Missing required field {field} in compose file !",
                file=sys.stderr,
            )
            return (False, [], [])
    networks = list(data.get("networks").keys())
    services = {
        k: {
            "action": "image" if v.get("image") else "build",
            "image": v.get("image") or v.get("build"),
            "networks": v.get("networks") or [],
            "deps": v.get("depends_on") or [],
            "outbound_access": True if v.get("ports") else False,
        }
        for k, v in data.get("services").items()
    }
    network_groups = {network: [] for network in networks}
    for node, nets in services.items():
        for network in nets.get("networks"):
            if network in network_groups:
                network_groups[network].append(node)

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
            }
        )
    links = []
    for link in connections:
        links.append(
            {
                "source": list(services.keys()).index(link[0]),
                "target": list(services.keys()).index(link[1]),
                "curvature": random.randint(20, 40) / 100,
                "color": "#0f83d0",
            }
        )

    return (
        True,
        nodes,
        links,
    )
