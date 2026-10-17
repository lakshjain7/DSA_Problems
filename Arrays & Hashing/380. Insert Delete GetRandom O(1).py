"""
380. Insert Delete GetRandom O(1)
Difficulty: Medium
Topics: Array, Hash Table, Math, Design, Randomized

Problem Statement:
Implement the RandomizedSet class:
- RandomizedSet() Initializes the RandomizedSet object.
- bool insert(int val) Inserts val if not present. Returns true if the item
  was not present, false otherwise.
- bool remove(int val) Removes val if present. Returns true if the item was
  present, false otherwise.
- int getRandom() Returns a random element from the current set. Each element
  must have the same probability of being returned.
You must implement the functions so that each works in average O(1) time.

Example 1:
    ["RandomizedSet","insert","remove","insert","getRandom","remove","insert","getRandom"]
    [[],[1],[2],[2],[],[1],[2],[]]
    Output: [null,true,false,true,2,true,false,2]

Constraints:
- -2^31 <= val <= 2^31 - 1
- At most 2 * 10^5 calls to insert, remove, and getRandom.
- There will be at least one element when getRandom is called.

Approach:
Keep a dynamic array `vals` (for O(1) random index) and a dict `pos` mapping
value -> index in the array. Insert appends. Remove is the trick: deleting from
the middle of an array is O(n), so swap the element with the last one, update
the moved element's index in the dict, then pop the tail. getRandom picks a
uniform random index.

Complexity:
Time: O(1) average per operation. Space: O(n).

Alternative approach:
A plain set with random.choice(tuple(set)) gives O(n) getRandom -> too slow.
"""
import random
from typing import Dict, List


class RandomizedSet:
    def __init__(self) -> None:
        self.vals: List[int] = []
        self.pos: Dict[int, int] = {}

    def insert(self, val: int) -> bool:
        if val in self.pos:
            return False
        self.pos[val] = len(self.vals)
        self.vals.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.pos:
            return False
        i = self.pos[val]
        last = self.vals[-1]
        self.vals[i] = last
        self.pos[last] = i
        self.vals.pop()
        del self.pos[val]
        return True

    def getRandom(self) -> int:
        return random.choice(self.vals)


if __name__ == "__main__":
    s = RandomizedSet()
    assert s.insert(1) is True
    assert s.remove(2) is False
    assert s.insert(2) is True
    assert s.getRandom() in (1, 2)
    assert s.remove(1) is True
    assert s.insert(2) is False
    assert s.getRandom() == 2
    # remove last element / only element
    assert s.remove(2) is True
    assert s.remove(2) is False
    assert s.insert(2) is True
    # removing last-position element and swapping middle
    t = RandomizedSet()
    for v in (10, 20, 30, 40):
        assert t.insert(v)
    assert t.remove(20) and t.remove(40)
    assert sorted(t.vals) == [10, 30]
    assert all(t.vals[t.pos[v]] == v for v in t.pos)
    # negative values and distribution sanity
    u = RandomizedSet()
    for v in (-1, 0, 1):
        u.insert(v)
    seen = {u.getRandom() for _ in range(200)}
    assert seen == {-1, 0, 1}
    print("All tests passed.")
