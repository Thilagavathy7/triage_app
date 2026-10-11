# heap.py - Min-Heap built from scratch (no heapq) for the triage system

class MinHeap:
    def __init__(self):
        self.data = []                      # the heap is stored in a plain list

    def size(self):
        return len(self.data)               # number of patients waiting

    def is_empty(self):
        return len(self.data) == 0          # True when nobody is waiting

    def peek(self):
        if self.is_empty():                 # nothing to look at
            return None
        return self.data[0]                 # root = most urgent patient

    def push(self, item):
        self.data.append(item)              # 1. add at the end (next free slot)
        self._sift_up(len(self.data) - 1)   # 2. move it up to its correct place

    def pop(self):
        if self.is_empty():                 # nothing to remove
            return None
        top = self.data[0]                  # 1. remember the most urgent patient
        last = self.data.pop()              # 2. remove the last item from the list
        if self.data:                       # 3. if the heap is not empty now...
            self.data[0] = last             #    put the last item at the root
            self._sift_down(0)              # 4. push it down to its correct place
        return top                          # 5. return the treated patient

    def _sift_up(self, i):
        while i > 0:                        # stop when we reach the root
            parent = (i - 1) // 2           # index of the parent node
            if self.data[i] < self.data[parent]:   # child more urgent than parent?
                self.data[i], self.data[parent] = self.data[parent], self.data[i]  # swap
                i = parent                  # continue from the parent's position
            else:
                break                       # heap rule satisfied, stop

    def _sift_down(self, i):
        n = len(self.data)
        while True:
            left = 2 * i + 1                # left child index
            right = 2 * i + 2               # right child index
            smallest = i                    # assume current node is the smallest
            if left < n and self.data[left] < self.data[smallest]:
                smallest = left             # left child is more urgent
            if right < n and self.data[right] < self.data[smallest]:
                smallest = right            # right child is more urgent
            if smallest == i:               # node is already in the right place
                break
            self.data[i], self.data[smallest] = self.data[smallest], self.data[i]  # swap
            i = smallest                    # continue from the child's position

    def sorted_view(self):
        copy = MinHeap()                    # work on a copy so the real heap is untouched
        copy.data = self.data[:]
        result = []
        while not copy.is_empty():
            result.append(copy.pop())       # popping repeatedly gives sorted order
        return result
