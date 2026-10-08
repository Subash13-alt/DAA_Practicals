import streamlit as st
import heapq

# -----------------------------
# Dijkstra Algorithm
# -----------------------------
def dijkstra(graph, source):
    n = len(graph)
    dist = [float('inf')] * n
    prev = [None] * n
    dist[source] = 0

    pq = [(0, source)]  # (distance, vertex)
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)

        if u in visited:
            continue

        visited.add(u)

        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, prev


# -----------------------------
# Reconstruct Path
# -----------------------------
def reconstruct_path(prev, source, target):
    path = []
    node = target

    while node is not None:
        path.append(node)
        node = prev[node]

    path.reverse()

    if path and path[0] == source:
        return path
    return []


# -----------------------------
# Graph Definition
# -----------------------------
graph = {
    0: [(1, 4), (2, 1)],
    1: [(3, 1)],
    2: [(1, 2), (3, 5)],
    3: [(4, 3)],
    4: [(5, 2)],
    5: []
}


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Dijkstra Algorithm", page_icon="🛣️")

st.title("🛣️ Dijkstra's Shortest Path Algorithm")

st.write("Find the shortest path from a selected source vertex.")

st.subheader("Graph")

st.code(graph, language="python")

source = st.selectbox(
    "Select Source Vertex",
    list(graph.keys())
)

if st.button("Find Shortest Paths"):

    dist, prev = dijkstra(graph, source)

    st.subheader(f"Shortest Paths from Vertex {source}")

    results = []

    for v in range(len(graph)):
        path = reconstruct_path(prev, source, v)

        if path:
            path_str = " → ".join(map(str, path))
        else:
            path_str = "No Path"

        distance = dist[v] if dist[v] != float("inf") else "INF"

        results.append({
            "Vertex": v,
            "Distance": distance,
            "Path": path_str
        })

    st.table(results)

    st.success("Computation Completed!")