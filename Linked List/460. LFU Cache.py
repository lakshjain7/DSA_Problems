"""
460. LFU Cache
Difficulty: Hard
Topics: Hash Table, Linked List, Design, Doubly-Linked List

Problem Statement:
Design and implement a data structure for a Least Frequently Used (LFU)
cache.

Implement the LFUCache class:
    - LFUCache(int capacity) Initializes the object with the capacity of
      the data structure.
    - int get(int key) Gets the value of the key if the key exists in the
      cache. Otherwise, returns -1.
    - void put(int key, int value) Update the value of the key if present,
      or insert the key if not already present. When the cache reaches its
      capacity, it should invalidate and remove the least frequently used
      key before inserting a new item. For this problem, when there is a
      tie (i.e., two or more keys with the same frequency), the least
      recently used key would be invalidated.

To determine the least frequently used key, a use counter is maintained
for each key in the cache. The key with the smallest use counter is the
least frequently used key. When a key is first inserted its use counter
is set to 1 (due to the put operation). The use counter for a key in the
cache is incremented either a get or put operation is called on it.

The functions get and put must each run in O(1) average time complexity.

Example 1:
    Input:
        ["LFUCache","put","put","get","put","get","get","put","get","get","get"]
        [[2],[1,1],[2,2],[1],[3,3],[2],[3],[4,4],[1],[3],[4]]
    Output:
        [null,null,null,1,null,-1,3,null,-1,3,4]

Constraints:
    1 <= capacity <= 10^4
    0 <= key <= 10^5
    0 <= value <= 10^9
    At most 2 * 10^5 calls will be made to get and put.

------------------------------------------------------------------------
Approach: Hash map of keys + hash map of frequency -> ordered bucket
------------------------------------------------------------------------
We need O(1) for both operations, including eviction, so we cannot scan.
Maintain three structures:

    1. node[key]      -> (value, freq)   the payload and current use count.
    2. freq_list[f]   -> an OrderedDict of keys that currently have
                         frequency f, kept in access order. The *first*
                         inserted (front) is the least recently used at
                         that frequency; the last is the most recent.
    3. min_freq       -> the smallest frequency present in the cache, so
                         eviction targets the right bucket in O(1).

get(key):
    - Miss -> return -1.
    - Hit  -> return value and "promote" the key: remove it from
      freq_list[f], append it to freq_list[f+1], bump its freq. If the
      old bucket became empty and it was the min_freq bucket, increment
      min_freq.

put(key, value):
    - capacity 0 -> no-op.
    - Existing key -> overwrite value then promote exactly like get.
    - New key -> if full, evict the front (LRU) of freq_list[min_freq].
      Insert the new key with freq 1 and reset min_freq to 1 (a brand
      new item is always the least frequently used).

Why the tie-break is correct: within a single frequency bucket we keep
keys in an OrderedDict ordered by recency of use. Promotion always
re-appends to the tail, so the front of a bucket is exactly the least
recently used among the least frequently used - which is precisely the
eviction target the problem specifies.

Every step is a constant number of hash lookups / OrderedDict end
operations, so both get and put are O(1).

Complexity:
    Time:  O(1) average per get and put.
    Space: O(capacity) for the stored keys across all structures.
"""

from collections import OrderedDict, defaultdict


class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        # key -> [value, freq]
        self.node = {}
        # freq -> OrderedDict{key: None} in least-recent -> most-recent order
        self.freq_list = defaultdict(OrderedDict)

    def _promote(self, key: int) -> None:
        """Move key from its current frequency bucket to the next."""
        value, freq = self.node[key]
        del self.freq_list[freq][key]
        if not self.freq_list[freq]:
            del self.freq_list[freq]
            if self.min_freq == freq:
                self.min_freq += 1
        self.freq_list[freq + 1][key] = None
        self.node[key] = [value, freq + 1]

    def get(self, key: int) -> int:
        if key not in self.node:
            return -1
        value = self.node[key][0]
        self._promote(key)
        return value

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return

        if key in self.node:
            self.node[key][0] = value
            self._promote(key)
            return

        if len(self.node) >= self.capacity:
            # Evict least-recently-used key in the min frequency bucket.
            evict_key, _ = self.freq_list[self.min_freq].popitem(last=False)
            if not self.freq_list[self.min_freq]:
                del self.freq_list[self.min_freq]
            del self.node[evict_key]

        self.node[key] = [value, 1]
        self.freq_list[1][key] = None
        self.min_freq = 1


if __name__ == "__main__":
    # Example 1 from the problem statement.
    cache = LFUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1        # returns 1
    cache.put(3, 3)                 # evicts key 2 (freq tie -> LRU)
    assert cache.get(2) == -1       # 2 was evicted
    assert cache.get(3) == 3        # returns 3
    cache.put(4, 4)                 # evicts key 1 (freq 2 vs 3's freq 2, 1 is LRU)
    assert cache.get(1) == -1       # 1 was evicted
    assert cache.get(3) == 3        # returns 3
    assert cache.get(4) == 4        # returns 4

    # Capacity 0 -> nothing ever stored.
    c0 = LFUCache(0)
    c0.put(0, 0)
    assert c0.get(0) == -1

    # Overwrite updates value and counts as a use (frequency bump).
    c = LFUCache(2)
    c.put(1, 10)
    c.put(1, 20)                    # overwrite; key 1 now freq 2
    assert c.get(1) == 20
    c.put(2, 30)                    # freq 1
    c.put(3, 40)                    # full -> evict key 2 (lowest freq)
    assert c.get(2) == -1
    assert c.get(1) == 20
    assert c.get(3) == 40

    # Frequency-based eviction over recency: key with higher freq stays.
    c = LFUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1            # key 1 freq 2, key 2 freq 1
    assert c.get(1) == 1            # key 1 freq 3
    c.put(3, 3)                     # evict key 2 (freq 1)
    assert c.get(2) == -1
    assert c.get(1) == 1
    assert c.get(3) == 3

    # Single capacity: every new put evicts the old one.
    c = LFUCache(1)
    c.put(1, 1)
    assert c.get(1) == 1
    c.put(2, 2)
    assert c.get(1) == -1
    assert c.get(2) == 2

    # LRU tie-break among equal frequencies.
    c = LFUCache(3)
    c.put(1, 1)
    c.put(2, 2)
    c.put(3, 3)                     # all freq 1: order [1, 2, 3]
    assert c.get(2) == 2           # 2 -> freq 2; freq-1 bucket order [1, 3]
    c.put(4, 4)                     # evict LRU of freq 1 -> key 1
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4

    print("All tests passed for 460. LFU Cache")
