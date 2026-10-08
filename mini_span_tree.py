import streamlit as st
import heapq
import networkx as nx
import matplotlib.pyplot as plt

# -------------------------------
# Union Find for Kruskal
# -------------------------------
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)

        if rx == ry:
            return False

        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx

        self.parent[ry] = rx

        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

        return True


# -------------------------------
# Kruskal Algorithm
# -------------------------------
def kruskal(n, edges):
    edges = sorted(edges)

    uf = UnionFind(n)
    mst = []
    cost = 0

    for w, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            cost += w

        if len(mst) == n - 1:
            break

    return mst, cost


# -------------------------------
# Prim Algorithm
# -------------------------------
def prim(n, adj, start=0):
    key = [float('inf')] * n
    parent = [-1] * n
    in_mst = [False] * n

    key[start] = 0
    pq = [(0, start)]

    mst = []
    cost = 0

    while pq:
        w, u = heapq.heappop(pq)

        if in_mst[u]:
            continue

        in_mst[u] = True

        if parent[u] != -1:
            mst.append((parent[u], u, w))
            cost += w

        for v, wt in adj.get(u, []):
            if not in_mst[v] and wt < key[v]:
                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))

    return mst, cost


# -------------------------------
# Draw Graph
# -------------------------------
def draw_graph(edges, mst_edges, title):
    G = nx.Graph()

    for w, u, v in edges:
        G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G, seed=42)

    fig, ax = plt.subplots(figsize=(8, 6))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=800,
        font_size=10,
        ax=ax
    )

    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    mst_set = {(u, v) for u, v, w in mst_edges}
    mst_set.update({(v, u) for u, v, w in mst_edges})

    mst_graph_edges = [
        (u, v)
        for u, v in G.edges()
        if (u, v) in mst_set
    ]

    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=mst_graph_edges,
        width=4
    )

    ax.set_title(title)

    return fig


# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="MST Visualizer", layout="wide")

st.title("🌳 Minimum Spanning Tree Visualizer")
st.subheader("Kruskal's Algorithm and Prim's Algorithm")

# Graph Data
n = 7

edges = [
    (7, 0, 1),
    (5, 0, 3),
    (8, 1, 2),
    (9, 1, 3),
    (7, 1, 4),
    (5, 2, 4),
    (15, 3, 4),
    (6, 3, 5),
    (8, 4, 5),
    (9, 4, 6),
    (11, 5, 6)
]

# Build adjacency list
adj = {}

for w, u, v in edges:
    adj.setdefault(u, []).append((v, w))
    adj.setdefault(v, []).append((u, w))

algorithm = st.selectbox(
    "Choose Algorithm",
    ["Kruskal", "Prim"]
)

if st.button("Generate MST"):

    if algorithm == "Kruskal":
        mst, cost = kruskal(n, edges)

        st.success(f"Total MST Cost = {cost}")

        st.write("### MST Edges")

        for u, v, w in mst:
            st.write(f"({u} - {v}) → Weight = {w}")

        fig = draw_graph(
            edges,
            mst,
            "Kruskal MST"
        )

        st.pyplot(fig)

    else:
        mst, cost = prim(n, adj)

        st.success(f"Total MST Cost = {cost}")

        st.write("### MST Edges")

        for u, v, w in mst:
            st.write(f"({u} - {v}) → Weight = {w}")

        fig = draw_graph(
            edges,
            mst,
            "Prim MST"
        )

        st.pyplot(fig)