import streamlit as st
import random
import time
import sys

sys.setrecursionlimit(20000)

comparisons = 0

# -----------------------------
# Partition Function
# -----------------------------
def partition(arr, low, high):
    global comparisons

    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        comparisons += 1

        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]

    return i + 1


# -----------------------------
# Deterministic Quick Sort
# -----------------------------
def deterministic_quicksort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)

        deterministic_quicksort(arr, low, pi - 1)
        deterministic_quicksort(arr, pi + 1, high)


# -----------------------------
# Randomized Quick Sort
# -----------------------------
def randomized_quicksort(arr, low, high):
    if low < high:

        rand_index = random.randint(low, high)
        arr[rand_index], arr[high] = arr[high], arr[rand_index]

        pi = partition(arr, low, high)

        randomized_quicksort(arr, low, pi - 1)
        randomized_quicksort(arr, pi + 1, high)


# -----------------------------
# Run Experiment
# -----------------------------
def run_test(sort_function, arr):
    global comparisons

    data = arr.copy()

    comparisons = 0

    start = time.perf_counter()

    sort_function(data, 0, len(data) - 1)

    elapsed = (time.perf_counter() - start) * 1000

    return comparisons, elapsed


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="Randomized Quick Sort",
    page_icon="⚡"
)

st.title("⚡ Randomized Quick Sort Performance")

st.write(
    "Compare Deterministic Quick Sort (DQS) and Randomized Quick Sort (RQS) using different input datasets."
)

N = st.slider(
    "Array Size",
    100,
    5000,
    1000,
    step=100
)

if st.button("Run Comparison"):

    test_cases = {
        "Random": [random.randint(1, 100000) for _ in range(N)],
        "Sorted": list(range(N)),
        "Reverse": list(range(N, 0, -1)),
        "Nearly Sorted": list(range(N))
    }

    # Slight shuffle
    nearly = test_cases["Nearly Sorted"]

    for _ in range(N // 20):
        i = random.randint(0, N - 1)
        j = random.randint(0, N - 1)
        nearly[i], nearly[j] = nearly[j], nearly[i]

    results = []

    for case, arr in test_cases.items():

        d_comp, d_time = run_test(deterministic_quicksort, arr)
        r_comp, r_time = run_test(randomized_quicksort, arr)

        results.append({
            "Input Type": case,
            "DQS Comparisons": d_comp,
            "DQS Time (ms)": round(d_time, 2),
            "RQS Comparisons": r_comp,
            "RQS Time (ms)": round(r_time, 2)
        })

    st.success("Experiment Completed!")

    st.subheader("Performance Comparison")

    st.table(results)