"""
1268. Search Suggestions System
Difficulty: Medium
Topics: Array, String, Binary Search, Trie, Sorting

Problem:
You are given an array of strings products and a string searchWord.
Design a system that suggests at most three product names from products
after each character of searchWord is typed. Suggested products should have
a common prefix with searchWord. If there are more than three products with
a common prefix, return the three lexicographically smallest products.
Return a list of lists of the suggested products after each character of
searchWord is typed.

Example 1:
    Input: products = ["mobile","mouse","moneypot","monitor","mousepad"],
           searchWord = "mouse"
    Output: [["mobile","moneypot","monitor"],["mobile","moneypot","monitor"],
             ["mouse","mousepad"],["mouse","mousepad"],["mouse","mousepad"]]

Example 2:
    Input: products = ["havana"], searchWord = "havana"
    Output: [["havana"],["havana"],["havana"],["havana"],["havana"],["havana"]]

Constraints:
    1 <= products.length <= 1000
    1 <= products[i].length <= 3000
    1 <= sum(products[i].length) <= 2 * 10^4
    All products are unique; lowercase English letters only.
    1 <= searchWord.length <= 1000

Approach (sort + binary search):
    Sort products. For each typed prefix, the products sharing it form a
    contiguous block in sorted order starting at bisect_left(prefix). Take up
    to three items from that index while they still start with the prefix.
    Since the prefix only grows, the left bound is monotone, so we could even
    reuse the previous index as the lower bound for bisect.

Complexity: O(S log n + m * 3 * L) time where S = total chars sorted cost,
    m = len(searchWord), L = prefix comparison cost; O(1) extra space besides
    output.

Alternative (Trie): insert all products keeping, at each node, the three
    smallest words passing through it (insert in sorted order, append while
    len < 3). Walk the trie along searchWord. O(total chars) build.
"""
from bisect import bisect_left
from typing import List


def suggestedProducts(products: List[str], searchWord: str) -> List[List[str]]:
    products = sorted(products)
    res: List[List[str]] = []
    lo = 0
    prefix = ""
    for ch in searchWord:
        prefix += ch
        lo = bisect_left(products, prefix, lo)
        cur = []
        for i in range(lo, min(lo + 3, len(products))):
            if products[i].startswith(prefix):
                cur.append(products[i])
            else:
                break
        res.append(cur)
    return res


def suggestedProductsTrie(products: List[str], searchWord: str) -> List[List[str]]:
    root: dict = {}
    for w in sorted(products):
        node = root
        for c in w:
            node = node.setdefault(c, {})
            lst = node.setdefault("#", [])
            if len(lst) < 3:
                lst.append(w)
    res: List[List[str]] = []
    node = root
    for c in searchWord:
        if node is not None and c in node:
            node = node[c]
            res.append(list(node["#"]))
        else:
            node = None
            res.append([])
    return res


if __name__ == "__main__":
    p1 = ["mobile", "mouse", "moneypot", "monitor", "mousepad"]
    e1 = [["mobile", "moneypot", "monitor"], ["mobile", "moneypot", "monitor"],
          ["mouse", "mousepad"], ["mouse", "mousepad"], ["mouse", "mousepad"]]
    for f in (suggestedProducts, suggestedProductsTrie):
        assert f(p1, "mouse") == e1
        assert f(["havana"], "havana") == [["havana"]] * 6
        assert f(["bags", "baggage", "banner", "box", "cloths"], "bags") == [
            ["baggage", "bags", "banner"], ["baggage", "bags", "banner"],
            ["baggage", "bags"], ["bags"]]
        assert f(["havana"], "tatiana") == [[]] * 7
        assert f(["a", "ab", "abc", "abcd"], "ab") == [["a", "ab", "abc"], ["ab", "abc", "abcd"]]
    print("All tests passed")
