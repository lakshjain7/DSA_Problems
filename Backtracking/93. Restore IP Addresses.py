"""
93. Restore IP Addresses
Difficulty: Medium
Topics: String, Backtracking

Problem:
A valid IP address consists of exactly four integers (0-255) separated by
single dots; no leading zeros allowed. Given a string s of digits, return all
possible valid IP addresses formed by inserting dots into s (not reordering or
removing digits). Answers may be returned in any order.

Example 1:
    Input: s = "25525511135"
    Output: ["255.255.11.135","255.255.111.35"]
Example 2:
    Input: s = "0000"
    Output: ["0.0.0.0"]
Example 3:
    Input: s = "101023"
    Output: ["1.0.10.23","1.0.102.3","10.1.0.23","10.10.2.3","101.0.2.3"]

Constraints:
    1 <= s.length <= 20
    s consists of digits only.

Approach (backtracking):
    Choose segment lengths 1..3 for each of 4 parts. Prune when a segment has
    a leading zero (length > 1), exceeds 255, or the remaining characters
    cannot fill the remaining parts (need between parts_left and 3*parts_left).
    The search tree has at most 3^4 leaves, so it is effectively constant.

Complexity: Time O(1) (bounded by 3^4 * 4), Space O(1) excluding output.
"""
from typing import List


def restore_ip_addresses(s: str) -> List[str]:
    res: List[str] = []
    n = len(s)
    if n < 4 or n > 12:
        return res
    parts: List[str] = []

    def bt(i: int) -> None:
        left = 4 - len(parts)
        rem = n - i
        if rem < left or rem > 3 * left:
            return
        if left == 0:
            res.append(".".join(parts))
            return
        for l in range(1, 4):
            seg = s[i:i + l]
            if len(seg) < l or (l > 1 and seg[0] == "0") or int(seg) > 255:
                continue
            parts.append(seg)
            bt(i + l)
            parts.pop()

    bt(0)
    return res


# Alternative: triple nested loops over the first three cut points.
def restore_ip_addresses_loops(s: str) -> List[str]:
    def ok(seg: str) -> bool:
        return bool(seg) and (len(seg) == 1 or seg[0] != "0") and int(seg) <= 255

    res = []
    n = len(s)
    for a in range(1, 4):
        for b in range(a + 1, a + 4):
            for c in range(b + 1, b + 4):
                if c >= n or n - c > 3:
                    continue
                segs = [s[:a], s[a:b], s[b:c], s[c:]]
                if all(ok(x) for x in segs):
                    res.append(".".join(segs))
    return res


if __name__ == "__main__":
    for fn in (restore_ip_addresses, restore_ip_addresses_loops):
        assert sorted(fn("25525511135")) == ["255.255.11.135", "255.255.111.35"]
        assert fn("0000") == ["0.0.0.0"]
        assert sorted(fn("101023")) == sorted(
            ["1.0.10.23", "1.0.102.3", "10.1.0.23", "10.10.2.3", "101.0.2.3"])
        assert fn("1") == []
        assert fn("1111111111111") == []
        assert fn("010010") == sorted(["0.10.0.10", "0.100.1.0"]) or \
            sorted(fn("010010")) == ["0.10.0.10", "0.100.1.0"]
        assert fn("256256256256") == []
    print("All tests passed")
