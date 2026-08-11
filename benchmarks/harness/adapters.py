"""Hermetic answer generation for the benchmark.

One job: generate an answer to a prompt with the output style OFF (default) or ON
(styled), under identical, isolated conditions, so the style is the only variable.

Hermetic means `--setting-sources ""` (no user/project CLAUDE.md, hooks, or
ambient output style), `--strict-mcp-config` (no MCP), every tool disallowed, and
an empty scratch cwd. So no personal data or live tool output can leak into either
arm, both answer the same question from the model's own knowledge, and runs are
reproducible. The default arm is genuinely vanilla Claude, not a tuned persona.

Used by: code-eval/run_code_eval.py, code-eval/deliverable_purity.py.
"""

import json
import os
import subprocess
import tempfile

GEN_MODEL = os.environ.get("BENCH_GEN_MODEL", "claude-opus-4-8")
GEN_TIMEOUT = int(os.environ.get("BENCH_GEN_TIMEOUT", "240"))

_FORCE_DEFAULT = json.dumps({"outputStyle": "default"})

# Every tool, denied. A benchmark answer must come from the model's own knowledge,
# never from the operator's live calendar/inbox/memory, or the two arms would
# answer different questions and the results would be irreproducible.
_DISALLOWED = (
    "Bash,Read,Edit,Write,MultiEdit,NotebookEdit,Glob,Grep,Task,WebFetch,"
    "WebSearch,TodoWrite,BashOutput,KillBash,SlashCommand,ExitPlanMode"
)

# An empty scratch cwd so file tools (even if one slipped through) see nothing.
_SCRATCH = os.path.join(tempfile.gettempdir(), "attn_bench_scratch")
os.makedirs(_SCRATCH, exist_ok=True)


def generate(question, style_body=None):
    """One hermetic answer. style_body=None -> default arm; a string -> styled."""
    cmd = [
        "claude", "-p",
        "--model", GEN_MODEL,
        "--setting-sources", "",
        "--strict-mcp-config",
        "--disallowedTools", _DISALLOWED,
        "--settings", _FORCE_DEFAULT,
    ]
    if style_body:
        cmd += ["--append-system-prompt", style_body]
    # Prompt via stdin so the variadic --disallowedTools cannot swallow it.
    out = subprocess.run(
        cmd, input=question, capture_output=True, text=True,
        timeout=GEN_TIMEOUT, cwd=_SCRATCH,
    )
    if out.returncode != 0:
        raise RuntimeError(f"generate failed: {out.stderr.strip()[:400]}")
    return out.stdout.strip()
