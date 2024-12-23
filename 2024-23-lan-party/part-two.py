import networkx as nx


with open("2024-23-lan-party/input.txt") as f:
    edges = [tuple(l.split("-")) for line in f if (l := line.strip())]


g = nx.Graph()
g.add_edges_from(edges)

print(",".join(sorted(max(nx.clique.find_cliques(g), key=lambda c: len(c)))))
