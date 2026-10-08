import streamlit as st
import random

# -----------------------------
# Divide and Conquer Min-Max
# -----------------------------
comparison_count = 0

def min_max_dc(arr, low, high):
    global comparison_count

    # Base case: One element
    if low == high:
        return arr[low], arr[low]

    # Base case: Two elements
    if high == low + 1:
        comparison_count += 1
        if arr[low] < arr[high]:
            return arr[low], arr[high]
        else:
            return arr[high], arr[low]

    # Divide
    mid = (low + high) // 2

    lmin, lmax = min_max_dc(arr, low, mid)
    rmin, rmax = min_max_dc(arr, mid + 1, high)

    # Combine
    comparison_count += 1
    overall_min = lmin if lmin < rmin else rmin

    comparison_count += 1
    overall_max = lmax if lmax > rmax else rmax

    return overall_min, overall_max


# -----------------------------
# Naive Method
# -----------------------------
def min_max_naive(arr):
    mn = mx = arr[0]
    comps = 0

    for x in arr[1:]:
        comps += 1
        if x < mn:
            mn = x

        comps += 1
        if x > mx:
            mx = x

    return mn, mx, comps


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Min-Max Divide & Conquer", page_icon="📊")

st.title("📊 Min-Max using Divide & Conquer")

st.write(
    "Find the minimum and maximum values in an array using the Divide & Conquer technique and compare it with the Naive approach."
)

option = st.radio(
    "Choose Input Method",
    ["Generate Random Array", "Enter Your Own Array"]
)

if option == "Generate Random Array":
    size = st.slider("Array Size", 5, 30, 10)
    arr = [random.randint(1, 100) for _ in range(size)]
else:
    user_input = st.text_input(
        "Enter numbers separated by commas",
        "3,1,7,4,9,2,8,5,6,0"
    )

    try:
        arr = [int(x.strip()) for x in user_input.split(",")]
    except:
        st.error("Please enter valid integers.")
        st.stop()

st.subheader("Input Array")
st.write(arr)

if st.button("Find Min & Max"):

    comparison_count = 0
    mn, mx = min_max_dc(arr, 0, len(arr)-1)
    dc_comps = comparison_count

    _, _, naive_comps = min_max_naive(arr)

    st.subheader("Results")

    st.table([
        {"Method": "Divide & Conquer", "Minimum": mn, "Maximum": mx, "Comparisons": dc_comps},
        {"Method": "Naive", "Minimum": mn, "Maximum": mx, "Comparisons": naive_comps}
    ])

    st.success("Computation Completed!")

st.markdown("---")

st.subheader("Performance Analysis")

sizes = [10, 100, 1000, 10000]
performance = []

for size in sizes:
    arr = [random.randint(1, 10000) for _ in range(size)]

    comparison_count = 0
    min_max_dc(arr, 0, len(arr)-1)
    dc = comparison_count

    _, _, naive = min_max_naive(arr)

    formula = 3 * size // 2 - 2

    performance.append({
        "Size": size,
        "D&C Comparisons": dc,
        "Naive Comparisons": naive,
        "Formula (3n/2 - 2)": formula
    })

st.table(performance)