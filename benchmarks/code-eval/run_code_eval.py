#!/usr/bin/env python3
"""Work-equivalence benchmark: does the output style change the CODE?

The single non-circular, no-LLM-judge test. For each coding task we generate a
solution with the style OFF (default) and ON (styled), hermetically, extract the
code, and run it against a HIDDEN test. Pass/fail is ground truth. If the styled
arm's pass rate matches the default arm's, the style does not touch the work,
which is the whole design claim (`keep-coding-instructions: true`).

Phases:
  selfcheck   run every task's hidden test against a reference solution, to prove
              the TESTS themselves are correct before trusting any result
  run         generate default + styled (N reps), extract code, run tests
  agg         report pass@1 per arm and per task

Usage:
  python3 run_code_eval.py selfcheck
  python3 run_code_eval.py run [--reps 3] [--workers 4] [--limit N]
  python3 run_code_eval.py agg
"""

import argparse
import concurrent.futures as cf
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "harness"))
import adapters  # noqa: E402  (hermetic generate + pinned model)

from tasks import TASKS  # noqa: E402

REPO = os.path.dirname(os.path.dirname(HERE))
DEFAULT_STYLE = os.path.join(REPO, "output-styles", "attention-kind.md")
STYLE_FILE = os.environ.get("BENCH_STYLE_FILE", DEFAULT_STYLE)
RESULTS = os.environ.get(
    "BENCH_CODE_RESULTS", os.path.join(HERE, "results.jsonl"))
TEST_TIMEOUT = 20


def load_style_body():
    lines = open(STYLE_FILE).read().splitlines()
    body, started = [], False
    for ln in lines:
        if "<!-- body-start -->" in ln:
            started = True
            continue
        if started:
            if ln.strip().startswith("<!--") and ln.strip().endswith("-->"):
                continue
            body.append(ln)
    out = "\n".join(body).strip()
    if not out:
        raise SystemExit("empty style body")
    return out


import ast  # noqa: E402


def extract_code(text, entry_point=None):
    """Extract the solution's definitions, dropping module-level demo/usage code.

    The verbose (default) arm often appends example calls like `print(f(...))`;
    importing that runs (and can crash) the demo, which would look like a code
    failure when it is really a demo. We parse the joined code blocks and keep
    only imports, functions, classes, and constant assignments, dropping bare
    expressions and any `if __name__ == '__main__'` block. Applied identically to
    both arms, so it is a fair normalization, not a thumb on the scale."""
    blocks = re.findall(r"```(?:python|py)\s*\n(.*?)```", text, flags=re.S)
    if not blocks:
        blocks = re.findall(r"```\s*\n(.*?)```", text, flags=re.S)
    code = "\n\n".join(b.strip() for b in blocks) if blocks else text
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return code  # unparseable => let the hidden test fail it honestly
    keep = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef,
                             ast.Import, ast.ImportFrom, ast.Assign,
                             ast.AnnAssign)):
            keep.append(node)
        # drop bare Expr (demo prints), If __main__ guards, etc.
    module = ast.Module(body=keep, type_ignores=[])
    try:
        return ast.unparse(module)
    except Exception:  # noqa: BLE001
        return code


def run_solution(sol_code, test_code, timeout=TEST_TIMEOUT):
    """Write solution.py + the hidden test, run it isolated. Return (passed, info)."""
    with tempfile.TemporaryDirectory() as td:
        with open(os.path.join(td, "solution.py"), "w") as f:
            f.write(sol_code)
        with open(os.path.join(td, "run_test.py"), "w") as f:
            f.write(test_code)
        try:
            p = subprocess.run(
                [sys.executable, "run_test.py"], cwd=td,
                capture_output=True, text=True, timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return False, "timeout"
        ok = p.returncode == 0 and "PASS" in p.stdout
        info = "ok" if ok else (p.stderr.strip().splitlines() or ["?"])[-1][:160]
        return ok, info


# ---- selfcheck: validate the hidden tests against reference solutions ----

def phase_selfcheck():
    import reference_solutions as ref
    bad = 0
    for t in TASKS:
        sol = ref.SOLUTIONS[t["id"]]
        ok, info = run_solution(sol, t["test"])
        print(f"  {t['id']:<22} {'OK' if ok else 'FAIL: ' + info}")
        bad += 0 if ok else 1
    print(f"\n{'ALL TESTS VALID' if not bad else str(bad) + ' BROKEN TESTS'}")
    sys.exit(1 if bad else 0)


# ---- run: generate + test both arms ----

def read_results():
    if not os.path.exists(RESULTS):
        return []
    return [json.loads(l) for l in open(RESULTS) if l.strip()]


def append_result(rec):
    with open(RESULTS, "a") as f:
        f.write(json.dumps(rec) + "\n")


def _one(task, rep, style_body):
    q = task["prompt"]
    out = {}
    for arm, body in (("default", None), ("styled", style_body)):
        text = adapters.generate(q, style_body=body)
        code = extract_code(text, task["entry_point"])
        passed, info = run_solution(code, task["test"])
        out[arm] = {"passed": passed, "info": info, "chars": len(text),
                    "code_chars": len(code), "text": text}
    return {"id": task["id"], "rep": rep,
            "default_pass": out["default"]["passed"],
            "styled_pass": out["styled"]["passed"],
            "detail": out}


def phase_run(reps, workers, limit):
    style_body = load_style_body()
    tasks = TASKS[:limit] if limit else TASKS
    done = {(r["id"], r["rep"]) for r in read_results()}
    jobs = [(t, rep) for t in tasks for rep in range(reps)
            if (t["id"], rep) not in done]
    print(f"[run] {len(jobs)} (task,rep) cells, reps={reps}, workers={workers}",
          file=sys.stderr)
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(_one, t, rep, style_body): (t["id"], rep)
                for t, rep in jobs}
        for fut in cf.as_completed(futs):
            tid, rep = futs[fut]
            try:
                rec = fut.result()
                append_result(rec)
                d = "P" if rec["default_pass"] else "F"
                s = "P" if rec["styled_pass"] else "F"
                print(f"[run] {tid:<22} rep{rep}  default={d} styled={s}",
                      file=sys.stderr)
            except Exception as e:  # noqa: BLE001
                print(f"[run] FAIL {tid} rep{rep}: {e}", file=sys.stderr)


def phase_agg():
    rows = read_results()
    if not rows:
        print("no results; run first", file=sys.stderr)
        return
    n = len(rows)
    dp = sum(r["default_pass"] for r in rows)
    sp = sum(r["styled_pass"] for r in rows)
    # per task
    per = {}
    for r in rows:
        per.setdefault(r["id"], {"d": 0, "s": 0, "n": 0})
        per[r["id"]]["d"] += r["default_pass"]
        per[r["id"]]["s"] += r["styled_pass"]
        per[r["id"]]["n"] += 1
    print(f"cells: {n}  (tasks={len(per)})")
    print(f"default pass@1: {dp}/{n} = {round(100*dp/n,1)}%")
    print(f"styled  pass@1: {sp}/{n} = {round(100*sp/n,1)}%")
    print(f"difference (styled - default): {round(100*(sp-dp)/n,1)} pp")
    print("\nper task (default vs styled, of reps):")
    for tid, v in sorted(per.items()):
        flag = "" if v["d"] == v["s"] else "   <-- differs"
        print(f"  {tid:<22} {v['d']}/{v['n']}  vs  {v['s']}/{v['n']}{flag}")
    out = {"cells": n, "tasks": len(per),
           "default_pass_pct": round(100*dp/n, 1),
           "styled_pass_pct": round(100*sp/n, 1),
           "diff_pp": round(100*(sp-dp)/n, 1),
           "gen_model": adapters.GEN_MODEL, "per_task": per}
    json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=["selfcheck", "run", "agg"])
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    if args.phase == "selfcheck":
        phase_selfcheck()
    elif args.phase == "run":
        phase_run(args.reps, args.workers, args.limit)
    else:
        phase_agg()


if __name__ == "__main__":
    main()
