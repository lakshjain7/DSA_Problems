"""
71. Simplify Path
Difficulty: Medium
Topics: String, Stack

Problem Statement
-----------------
You are given an absolute path for a Unix-style file system, which always
begins with a slash '/'. Your task is to transform this absolute path into
its simplified canonical path.

The rules of a Unix-style file system are as follows:
    - A single period '.' represents the current directory.
    - A double period '..' represents the previous/parent directory.
    - Multiple consecutive slashes such as '//' and '///' are treated as a
      single slash '/'.
    - Any sequence of periods that does NOT match the current/parent
      directory rules (for example '...' or '....') is treated as a valid
      directory or file name.

The simplified canonical path should follow these rules:
    - The path must start with a single slash '/'.
    - Directories within the path must be separated by exactly one slash '/'.
    - The path must not end with a slash '/', unless it is the root directory.
    - The path must not have any single or double periods ('.' and '..') used
      to denote the current or parent directories.

Return the simplified canonical path.

Examples
--------
Example 1:
    Input:  path = "/home/"
    Output: "/home"

Example 2:
    Input:  path = "/home//foo/"
    Output: "/home/foo"

Example 3:
    Input:  path = "/home/user/Documents/../Pictures"
    Output: "/home/user/Pictures"

Example 4:
    Input:  path = "/../"
    Output: "/"
    (Going one level up from the root '/' is a no-op, as the root is the
     highest level.)

Example 5:
    Input:  path = "/.../a/../b/c/../d/./"
    Output: "/.../b/d"
    ("..." is a valid name for a directory in this problem.)

Constraints
-----------
    1 <= path.length <= 3000
    path consists of English letters, digits, period '.', slash '/' or '_'.
    path is a valid absolute Unix path.

Approach (Stack)
----------------
Split the path on '/'. Splitting naturally handles multiple consecutive
slashes because they produce empty components. Then walk the components,
maintaining a stack of directory names:

    - ""  (empty, from '//' or leading/trailing slash) -> skip
    - "." (current directory)                          -> skip
    - ".." (parent directory)                          -> pop from the stack
                                                          if it is non-empty;
                                                          otherwise ignore
                                                          (we are at root)
    - anything else                                    -> push onto the stack

Finally, join the stack with '/' and prepend a leading '/'. If the stack is
empty, the answer is just the root "/".

Why it works: the stack always holds the canonical sequence of directories
seen so far. A ".." undoes the most recent real directory (LIFO), which is
exactly the semantics of moving to a parent directory. Empty and "."
components carry no directory information and are dropped.

Complexity
----------
Time:  O(n) - we scan each character once while splitting and once while
       processing the O(n) components.
Space: O(n) - the stack of directory names in the worst case.
"""

from typing import List


def simplify_path(path: str) -> str:
    """Return the simplified canonical Unix path using a stack."""
    stack: List[str] = []

    for part in path.split("/"):
        if part == "" or part == ".":
            continue
        if part == "..":
            if stack:
                stack.pop()
        else:
            stack.append(part)

    return "/" + "/".join(stack)


if __name__ == "__main__":
    # Provided examples
    assert simplify_path("/home/") == "/home"
    assert simplify_path("/home//foo/") == "/home/foo"
    assert simplify_path("/home/user/Documents/../Pictures") == "/home/user/Pictures"
    assert simplify_path("/../") == "/"
    assert simplify_path("/.../a/../b/c/../d/./") == "/.../b/d"

    # Root only
    assert simplify_path("/") == "/"
    assert simplify_path("///") == "/"

    # Single '.' collapses to root
    assert simplify_path("/./") == "/"

    # Multiple parent references beyond root stay at root
    assert simplify_path("/a/../../../") == "/"
    assert simplify_path("/a/./b/../../c/") == "/c"

    # '...' and '....' are valid directory names
    assert simplify_path("/...") == "/..."
    assert simplify_path("/....") == "/...."

    # Consecutive slashes everywhere
    assert simplify_path("/a//b////c/d//././/..") == "/a/b/c"

    # Path that ends up empty
    assert simplify_path("/..") == "/"

    # No trailing slash, plain path
    assert simplify_path("/abc") == "/abc"

    print("All tests passed for 71. Simplify Path")
