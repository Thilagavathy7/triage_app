# Hospital Emergency Triage System - Using a Min-Heap (Priority Queue)

## 1. Problem
A normal queue serves people first-come-first-served. In an emergency room, a heart-attack patient who arrives
late must be treated before someone with a mild cold who arrived earlier. We need a structure that always gives
us the **most urgent** patient quickly. That structure is a **priority queue**, implemented with a **min-heap**.

## 2. What is a min-heap?
- A **complete binary tree** where every parent is **smaller than or equal to** its children.
- So the smallest value is always at the top (the root).
- We store the tree in a plain Python list, with no node objects:

| For index i | Formula |
|---|---|
| Parent | (i - 1) // 2 |
| Left child | 2*i + 1 |
| Right child | 2*i + 2 |

Each patient is a tuple `(severity, arrival_no, name, age, complaint, time)`.
Python compares tuples left to right: first severity (1 = most critical), then arrival_no for ties.

## 3. Line-by-line: `heap.py`

```python
class MinHeap:
```
Defines the class that holds all heap operations.

```python
    def __init__(self):
        self.data = []
```
The constructor runs when we write `MinHeap()`. `self.data` is an empty list that will store the heap.

```python
    def size(self):
        return len(self.data)
    def is_empty(self):
        return len(self.data) == 0
```
Helpers: how many patients wait, and whether nobody is waiting.

```python
    def peek(self):
        if self.is_empty():
            return None
        return self.data[0]
```
Look at the most urgent patient without removing them. The root is index 0, so this is **O(1)**.

### push (add a patient)
```python
    def push(self, item):
        self.data.append(item)
        self._sift_up(len(self.data) - 1)
```
1. `append` places the new patient at the end of the list (the next free spot in the tree).
2. That spot may break the heap rule, so `_sift_up` moves the patient upward until the rule holds again.

### _sift_up
```python
    def _sift_up(self, i):
        while i > 0:
```
Keep going until we reach the root (index 0), which has no parent.
```python
            parent = (i - 1) // 2
```
Find the parent's index using the formula.
```python
            if self.data[i] < self.data[parent]:
```
Is the new patient more urgent (smaller tuple) than their parent?
```python
                self.data[i], self.data[parent] = self.data[parent], self.data[i]
                i = parent
```
If yes, swap them and continue checking from the parent's old position.
```python
            else:
                break
```
If no, the heap rule is satisfied, so stop. At most the height of the tree is climbed, so this is **O(log n)**.

### pop (treat the most urgent patient)
```python
    def pop(self):
        if self.is_empty():
            return None
```
Nothing to treat.
```python
        top = self.data[0]
```
Save the root, because this is the patient being treated.
```python
        last = self.data.pop()
```
Remove the last item of the list. (Removing from the end is cheap; removing from the front would shift everything.)
```python
        if self.data:
            self.data[0] = last
            self._sift_down(0)
```
If patients remain, move the last item into the root's place (filling the gap), then push it down to restore order.
```python
        return top
```
Hand back the treated patient. Total cost **O(log n)**.

### _sift_down
```python
    def _sift_down(self, i):
        n = len(self.data)
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            smallest = i
```
Compute the children's indexes and assume the current node is the smallest.
```python
            if left < n and self.data[left] < self.data[smallest]:
                smallest = left
            if right < n and self.data[right] < self.data[smallest]:
                smallest = right
```
`left < n` checks the child exists. Pick whichever of node, left, right is most urgent.
```python
            if smallest == i:
                break
```
The node is already more urgent than both children, so the heap is fixed.
```python
            self.data[i], self.data[smallest] = self.data[smallest], self.data[i]
            i = smallest
```
Otherwise swap with the more urgent child and keep going down.

### sorted_view
```python
    def sorted_view(self):
        copy = MinHeap()
        copy.data = self.data[:]
```
`[:]` makes a copy of the list, so the real queue is not damaged.
```python
        result = []
        while not copy.is_empty():
            result.append(copy.pop())
        return result
```
Popping repeatedly gives patients in priority order. This is used only to display the queue.

## 4. Worked example
Add severities in this order: Ravi(3), Meena(5), Arun(1).

1. push Ravi(3): `[3]`
2. push Meena(5): `[3, 5]` (5 > 3, no swap)
3. push Arun(1): `[3, 5, 1]`, then sift up: 1 < parent 3, swap, giving `[1, 5, 3]`

Now Arun (severity 1) is at the root. `pop()` returns Arun, moves the last item (3) to the root,
and sift down gives `[3, 5]`. Next treated: Ravi, then Meena.

## 5. Complexity
| Operation | Time |
|---|---|
| push | O(log n) |
| pop | O(log n) |
| peek | O(1) |
| sorted_view | O(n log n) |

## 6. Why not a plain list or sorted list?
- Unsorted list: adding is O(1), but finding the most urgent is O(n).
- Sorted list: finding is O(1), but inserting is O(n).
- Heap: both are O(log n), which is the best balance.

## 7. Line-by-line: `app.py` (key parts)
- `st.session_state`: Streamlit re-runs the whole script on every click, so the heap, counter and history are
  stored here to survive reruns.
- `heap.push(patient)`: called when the form is submitted.
- `heap.peek()`: shows the next patient in the metric card.
- `heap.pop()`: called by the "Treat next patient" button.
- `heap.sorted_view()`: builds the waiting-queue table.
- `heap.data`: the raw list shown in the "Inside the heap" tab.

## 8. How to run
```
pip install streamlit
streamlit run app.py
```
Click "Load demo patients", then press "Treat next patient" repeatedly and watch the order follow severity, not arrival.

## 9. Real-world and data science links
Priority queues are used in OS schedulers, Dijkstra's shortest path, Top-K problems, and event-driven simulation.
