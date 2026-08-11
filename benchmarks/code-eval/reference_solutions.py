"""Correct reference solutions, used only by `selfcheck` to prove the hidden
tests are valid. Not used in the actual style A/B."""

SOLUTIONS = {
    "merge_intervals": r"""
def merge_intervals(intervals):
    if not intervals:
        return []
    s = sorted([list(iv) for iv in intervals], key=lambda x: x[0])
    out = [s[0][:]]
    for a, b in s[1:]:
        if a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out
""",
    "balanced_brackets": r"""
def is_balanced(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch in '([{':
            stack.append(ch)
        elif ch in ')]}':
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack
""",
    "word_frequencies": r"""
import re
def word_frequencies(text):
    out = {}
    for w in re.findall(r'[A-Za-z0-9]+', text.lower()):
        out[w] = out.get(w, 0) + 1
    return out
""",
    "roman_to_int": r"""
def roman_to_int(s):
    v = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
    total = 0
    for i, ch in enumerate(s):
        if i + 1 < len(s) and v[ch] < v[s[i+1]]:
            total -= v[ch]
        else:
            total += v[ch]
    return total
""",
    "flatten": r"""
def flatten(nested):
    out = []
    for x in nested:
        if isinstance(x, list):
            out.extend(flatten(x))
        else:
            out.append(x)
    return out
""",
    "rle_encode": r"""
def rle_encode(s):
    if not s:
        return ""
    out = []
    prev = s[0]
    count = 1
    for ch in s[1:]:
        if ch == prev:
            count += 1
        else:
            out.append(prev + str(count))
            prev = ch
            count = 1
    out.append(prev + str(count))
    return "".join(out)
""",
    "is_valid_ipv4": r"""
def is_valid_ipv4(s):
    parts = s.split('.')
    if len(parts) != 4:
        return False
    for p in parts:
        if not p.isdigit():
            return False
        if len(p) > 1 and p[0] == '0':
            return False
        if int(p) > 255:
            return False
    return True
""",
    "rotate_matrix": r"""
def rotate_matrix(m):
    if not m:
        return []
    n = len(m)
    return [[m[n-1-j][i] for j in range(n)] for i in range(n)]
""",
    "parse_query_string": r"""
def parse_query_string(qs):
    if not qs:
        return {}
    out = {}
    for pair in qs.split('&'):
        if '=' in pair:
            k, v = pair.split('=', 1)
        else:
            k, v = pair, ''
        if k in out:
            if isinstance(out[k], list):
                out[k].append(v)
            else:
                out[k] = [out[k], v]
        else:
            out[k] = v
    return out
""",
    "longest_common_prefix": r"""
def longest_common_prefix(strs):
    if not strs:
        return ""
    pref = strs[0]
    for s in strs[1:]:
        while not s.startswith(pref):
            pref = pref[:-1]
            if not pref:
                return ""
    return pref
""",
    "chunk": r"""
def chunk(lst, n):
    if n <= 0:
        raise ValueError("n must be positive")
    return [lst[i:i+n] for i in range(0, len(lst), n)]
""",
    "deep_get": r"""
def deep_get(d, path, default=None):
    if not path:
        return default
    cur = d
    for key in path.split('.'):
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur
""",
}
