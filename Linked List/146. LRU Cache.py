"""
146. LRU Cache
Difficulty: Medium
Topics: Linked List, Hash Table, Design, Doubly Linked List

Problem Statement:
Design a data structure that follows the constraints of a Least Recently
Used (LRU) cache.

Implement the LRUCache class:
- LRUCache(int capacity) initializes the LRU cache with positive size
  capacity.
- int get(int key) returns the value of the key if the key exists,
  otherwise returns -1.
- void put(int key, int value) updates the value of the key if the key
  exists. Otherwise, adds the key-value pair to the cache. If the number
  of keys exceeds the capacity from this operation, evict the least
  recently used key.

The functions get and put must each run in O(1) average time complexity.

Example:
Input:
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
Output:
[null, null, null, 1, null, -1, null, -1, 3, 4]

Explanation:
LRUCache lRUCache = new LRUCache(2);
lRUCache.put(1, 1); // cache is {1=1}
lRUCache.put(2, 2); // cache is {1=1, 2=2}
lRUCache.get(1);    // return 1
lRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
lRUCache.get(2);    // returns -1 (not found)
lRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}
lRUCache.get(1);    // return -1 (not found)
lRUCache.get(3);    // return 3
lRUCache.get(4);    // return 4

Constraints:
- 1 <= capacity <= 3000
- 0 <= key <= 10^4
- 0 <= value <= 10^5
- At most 2 * 10^5 calls will be made to get and put.

Approach:
Use a hash map for O(1) key lookup combined with a doubly linked list to
maintain usage order. The doubly linked list keeps the most recently used
node near the "head" and the least recently used node near the "tail".
Two sentinel nodes (head and tail) simplify insert/remove logic by
removing edge cases at the boundaries.

- get(key): if the key exists, move its node to the front (most recently
  used position) and return its value; otherwise return -1.
- put(key, value): if the key exists, update its value and move it to the
  front. Otherwise create a new node, insert it at the front, and if
  capacity is exceeded, remove the node just before the tail sentinel
  (the least recently used node) along with its hash map entry.

Because the hash map stores direct references to linked list nodes,
removal and insertion at any position take O(1) time — no need to
traverse the list to find a node.

Why it works:
The doubly linked list preserves relative recency ordering while
allowing O(1) removal/insertion at arbitrary points (given a node
reference), and the hash map avoids linear-time search for a given key.
Together they satisfy the O(1) average-time requirement for both
operations.

Complexity:
- Time: O(1) average for both get and put.
- Space: O(capacity) for the hash map and linked list nodes.

Alternative approach:
Python's collections.OrderedDict provides move_to_end() and popitem()
which internally use a similar doubly linked list + hash map structure.
This yields a much shorter implementation with the same O(1) guarantees,
shown below as LRUCacheOrderedDict.
"""

from collections import OrderedDict


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: dict[int, _Node] = {}

        # Sentinel head/tail nodes to avoid null checks at boundaries.
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: "_Node") -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_at_front(self, node: "_Node") -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._insert_at_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._insert_at_front(node)
            return

        if len(self.cache) >= self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]

        node = _Node(key, value)
        self.cache[key] = node
        self._insert_at_front(node)


class LRUCacheOrderedDict:
    """Alternative implementation using OrderedDict."""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.od: "OrderedDict[int, int]" = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.od:
            return -1
        self.od.move_to_end(key)
        return self.od[key]

    def put(self, key: int, value: int) -> None:
        if key in self.od:
            self.od.move_to_end(key)
        self.od[key] = value
        if len(self.od) > self.capacity:
            self.od.popitem(last=False)


if __name__ == "__main__":
    for Impl in (LRUCache, LRUCacheOrderedDict):
        cache = Impl(2)
        cache.put(1, 1)
        cache.put(2, 2)
        assert cache.get(1) == 1
        cache.put(3, 3)  # evicts key 2
        assert cache.get(2) == -1
        cache.put(4, 4)  # evicts key 1
        assert cache.get(1) == -1
        assert cache.get(3) == 3
        assert cache.get(4) == 4

        # Capacity of 1.
        c1 = Impl(1)
        c1.put(1, 10)
        assert c1.get(1) == 10
        c1.put(2, 20)  # evicts key 1
        assert c1.get(1) == -1
        assert c1.get(2) == 20

        # Updating an existing key should refresh recency, not evict it.
        c2 = Impl(2)
        c2.put(1, 1)
        c2.put(2, 2)
        c2.put(1, 10)  # key 1 is now most recently used
        c2.put(3, 3)  # should evict key 2, not key 1
        assert c2.get(2) == -1
        assert c2.get(1) == 10
        assert c2.get(3) == 3

        # get on missing key.
        c3 = Impl(2)
        assert c3.get(5) == -1

    print("All LRU Cache tests passed.")
