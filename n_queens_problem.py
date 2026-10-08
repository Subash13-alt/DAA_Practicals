import streamlit as st

# -----------------------------
# Check if Queen Placement is Safe
# -----------------------------
def is_safe(board, row, col):
    for prev_row in range(row):
        placed = board[prev_row]

        # Same column
        if placed == col:
            return False

        # Diagonal
        if abs(prev_row - row) == abs(placed - col):
            return False

    return True


# -----------------------------
# Solve N-Queens
# -----------------------------
def solve_n_queens(n):
    board = [-1] * n
    solutions = []
    backtrack_count = [0]

    def backtrack(row):
        if row == n:
            solutions.append(board[:])
            return

        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1
                backtrack_count[0] += 1

    backtrack(0)

    return solutions, backtrack_count[0]


# -----------------------------
# Convert Board to Display Format
# -----------------------------
def board_to_table(solution, n):
    board = []

    for row in range(n):
        current = []
        for col in range(n):
            if solution[row] == col:
                current.append("♛")
            else:
                current.append("·")
        board.append(current)

    return board


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="N-Queens Problem",
    page_icon="♛"
)

st.title("♛ N-Queens Problem using Backtracking")

st.write(
    "Solve the N-Queens problem using the Backtracking algorithm."
)

n = st.slider(
    "Select the value of N",
    min_value=4,
    max_value=10,
    value=4
)

if st.button("Solve"):

    solutions, backtracks = solve_n_queens(n)

    st.success("Computation Completed!")

    st.subheader("Results")

    st.write(f"**Board Size:** {n} × {n}")
    st.write(f"**Number of Solutions:** {len(solutions)}")
    st.write(f"**Backtracks:** {backtracks}")

    if n <= 6:
        st.subheader("Solutions")

        for i, solution in enumerate(solutions, start=1):
            st.write(f"### Solution {i}")

            board = board_to_table(solution, n)

            st.table(board)

            st.write(f"Position Representation: {solution}")