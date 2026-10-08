import streamlit as st
import math

# -----------------------------
# First Fit
# -----------------------------
def first_fit(items, capacity=1.0):
    bins = []
    bin_contents = []

    for item in items:
        placed = False

        for i, space in enumerate(bins):
            if space >= item:
                bins[i] -= item
                bin_contents[i].append(item)
                placed = True
                break

        if not placed:
            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


# -----------------------------
# First Fit Decreasing
# -----------------------------
def first_fit_decreasing(items, capacity=1.0):
    return first_fit(sorted(items, reverse=True), capacity)


# -----------------------------
# Best Fit Decreasing
# -----------------------------
def best_fit_decreasing(items, capacity=1.0):
    items = sorted(items, reverse=True)

    bins = []
    bin_contents = []

    for item in items:

        best_idx = -1
        best_space = float("inf")

        for i, space in enumerate(bins):
            if space >= item and (space - item) < best_space:
                best_space = space - item
                best_idx = i

        if best_idx != -1:
            bins[best_idx] -= item
            bin_contents[best_idx].append(item)
        else:
            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="Bin Packing Problem",
    page_icon="📦"
)

st.title("📦 Bin Packing Problem")

st.write(
    "Compare First Fit (FF), First Fit Decreasing (FFD), and Best Fit Decreasing (BFD) algorithms."
)

items_input = st.text_input(
    "Enter item sizes (comma separated)",
    "0.5,0.7,0.3,0.9,0.2,0.6,0.8,0.4,0.1,0.5"
)

capacity = st.number_input(
    "Bin Capacity",
    value=1.0,
    min_value=0.1,
    step=0.1
)

try:
    items = [float(x.strip()) for x in items_input.split(",")]
except:
    st.error("Please enter valid decimal values.")
    st.stop()

if st.button("Run Algorithms"):

    lower_bound = math.ceil(sum(items) / capacity)

    ff = first_fit(items, capacity)
    ffd = first_fit_decreasing(items, capacity)
    bfd = best_fit_decreasing(items, capacity)

    st.subheader("Input Details")

    st.write(f"**Items:** {items}")
    st.write(f"**Capacity:** {capacity}")
    st.write(f"**Total Item Size:** {sum(items):.2f}")
    st.write(f"**Lower Bound on Bins:** {lower_bound}")

    def show_bins(title, bins):
        st.subheader(title)

        table = []

        for i, b in enumerate(bins, start=1):
            table.append({
                "Bin": i,
                "Items": b,
                "Used Space": round(sum(b), 2),
                "Remaining": round(capacity - sum(b), 2)
            })

        st.table(table)

    show_bins("First Fit (FF)", ff)
    show_bins("First Fit Decreasing (FFD)", ffd)
    show_bins("Best Fit Decreasing (BFD)", bfd)

    st.subheader("Summary")

    st.table([
        {
            "Algorithm": "Lower Bound",
            "Bins Used": lower_bound
        },
        {
            "Algorithm": "First Fit",
            "Bins Used": len(ff)
        },
        {
            "Algorithm": "First Fit Decreasing",
            "Bins Used": len(ffd)
        },
        {
            "Algorithm": "Best Fit Decreasing",
            "Bins Used": len(bfd)
        }
    ])

    st.success("Computation Completed!")