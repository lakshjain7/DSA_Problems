"""
271. Encode and Decode Strings
Difficulty: Medium
Topics: Array, String, Design

PROBLEM STATEMENT
-----------------
Design an algorithm to encode a list of strings to a single string. The encoded
string is then decoded back to the original list of strings.

Please implement `encode` and `decode` methods.

You are not allowed to solve the problem using any serialize methods (such as
`eval`).

Example 1:
    Input:  dummy_input = ["Hello", "World"]
    Output: ["Hello", "World"]
    Explanation:
        Machine 1:
            Codec encoder = new Codec();
            String msg = encoder.encode(strs);
        Machine 2:
            Codec decoder = new Codec();
            String[] strs = decoder.decode(msg);

Example 2:
    Input:  dummy_input = [""]
    Output: [""]

Constraints:
    1 <= strs.length <= 200
    0 <= strs[i].length <= 200
    strs[i] contains any possible characters out of 256 valid ASCII characters.

APPROACH — Length Prefixing
---------------------------
The core difficulty is that any delimiter we pick (a comma, a space, etc.) could
also legally appear inside one of the strings, which would make the boundary
ambiguous. Instead of relying on a delimiter that must not collide, we prepend
each string with its length followed by a separator character `#`:

    "Hello" -> "5#Hello"
    ""      -> "0#"

Encoding produces:  "5#Hello5#World"

To decode, we read digits up until we hit a `#`. Those digits tell us exactly how
many characters to consume next, so the content itself can contain any character
(including `#` or digits) without breaking the parse. Because the length is read
first and used to slice a precise window, there is never any ambiguity.

WHY IT WORKS
------------
The decoder never has to guess where a string ends. The length header is an
unambiguous instruction: "the next N characters — whatever they are — form the
payload." After consuming N characters the pointer lands exactly on the next
length header, and the process repeats until the string is exhausted.

COMPLEXITY
----------
Let n be the total number of characters across all strings.
    encode: O(n) time, O(n) space for the output.
    decode: O(n) time, O(n) space for the reconstructed list.
"""

from typing import List


class Codec:
    def encode(self, strs: List[str]) -> str:
        """Encodes a list of strings to a single string."""
        return "".join(f"{len(s)}#{s}" for s in strs)

    def decode(self, s: str) -> List[str]:
        """Decodes a single string to a list of strings."""
        res: List[str] = []
        i = 0
        n = len(s)
        while i < n:
            # Read the length header up to the '#' delimiter.
            j = i
            while s[j] != "#":
                j += 1
            length = int(s[i:j])
            # The payload is exactly `length` chars after the '#'.
            start = j + 1
            res.append(s[start:start + length])
            i = start + length
        return res


# ----------------------------------------------------------------------------
# Alternative approach: store lengths padded to a fixed width (4 chars), avoiding
# the need to scan for '#'. It trades a scan for a fixed offset — useful when
# payloads may themselves start with '#'.
# ----------------------------------------------------------------------------
class CodecFixedWidth:
    WIDTH = 4  # supports lengths up to 9999, enough for the constraints.

    def encode(self, strs: List[str]) -> str:
        return "".join(str(len(s)).rjust(self.WIDTH, "0") + s for s in strs)

    def decode(self, s: str) -> List[str]:
        res: List[str] = []
        i = 0
        n = len(s)
        while i < n:
            length = int(s[i:i + self.WIDTH])
            start = i + self.WIDTH
            res.append(s[start:start + length])
            i = start + length
        return res


if __name__ == "__main__":
    for CodecClass in (Codec, CodecFixedWidth):
        codec = CodecClass()

        # Basic round-trip.
        assert codec.decode(codec.encode(["Hello", "World"])) == ["Hello", "World"]

        # Single empty string.
        assert codec.decode(codec.encode([""])) == [""]

        # Multiple empty strings.
        assert codec.decode(codec.encode(["", "", ""])) == ["", "", ""]

        # Strings that contain the delimiter and digits.
        tricky = ["5#Hello", "12#", "###", "0#0#", "abc123"]
        assert codec.decode(codec.encode(tricky)) == tricky

        # Single string.
        assert codec.decode(codec.encode(["single"])) == ["single"]

        # Special ASCII characters.
        special = ["a b", "tab\tend", "new\nline", "quote\"q"]
        assert codec.decode(codec.encode(special)) == special

        # A longer list.
        big = [str(x) * (x % 7) for x in range(50)]
        assert codec.decode(codec.encode(big)) == big

        print(f"{CodecClass.__name__}: all tests passed!")
