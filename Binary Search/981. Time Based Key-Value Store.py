"""
Problem Number: 981
Title: Time Based Key-Value Store
Difficulty: Medium
Topics: Hash Table, String, Binary Search, Design

Problem Statement:
Design a time-based key-value data structure that can store multiple values for the same key
at different time stamps and retrieve the key's value at a certain timestamp.

Implement the TimeMap class:
    - TimeMap() Initializes the object of the data structure.
    - void set(String key, String value, int timestamp) Stores the key with the value value
      at the given time timestamp.
    - String get(String key, int timestamp) Returns a value such that set was called previously,
      with timestamp_prev <= timestamp. If there are multiple such values, it returns the value
      associated with the largest timestamp_prev. If there are no values, it returns "".

Examples:
    Input:
        ["TimeMap", "set", "get", "get", "set", "get", "get"]
        [[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]]
    Output:
        [null, null, "bar", "bar", null, "bar2", "bar2"]

Constraints:
    1 <= key.length, value.length <= 100
    key and value consist of lowercase English letters and digits.
    1 <= timestamp <= 10^7
    All the timestamps timestamp of set are strictly increasing.
    At most 2 * 10^5 calls will be made to set and get.

Approach:
    Store each key's values as a list of (timestamp, value) pairs. Since set() is always called
    with strictly increasing timestamps, this list is naturally sorted by timestamp.

    For get(key, timestamp): binary search the list for the largest timestamp <= the query
    timestamp. Use bisect_right to find the insertion point for timestamp, then step back one.
    If the index is 0, no valid entry exists -> return "".

Complexity:
    Time:  set O(1), get O(log n) where n = number of set calls for that key
    Space: O(n) total across all set calls
"""

import bisect
from collections import defaultdict


class TimeMap:
    def __init__(self):
        # key -> list of (timestamp, value), always sorted by timestamp
        self.store: dict[str, list[tuple[int, str]]] = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        entries = self.store.get(key, [])
        if not entries:
            return ""
        # Find rightmost timestamp <= query timestamp
        # bisect_right on timestamps: search in a list of (ts, val) tuples
        # We extract timestamps for bisect
        timestamps = [ts for ts, _ in entries]
        idx = bisect.bisect_right(timestamps, timestamp)
        if idx == 0:
            return ""
        return entries[idx - 1][1]


if __name__ == "__main__":
    # Example from problem
    tm = TimeMap()
    tm.set("foo", "bar", 1)
    assert tm.get("foo", 1) == "bar"
    assert tm.get("foo", 3) == "bar"   # no entry at t=3, return t=1 value
    tm.set("foo", "bar2", 4)
    assert tm.get("foo", 4) == "bar2"
    assert tm.get("foo", 5) == "bar2"  # latest <= 5 is t=4

    # Edge: timestamp before any set
    tm2 = TimeMap()
    tm2.set("a", "val", 5)
    assert tm2.get("a", 3) == ""   # no entry at or before t=3
    assert tm2.get("a", 5) == "val"
    assert tm2.get("a", 10) == "val"

    # Edge: key not set
    tm3 = TimeMap()
    assert tm3.get("missing", 1) == ""

    # Multiple keys independent
    tm4 = TimeMap()
    tm4.set("x", "a", 1)
    tm4.set("y", "b", 2)
    assert tm4.get("x", 2) == "a"
    assert tm4.get("y", 1) == ""
    assert tm4.get("y", 2) == "b"

    print("All tests passed!")
