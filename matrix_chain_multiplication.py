import streamlit as st

# -----------------------------
# Matrix Chain Multiplication
# -----------------------------
def matrix_chain_order(dims):
    n = len(dims) - 1

    # Cost table
    m = [[0] * (n + 1) for _ in range(n + 1)]

    # Split table
    s = [[0] * (n + 1) for _ in range(n + 1)]

    # Chain length
    for l in range(2, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1
            m[i][j] = float("inf")

            for k in range(i, j):
                cost = (
                    m[i][k]
                    + m[k + 1][j]
                    + dims[i - 1] * dims[k] * dims[j]
                )

                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k

    return m, s


# -----------------------------
# Print Parenthesization
# -----------------------------
def print_optimal_parens(s, i, j):
    if i == j:
        return f"A{i}"

    k = s[i][j]

    left = print_optimal_parens(s, i, k)
    right = print_optimal_parens(s, k + 1, j)

    return f"({left} × {right})"


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="Matrix Chain Multiplication",
    page_icon="🧮"
)

st.title("🧮 Matrix Chain Multiplication")

st.write(
    "Find the minimum number of scalar multiplications using Dynamic Programming."
)

st.subheader("Enter Matrix Dimensions")

st.write(
    "Example: For matrices A1(10×30), A2(30×5), A3(5×60), A4(60×10), enter:"
)

dims_input = st.text_input(
    "Dimensions",
    "10,30,5,60,10"
)

try:
    dims = [int(x.strip()) for x in dims_input.split(",")]

    if len(dims) < 2:
        st.error("Enter at least two dimensions.")
        st.stop()

except:
    st.error("Please enter valid integers separated by commas.")
    st.stop()

n = len(dims) - 1

st.subheader("Matrices")

for i in range(n):
    st.write(f"**A{i+1}** : {dims[i]} × {dims[i+1]}")

if st.button("Compute"):

    m, s = matrix_chain_order(dims)

    st.success("Computation Completed!")

    st.subheader("Results")

    st.write(
        f"**Minimum Scalar Multiplications:** {m[1][n]}"
    )

    st.write(
        f"**Optimal Parenthesization:** {print_optimal_parens(s,1,n)}"
    )

    st.subheader("DP Cost Table")

    table = []

    for i in range(1, n + 1):

        row = {"Matrix": f"A{i}"}

        for j in range(1, n + 1):

            if j < i:
                row[f"A{j}"] = "---"
            else:
                row[f"A{j}"] = m[i][j]

        table.append(row)

    st.table(table)