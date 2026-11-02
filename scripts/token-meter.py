#!/usr/bin/env python3
"""Token meter for a Claude Code session, read from its transcript (.jsonl).

Usage:
  token-meter.py                     latest transcript under ~/.claude/projects
  token-meter.py PATH                a specific transcript
  token-meter.py --window 1000000    context window to measure against (default 200000)
  token-meter.py --json              machine-readable output
  token-meter.py --statusline        one line; reads Claude Code's status JSON on stdin

Counts are taken from the API usage records in the transcript, one per API call
(streamed chunks of the same message id are merged). This is not your plan quota:
check /usage in Claude Code or Settings > Usage on claude.ai for that.
"""
import argparse, glob, json, os, sys


def find_latest():
    files = glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl"))
    return max(files, key=os.path.getmtime) if files else None


def read_calls(path):
    calls = {}  # message id -> (order, usage, model, timestamp)
    order = 0
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            m = d.get("message")
            if d.get("type") != "assistant" or not isinstance(m, dict) or not m.get("usage"):
                continue
            mid = m.get("id") or d.get("uuid")
            prev = calls.get(mid)
            u = m["usage"]
            if prev is None:
                order += 1
                calls[mid] = (order, u, m.get("model"), d.get("timestamp"))
            elif (u.get("output_tokens") or 0) >= (prev[1].get("output_tokens") or 0):
                calls[mid] = (prev[0], u, m.get("model") or prev[2], d.get("timestamp") or prev[3])
    return [v for v in sorted(calls.values(), key=lambda v: v[0])]


def summarize(calls, window):
    g = lambda u, k: int(u.get(k) or 0)
    tot = {"input": 0, "cache_write": 0, "cache_read": 0, "output": 0}
    for _, u, _, _ in calls:
        tot["input"] += g(u, "input_tokens")
        tot["cache_write"] += g(u, "cache_creation_input_tokens")
        tot["cache_read"] += g(u, "cache_read_input_tokens")
        tot["output"] += g(u, "output_tokens")
    ctx = 0
    model = None
    if calls:
        _, u, model, _ = calls[-1]
        ctx = g(u, "input_tokens") + g(u, "cache_creation_input_tokens") + g(u, "cache_read_input_tokens")
    return {
        "api_calls": len(calls),
        "context_now": ctx,
        "context_window": window,
        "context_pct": round(100 * ctx / window, 1) if window else None,
        "totals": tot,
        "model": model,
        "started": calls[0][3] if calls else None,
        "last": calls[-1][3] if calls else None,
    }


def k(n):
    return f"{n/1000:.1f}k" if n >= 1000 else str(n)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?")
    ap.add_argument("--window", type=int, default=int(os.environ.get("MDCP_CONTEXT_WINDOW", 200000)))
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--statusline", action="store_true")
    a = ap.parse_args()

    path = a.path
    if a.statusline:
        try:
            path = json.load(sys.stdin).get("transcript_path") or path
        except ValueError:
            pass
    path = path or find_latest()
    if not path or not os.path.exists(path):
        print("no transcript found" if not a.statusline else "tokens: n/a")
        return 1 if not a.statusline else 0
    calls = read_calls(path)
    s = summarize(calls, a.window)
    if s["context_now"] > a.window:  # the session outgrew the assumed window, so it must be larger
        a.window = 1000000
        s = summarize(calls, a.window)
        s["window_assumed"] = True

    if a.json:
        print(json.dumps(s, indent=2))
    elif a.statusline:
        print(f"ctx {k(s['context_now'])}/{k(a.window)} ({s['context_pct']}%) | out {k(s['totals']['output'])} | {s['api_calls']} calls")
    else:
        t = s["totals"]
        bar = "#" * int((s["context_pct"] or 0) / 5)
        print(f"model            {s['model']}")
        print(f"api calls        {s['api_calls']}")
        print(f"context now      {s['context_now']:,} / {a.window:,}  ({s['context_pct']}%)  [{bar:<20}]")
        print(f"output total     {t['output']:,}")
        print(f"fresh input      {t['input']:,}")
        print(f"cache written    {t['cache_write']:,}")
        print(f"cache read       {t['cache_read']:,}  (re-reads of the same context; not new text)")
        print(f"first / last     {s['started']}  ->  {s['last']}")
        print("note: context window is a setting (--window); this is not your plan quota.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
