import streamlit as st
from itertools import permutations

INF = float("inf")

# -----------------------------
# Brute Force TSP
# -----------------------------
def tsp_brute_force(cost, n):
    cities = list(range(1, n))

    best_cost = INF
    best_path = None

    for perm in permutations(cities):
        path = [0] + list(perm) + [0]

        current_cost = 0
        for i in range(n):
            current_cost += cost[path[i]][path[i + 1]]

        if current_cost < best_cost:
            best_cost = current_cost
            best_path = path

    return best_path, best_cost


# -----------------------------
# Cost Matrix
# -----------------------------
cost = [
    [INF, 10, 8, 9, 7],
    [10, INF, 10, 5, 6],
    [8, 10, INF, 8, 9],
    [9, 5, 8, INF, 6],
    [7, 6, 9, 6, INF]
]

cities = ["A", "B", "C", "D", "E"]
n = len(cost)

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="Travelling Salesman Problem",
    page_icon="🚗"
)

st.title("🚗 Travelling Salesman Problem (TSP)")

st.write(
    "Find the optimal tour using the Brute Force approach."
)

st.subheader("Cost Matrix")

table = []

for i in range(n):
    row = {"City": cities[i]}
    for j in range(n):
        if cost[i][j] == INF:
            row[cities[j]] = "INF"
        else:
            row[cities[j]] = cost[i][j]
    table.append(row)

st.table(table)

if st.button("Find Optimal Tour"):

    best_path, best_cost = tsp_brute_force(cost, n)

    st.success("Computation Completed!")

    st.subheader("Optimal Tour")

    path = " → ".join(cities[i] for i in best_path)

    st.write(f"**Tour:** {path}")
    st.write(f"**Minimum Cost:** {best_cost}")

    st.subheader("Path Verification")

    verify = []

    for i in range(n):
        u = best_path[i]
        v = best_path[i + 1]

        verify.append({
            "From": cities[u],
            "To": cities[v],
            "Cost": cost[u][v]
        })

    st.table(verify)