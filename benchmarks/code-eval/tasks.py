"""Work-equivalence coding tasks with hidden tests.

Each task: a natural coding request (prompt) + an entry_point the solution must
define + a hidden test (asserts, incl. edge cases) the extracted code must pass.
The style is the single toggled variable at generation time; the CODE is what the
tests judge. Pass/fail is ground truth, no LLM judge is involved anywhere.

Specs are deliberately a little non-standard (custom rules, edge cases) so a
memorized textbook answer does not automatically pass, giving the benchmark real
discriminating power.
"""

TASKS = [
    {
        "id": "merge_intervals",
        "entry_point": "merge_intervals",
        "prompt": (
            "Write a Python function `merge_intervals(intervals)` that takes a list "
            "of [start, end] integer pairs and returns a new list of merged, "
            "non-overlapping intervals sorted by start. Intervals that only touch at "
            "an endpoint (e.g. [1,2] and [2,3]) count as overlapping and must be "
            "merged. The input may be unsorted and may be empty."
        ),
        "test": r"""
from solution import merge_intervals as f
assert f([]) == []
assert f([[1,3]]) == [[1,3]]
assert f([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
assert f([[1,4],[4,5]]) == [[1,5]]           # touching endpoints merge
assert f([[5,6],[1,3],[2,2]]) == [[1,3],[5,6]]  # unsorted input
assert f([[1,10],[2,3],[4,5]]) == [[1,10]]   # fully contained
print("PASS")
""",
    },
    {
        "id": "balanced_brackets",
        "entry_point": "is_balanced",
        "prompt": (
            "Write a Python function `is_balanced(s)` that returns True iff every "
            "opening bracket in the string has a correct matching closing bracket in "
            "the right order, for the three bracket types (), [], and {}. Non-bracket "
            "characters are ignored. The empty string is balanced."
        ),
        "test": r"""
from solution import is_balanced as f
assert f("") is True
assert f("()") is True
assert f("([]{})") is True
assert f("(]") is False
assert f("([)]") is False          # wrong order
assert f("a(b)c[d]{e}") is True    # ignores non-brackets
assert f("(((") is False
assert f("}{") is False
print("PASS")
""",
    },
    {
        "id": "word_frequencies",
        "entry_point": "word_frequencies",
        "prompt": (
            "Write a Python function `word_frequencies(text)` that returns a dict "
            "mapping each word to how many times it appears, case-insensitive. A word "
            "is a maximal run of letters and digits; all other characters are "
            "separators. Apostrophes do NOT join words (so \"don't\" is two words: "
            "\"don\" and \"t\"). An empty or punctuation-only string returns an empty "
            "dict."
        ),
        "test": r"""
from solution import word_frequencies as f
assert f("") == {}
assert f("...!!!") == {}
assert f("The cat the CAT") == {"the": 2, "cat": 2}
assert f("a1 A1 a1") == {"a1": 3}
assert f("don't") == {"don": 1, "t": 1}
assert f("Hello, hello... world!") == {"hello": 2, "world": 1}
print("PASS")
""",
    },
    {
        "id": "roman_to_int",
        "entry_point": "roman_to_int",
        "prompt": (
            "Write a Python function `roman_to_int(s)` that converts an uppercase "
            "Roman numeral string (I, V, X, L, C, D, M) to its integer value, "
            "supporting subtractive notation (IV=4, IX=9, XL=40, XC=90, CD=400, "
            "CM=900)."
        ),
        "test": r"""
from solution import roman_to_int as f
assert f("I") == 1
assert f("IV") == 4
assert f("IX") == 9
assert f("LVIII") == 58
assert f("MCMXCIV") == 1994
assert f("MMXXVI") == 2026
assert f("XLII") == 42
print("PASS")
""",
    },
    {
        "id": "flatten",
        "entry_point": "flatten",
        "prompt": (
            "Write a Python function `flatten(nested)` that flattens an arbitrarily "
            "nested list of integers into a single flat list, preserving left-to-right "
            "order. Only lists are containers; other values are leaves. Strings must "
            "be treated as leaves, not iterated. Handles empty lists at any depth."
        ),
        "test": r"""
from solution import flatten as f
assert f([]) == []
assert f([1,2,3]) == [1,2,3]
assert f([1,[2,[3,[4]]]]) == [1,2,3,4]
assert f([[],[1],[[2],[]]]) == [1,2]
assert f([1,["ab",[2]]]) == [1,"ab",2]   # strings are leaves
print("PASS")
""",
    },
    {
        "id": "rle_encode",
        "entry_point": "rle_encode",
        "prompt": (
            "Write a Python function `rle_encode(s)` that run-length-encodes a string: "
            "each maximal run of a repeated character becomes the character followed "
            "by the run length as a decimal number, even when the length is 1 (so "
            "\"abc\" -> \"a1b1c1\"). The empty string returns the empty string."
        ),
        "test": r"""
from solution import rle_encode as f
assert f("") == ""
assert f("a") == "a1"
assert f("aaa") == "a3"
assert f("abc") == "a1b1c1"
assert f("aaabbc") == "a3b2c1"
assert f("aabbaa") == "a2b2a2"     # runs, not global counts
print("PASS")
""",
    },
    {
        "id": "is_valid_ipv4",
        "entry_point": "is_valid_ipv4",
        "prompt": (
            "Write a Python function `is_valid_ipv4(s)` that returns True iff s is a "
            "valid dotted IPv4 address: exactly four parts separated by single dots, "
            "each part a decimal number 0-255 with NO leading zeros (so \"0\" is ok "
            "but \"00\" and \"01\" are not), and no other characters."
        ),
        "test": r"""
from solution import is_valid_ipv4 as f
assert f("0.0.0.0") is True
assert f("192.168.1.1") is True
assert f("255.255.255.255") is True
assert f("256.1.1.1") is False
assert f("1.1.1.01") is False      # leading zero
assert f("1.1.1") is False         # too few parts
assert f("1.1.1.1.1") is False     # too many
assert f("1.1.1.-1") is False
assert f("a.b.c.d") is False
assert f("1.1.1.1 ") is False      # trailing space
print("PASS")
""",
    },
    {
        "id": "rotate_matrix",
        "entry_point": "rotate_matrix",
        "prompt": (
            "Write a Python function `rotate_matrix(m)` that takes an NxN matrix "
            "(list of lists) and returns a NEW matrix rotated 90 degrees clockwise. "
            "Do not mutate the input. Handles the 1x1 and empty cases."
        ),
        "test": r"""
from solution import rotate_matrix as f
assert f([]) == []
assert f([[1]]) == [[1]]
assert f([[1,2],[3,4]]) == [[3,1],[4,2]]
m = [[1,2,3],[4,5,6],[7,8,9]]
assert f(m) == [[7,4,1],[8,5,2],[9,6,3]]
assert m == [[1,2,3],[4,5,6],[7,8,9]]   # input not mutated
print("PASS")
""",
    },
    {
        "id": "parse_query_string",
        "entry_point": "parse_query_string",
        "prompt": (
            "Write a Python function `parse_query_string(qs)` that parses a URL query "
            "string like \"a=1&b=2&a=3\" into a dict. A key that appears once maps to "
            "its string value; a key that appears more than once maps to a list of its "
            "values in order. A key with no '=' maps to the empty string. The empty "
            "input returns an empty dict."
        ),
        "test": r"""
from solution import parse_query_string as f
assert f("") == {}
assert f("a=1") == {"a": "1"}
assert f("a=1&b=2") == {"a": "1", "b": "2"}
assert f("a=1&a=2&a=3") == {"a": ["1","2","3"]}
assert f("x") == {"x": ""}
assert f("a=1&b=2&a=3") == {"a": ["1","3"], "b": "2"}
print("PASS")
""",
    },
    {
        "id": "longest_common_prefix",
        "entry_point": "longest_common_prefix",
        "prompt": (
            "Write a Python function `longest_common_prefix(strs)` that returns the "
            "longest string that is a prefix of every string in the list. Returns the "
            "empty string if the list is empty or there is no common prefix. "
            "Comparison is case-sensitive."
        ),
        "test": r"""
from solution import longest_common_prefix as f
assert f([]) == ""
assert f(["flower","flow","flight"]) == "fl"
assert f(["dog","racecar","car"]) == ""
assert f(["same","same","same"]) == "same"
assert f(["abc"]) == "abc"
assert f(["ABC","ABc"]) == "AB"       # case-sensitive
assert f(["", "abc"]) == ""
print("PASS")
""",
    },
    {
        "id": "chunk",
        "entry_point": "chunk",
        "prompt": (
            "Write a Python function `chunk(lst, n)` that splits a list into "
            "consecutive sublists of length n; the final chunk may be shorter if there "
            "are not enough elements. If n <= 0, raise ValueError. An empty list "
            "returns an empty list."
        ),
        "test": r"""
from solution import chunk as f
assert f([], 3) == []
assert f([1,2,3,4,5], 2) == [[1,2],[3,4],[5]]
assert f([1,2,3,4], 2) == [[1,2],[3,4]]
assert f([1,2,3], 5) == [[1,2,3]]
try:
    f([1,2,3], 0); assert False, "expected ValueError"
except ValueError:
    pass
print("PASS")
""",
    },
    {
        "id": "deep_get",
        "entry_point": "deep_get",
        "prompt": (
            "Write a Python function `deep_get(d, path, default=None)` that looks up a "
            "value in a nested dict by a dot-separated path string (e.g. "
            "\"a.b.c\"). Return the value if the full path exists, otherwise return "
            "default. If at any step the current value is not a dict, or the key is "
            "missing, return default. An empty path returns default."
        ),
        "test": r"""
from solution import deep_get as f
d = {"a": {"b": {"c": 42}}, "x": 1}
assert f(d, "a.b.c") == 42
assert f(d, "a.b") == {"c": 42}
assert f(d, "a.b.z") is None
assert f(d, "a.b.c.d") is None       # c is not a dict
assert f(d, "x.y", "missing") == "missing"
assert f(d, "") is None
assert f(d, "nope", 0) == 0
print("PASS")
""",
    },
]
