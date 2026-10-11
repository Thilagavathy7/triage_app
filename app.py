# app.py - Hospital Emergency Triage System (Streamlit UI)
import streamlit as st
from datetime import datetime
from heap import MinHeap

SEVERITY = {1: "1 - Critical", 2: "2 - Emergency", 3: "3 - Urgent",
            4: "4 - Less urgent", 5: "5 - Non-urgent"}

st.set_page_config(page_title="ER Triage (Heap)", page_icon="🏥", layout="wide")

# Streamlit reruns the script on every click, so we keep data in session_state
if "heap" not in st.session_state:
    st.session_state.heap = MinHeap()       # the priority queue
    st.session_state.counter = 0            # arrival number (tie-breaker)
    st.session_state.treated = []           # history of treated patients

heap = st.session_state.heap

st.title("🏥 Hospital Emergency Triage System")
st.caption("Data structure used: Min-Heap (Priority Queue) - Python, built from scratch")

# ---------- Sidebar: register a patient ----------
with st.sidebar:
    st.header("Register patient")
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Name")
        age = st.number_input("Age", 0, 120, 30)
        complaint = st.text_input("Complaint (e.g. chest pain)")
        level = st.selectbox("Severity", list(SEVERITY), format_func=lambda k: SEVERITY[k])
        submitted = st.form_submit_button("Add to queue")
    if submitted and name.strip():
        st.session_state.counter += 1
        patient = (level, st.session_state.counter, name.strip(), age,
                   complaint, datetime.now().strftime("%H:%M:%S"))
        heap.push(patient)                  # O(log n)
        st.success(f"{name} added")
    if st.button("Load demo patients"):
        demo = [(3, "Ravi", 34, "Fracture"), (5, "Meena", 22, "Mild cold"),
                (1, "Arun", 58, "Heart attack"), (2, "Divya", 41, "Severe bleeding"),
                (4, "Karthik", 29, "Sprain")]
        for lvl, n, a, c in demo:
            st.session_state.counter += 1
            heap.push((lvl, st.session_state.counter, n, a, c,
                       datetime.now().strftime("%H:%M:%S")))
        st.rerun()
    if st.button("Reset everything"):
        st.session_state.clear()
        st.rerun()

tab1, tab2, tab3 = st.tabs(["Dashboard", "Inside the heap", "How it works"])

# ---------- Tab 1: dashboard ----------
with tab1:
    c1, c2, c3 = st.columns(3)
    c1.metric("Waiting", heap.size())
    c2.metric("Treated", len(st.session_state.treated))
    nxt = heap.peek()                       # O(1)
    c3.metric("Next patient", nxt[2] if nxt else "-")

    if st.button("🩺 Treat next patient", type="primary", disabled=heap.is_empty()):
        st.session_state.treated.append(heap.pop())   # O(log n)
        st.rerun()

    st.subheader("Waiting queue (most urgent first)")
    rows = [{"Name": p[2], "Age": p[3], "Complaint": p[4],
             "Severity": SEVERITY[p[0]], "Arrival #": p[1], "Arrived": p[5]}
            for p in heap.sorted_view()]
    if rows:
        st.dataframe(rows, use_container_width=True)
    else:
        st.info("Queue is empty.")

    st.subheader("Treated patients")
    done = [{"Order": i + 1, "Name": p[2], "Severity": SEVERITY[p[0]]}
            for i, p in enumerate(st.session_state.treated)]
    if done:
        st.dataframe(done, use_container_width=True)
    else:
        st.write("None yet.")

# ---------- Tab 2: show the raw heap array ----------
with tab2:
    st.write("The heap is stored as a **list**. For index `i`: parent = `(i-1)//2`, "
             "left child = `2i+1`, right child = `2i+2`.")
    internals = [{"Index": i, "Name": p[2], "Severity": p[0], "Arrival #": p[1],
                  "Parent index": str((i - 1) // 2) if i else "-"}
                 for i, p in enumerate(heap.data)]
    if internals:
        st.dataframe(internals, use_container_width=True)
    else:
        st.info("Heap is empty.")
    st.caption("Notice: index 0 (the root) is always the most urgent patient. "
               "The rest is only partially ordered - that is what makes a heap fast.")

# ---------- Tab 3: short explanation ----------
with tab3:
    st.markdown("""
**Why a heap?** A normal queue is first-come-first-served. In an ER the *most critical* patient must go first.
A min-heap always keeps the smallest `(severity, arrival_no)` tuple at the root.

| Operation | Time |
|---|---|
| Add patient (`push`) | O(log n) |
| See next patient (`peek`) | O(1) |
| Treat next patient (`pop`) | O(log n) |

**Tie-break:** two patients with the same severity are compared by arrival number, so the earlier one goes first.

See `EXPLANATION.md` for the full line-by-line explanation.
""")
