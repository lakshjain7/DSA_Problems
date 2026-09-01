"""
68. Text Justification
Difficulty: Hard
Topics: Array, String, Simulation, Greedy

PROBLEM STATEMENT
-----------------
Given an array of strings `words` and a width `maxWidth`, format the text so
that each line has exactly `maxWidth` characters and is fully (left and right)
justified.

Pack as many words as possible into each line using a greedy approach, then pad
each line with spaces so it becomes exactly `maxWidth` characters:

  * Distribute extra spaces between words as evenly as possible. If the spaces on
    a line do not divide evenly, the empty slots on the LEFT receive more spaces
    than the slots on the right.
  * The LAST line, and any line containing only a single word, is
    LEFT-justified: words separated by a single space and the remaining width
    padded with trailing spaces (no extra space is inserted between words).

Each word is guaranteed to be longer than 0 and not exceed maxWidth. The input
words are separated by at least one space, and a line's total length is the sum
of the word lengths plus the spaces between them.

Example 1:
    Input:
        words = ["This", "is", "an", "example", "of", "text", "justification."]
        maxWidth = 16
    Output:
        [
           "This    is    an",
           "example  of text",
           "justification.  "
        ]

Example 2:
    Input:
        words = ["What", "must", "be", "acknowledgment", "shall", "be"]
        maxWidth = 16
    Output:
        [
          "What   must   be",
          "acknowledgment  ",
          "shall be        "
        ]
    Explanation: the second line has a single word "acknowledgment" so it is
    left-justified, and the last line "shall be" is also left-justified.

Example 3:
    Input:
        words = ["Science","is","what","we","understand","well","enough","to",
                 "explain","to","a","computer.","Art","is","everything","else",
                 "we","do"]
        maxWidth = 20
    Output:
        [
          "Science  is  what we",
          "understand      well",
          "enough to explain to",
          "a  computer.  Art is",
          "everything  else  we",
          "do                  "
        ]

Constraints:
    1 <= words.length <= 300
    1 <= words[i].length <= 20
    words[i] consists of only English letters and symbols.
    1 <= maxWidth <= 100
    words[i].length <= maxWidth


APPROACH — Greedy line packing + per-line justification (simulation)
--------------------------------------------------------------------
Two phases per output line:

1. Pack greedily. Starting from the current word index, keep adding words to the
   current line while they fit. A group of `cnt` words needs at least
   (sum of their lengths) + (cnt - 1) minimum single spaces. We track the running
   sum of raw word lengths `line_len`; word `w` still fits if
        line_len + len(w) + (number_of_words_already_on_line) <= maxWidth
   where the added count term accounts for the minimum single space before `w`.

2. Justify the packed line.
   * If it is the LAST line, or it holds a single word, LEFT-justify: join with
     single spaces, then pad the right with spaces up to maxWidth.
   * Otherwise FULL-justify: there are `gaps = cnt - 1` slots and
     `total_spaces = maxWidth - line_len` spaces to spread. Each gap gets
     `total_spaces // gaps`, and the leftmost `total_spaces % gaps` gaps get one
     extra space each. Build the line gap by gap.

Why greedy is optimal here: the problem *defines* the packing rule as "fit as
many words as possible per line", so a left-to-right greedy pass is not just a
heuristic — it is the specification. Justification is then a deterministic
formatting step on each fixed group.

Time Complexity:  O(total characters of output) = O(n * maxWidth) in the worst
                  case — every character of every line is produced once.
Space Complexity: O(maxWidth) auxiliary per line (excluding the output list).
"""

from __future__ import annotations

from typing import List


class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        result: List[str] = []
        i = 0
        n = len(words)

        while i < n:
            # --- Phase 1: greedily pack words [i, j) onto the current line. ---
            j = i
            line_len = 0  # sum of raw word lengths on the line
            while j < n:
                # words already chosen so far == (j - i); each needs >= 1 space
                # before it, so minimum consumed width if we add words[j] is:
                if line_len + len(words[j]) + (j - i) > maxWidth:
                    break
                line_len += len(words[j])
                j += 1

            count = j - i  # number of words on this line
            is_last_line = j == n

            # --- Phase 2: justify. ---
            if is_last_line or count == 1:
                # Left-justify: single spaces, pad the right.
                line = " ".join(words[i:j])
                line += " " * (maxWidth - len(line))
            else:
                total_spaces = maxWidth - line_len
                gaps = count - 1
                base, extra = divmod(total_spaces, gaps)

                pieces: List[str] = []
                for idx in range(i, j - 1):
                    pieces.append(words[idx])
                    # Leftmost `extra` gaps get one additional space.
                    spaces = base + (1 if (idx - i) < extra else 0)
                    pieces.append(" " * spaces)
                pieces.append(words[j - 1])  # last word, no trailing gap space
                line = "".join(pieces)

            result.append(line)
            i = j

        return result


if __name__ == "__main__":
    sol = Solution()

    def check(words: List[str], maxWidth: int, expected: List[str]) -> None:
        got = sol.fullJustify(words, maxWidth)
        # Every produced line must be exactly maxWidth wide.
        for ln in got:
            assert len(ln) == maxWidth, f"width {len(ln)} != {maxWidth}: {ln!r}"
        assert got == expected, f"\n got={got}\n want={expected}"

    # Example 1.
    check(
        ["This", "is", "an", "example", "of", "text", "justification."],
        16,
        [
            "This    is    an",
            "example  of text",
            "justification.  ",
        ],
    )

    # Example 2.
    check(
        ["What", "must", "be", "acknowledgment", "shall", "be"],
        16,
        [
            "What   must   be",
            "acknowledgment  ",
            "shall be        ",
        ],
    )

    # Example 3.
    check(
        [
            "Science", "is", "what", "we", "understand", "well", "enough", "to",
            "explain", "to", "a", "computer.", "Art", "is", "everything",
            "else", "we", "do",
        ],
        20,
        [
            "Science  is  what we",
            "understand      well",
            "enough to explain to",
            "a  computer.  Art is",
            "everything  else  we",
            "do                  ",
        ],
    )

    # Single word exactly filling the width.
    check(["abc"], 3, ["abc"])

    # Single word narrower than the width -> left-justified padding.
    check(["hi"], 5, ["hi   "])

    # Two words, single line, not last would still be last here -> left-justified.
    check(["a", "b"], 5, ["a b  "])

    # A line with one very long word among others: that word sits on its own line.
    check(
        ["a", "bb", "ccc", "dddd"],
        4,
        [
            "a bb",
            "ccc ",
            "dddd",
        ],
    )

    # A single line is always the LAST line, hence left-justified.
    check(["a", "b", "c"], 9, ["a b c    "])
    check(["a", "b", "c"], 8, ["a b c   "])

    # Full-justification with uneven spaces (force a non-last line by adding a
    # second line). First line "a b c" on width 8: line_len=3, gaps=2,
    # total_spaces=5 -> base 2, extra 1 -> leftmost gap gets 3 spaces.
    check(["a", "b", "c", "dddddddd"], 8, ["a   b  c", "dddddddd"])
    # First line "a b c" on width 9: total_spaces=6, gaps=2 -> 3 each.
    check(["a", "b", "c", "ddddddddd"], 9, ["a   b   c", "ddddddddd"])

    print("All 68. Text Justification tests passed!")
