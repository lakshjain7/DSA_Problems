"""
721. Accounts Merge
Difficulty: Medium
Topics: Array, Hash Table, String, Depth-First Search, Union Find, Sorting

Problem:
Given a list of accounts where each element accounts[i] is a list of strings,
where the first element accounts[i][0] is a name, and the rest are emails
representing emails of the account.

Two accounts definitely belong to the same person if there is some common email
to both accounts. A person can have any number of accounts initially, but all
of their accounts definitely have the same name.

After merging the accounts, return the accounts in the following format: the
first element of each account is the name, and the rest are emails in sorted
order. The accounts themselves can be returned in any order.

Example 1:
    Input: accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],
                       ["John","johnsmith@mail.com","john00@mail.com"],
                       ["Mary","mary@mail.com"],
                       ["John","johnnybravo@mail.com"]]
    Output: [["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],
             ["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]

Constraints:
    1 <= accounts.length <= 1000
    2 <= accounts[i].length <= 10
    1 <= accounts[i][j].length <= 30
    accounts[i][0] consists of English letters.
    accounts[i][j] (for j > 0) is a valid email.

Approach (Union-Find on emails):
    Every email is a node. For each account, union all its emails with the
    account's first email. Emails that share a component belong to the same
    person. Finally group emails by root, sort each group, prepend the name.
    Correct because "shares an email" is transitive through the union relation.

Complexity:
    Time:  O(N * alpha(N) + N log N) where N = total emails (sorting dominates)
    Space: O(N)
"""
from collections import defaultdict
from typing import Dict, List


def accountsMerge(accounts: List[List[str]]) -> List[List[str]]:
    parent: Dict[str, str] = {}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    owner: Dict[str, str] = {}
    for acc in accounts:
        name = acc[0]
        for e in acc[1:]:
            if e not in parent:
                parent[e] = e
            owner[e] = name
            union(acc[1], e)

    groups = defaultdict(list)
    for e in parent:
        groups[find(e)].append(e)
    return [[owner[r]] + sorted(es) for r, es in groups.items()]


# Alternative approach: DFS over an email graph.
def accountsMergeDFS(accounts: List[List[str]]) -> List[List[str]]:
    graph = defaultdict(set)
    owner = {}
    for acc in accounts:
        for e in acc[1:]:
            owner[e] = acc[0]
            graph[acc[1]].add(e)
            graph[e].add(acc[1])
    seen = set()
    res = []
    for e in graph:
        if e in seen:
            continue
        seen.add(e)
        stack, comp = [e], []
        while stack:
            cur = stack.pop()
            comp.append(cur)
            for nb in graph[cur]:
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        res.append([owner[e]] + sorted(comp))
    return res


def _norm(r):
    return sorted(map(tuple, r))


if __name__ == "__main__":
    a = [["John", "johnsmith@mail.com", "john_newyork@mail.com"],
         ["John", "johnsmith@mail.com", "john00@mail.com"],
         ["Mary", "mary@mail.com"],
         ["John", "johnnybravo@mail.com"]]
    exp = [["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
           ["Mary", "mary@mail.com"], ["John", "johnnybravo@mail.com"]]
    for f in (accountsMerge, accountsMergeDFS):
        assert _norm(f(a)) == _norm(exp)
        # single account
        assert f([["A", "a@x.com"]]) == [["A", "a@x.com"]]
        # transitive chain across three accounts
        t = [["A", "1@x", "2@x"], ["A", "3@x", "4@x"], ["A", "2@x", "3@x"]]
        assert f(t) == [["A", "1@x", "2@x", "3@x", "4@x"]]
        # same name, disjoint emails stay separate
        d = [["Bob", "b1@x"], ["Bob", "b2@x"]]
        assert _norm(f(d)) == _norm(d)
        # duplicate emails inside an account
        assert f([["C", "c@x", "c@x"]]) == [["C", "c@x"]]
    print("All tests passed.")
