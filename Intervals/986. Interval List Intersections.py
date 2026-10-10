"""
986. Interval List Intersections
Difficulty: Medium
Topics: Array, Two Pointers

Problem:
You are given two lists of closed intervals, firstList and secondList, where
firstList[i] = [start_i, end_i] and secondList[j] = [start_j, end_j]. Each
list of intervals is pairwise disjoint and in sorted order.
Return the intersection of these two interval lists.
A closed interval [a, b] (a <= b) denotes the set of real numbers x with
a <= x <= b. The intersection of two closed intervals is a set of real
numbers that is either empty or represented as a closed interval.

Example 1:
    Input: firstList = [[0,2],[5,10],[13,23],[24,25]],
           secondList = [[1,5],[8,12],[15,24],[25,26]]
    Output: [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]
Example 2:
    Input: firstList = [[1,3],[5,9]], secondList = []
    Output: []

Constraints:
    0 <= firstList.length, secondList.length <= 1000
    firstList.length + secondList.length >= 1
    0 <= start_i < end_i <= 10^9, end_i < start_{i+1}
    0 <= start_j < end_j <= 10^9, end_j < start_{j+1}

Approach (two pointers):
    At pointers i, j the overlap is [max(starts), min(ends)]; it is valid if
    lo <= hi. Afterwards the interval that ends first can never intersect
    anything further in the other list (the other list's later intervals start
    after its current one), so advance that pointer.

Complexity:
    Time:  O(m + n)
    Space: O(1) extra (output excluded)

Alternative: sweep line over merged events, O((m+n) log(m+n)) - slower.
"""
from typing import List


def intervalIntersection(firstList: List[List[int]],
                         secondList: List[List[int]]) -> List[List[int]]:
    i = j = 0
    out: List[List[int]] = []
    while i < len(firstList) and j < len(secondList):
        lo = max(firstList[i][0], secondList[j][0])
        hi = min(firstList[i][1], secondList[j][1])
        if lo <= hi:
            out.append([lo, hi])
        if firstList[i][1] < secondList[j][1]:
            i += 1
        else:
            j += 1
    return out


def intervalIntersection_sweep(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    """Alternative: brute-force pairwise check (for cross-validation)."""
    out = []
    for s1, e1 in a:
        for s2, e2 in b:
            lo, hi = max(s1, s2), min(e1, e2)
            if lo <= hi:
                out.append([lo, hi])
    return sorted(out)


if __name__ == "__main__":
    a = [[0, 2], [5, 10], [13, 23], [24, 25]]
    b = [[1, 5], [8, 12], [15, 24], [25, 26]]
    exp = [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]
    assert intervalIntersection(a, b) == exp
    assert intervalIntersection_sweep(a, b) == exp
    assert intervalIntersection([[1, 3], [5, 9]], []) == []
    assert intervalIntersection([], [[4, 8], [10, 12]]) == []
    assert intervalIntersection([[1, 7]], [[3, 10]]) == [[3, 7]]
    assert intervalIntersection([[1, 3]], [[3, 5]]) == [[3, 3]]
    assert intervalIntersection([[1, 2]], [[3, 4]]) == []
    assert intervalIntersection([[1, 10]], [[2, 3], [5, 6]]) == [[2, 3], [5, 6]]
    import random
    for _ in range(200):
        def gen():
            pts = sorted(random.sample(range(0, 60), random.randint(0, 10) * 2))
            return [[pts[k], pts[k + 1]] for k in range(0, len(pts), 2)]
        x, y = gen(), gen()
        assert intervalIntersection(x, y) == intervalIntersection_sweep(x, y)
    print("All tests passed")
