import itertools
import numpy as np


with open("2024-23-lan-party/input.txt") as f:
    edges = [tuple(l.split("-")) for line in f if (l := line.strip())]


print(edges)

node_id = {}
for e in itertools.chain(*edges):
    if e not in node_id:
        node_id[e] = len(node_id)

m = np.zeros((len(node_id), len(node_id)), dtype=np.int32)
for a, b in edges:
    m[node_id[a], node_id[b]] = 1
    m[node_id[b], node_id[a]] = 1


t_mask = np.zeros(len(node_id), dtype=np.int32)
for k, id in node_id.items():
    t_mask[id] = int(k.startswith("t"))


total_triangles = ((m @ m) * m).sum() // 6

mt = (
    m
    * (1 - t_mask.reshape((1, len(node_id))))
    * (1 - t_mask.reshape((len(node_id), 1)))
)
triangles_without_t = ((mt @ mt) * mt).sum() // 6


print(total_triangles)
print(total_triangles - triangles_without_t)
