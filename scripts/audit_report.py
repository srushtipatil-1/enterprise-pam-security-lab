"""Turn a HashiCorp Vault file audit log into human-readable audit evidence.

Reads the JSON-lines audit log, keeps one row per completed request
(`type == "response"`), and writes a Markdown report with:
  - summary counts (total / allowed / denied / root-token usage)
  - activity per identity (WHO)
  - every DENIED request (the most important evidence for RBAC)
  - a full WHO / WHAT / WHEN / RESULT table

Secret values never appear: Vault already HMACs sensitive fields, and this
script only reads metadata (identity, policies, operation, path, time, error).

Usage:
    python scripts/audit_report.py C:\\vault\\audit.log
    python scripts/audit_report.py C:\\vault\\audit.log -o evidence/audit-report.md
    python scripts/audit_report.py C:\\vault\\audit.log --denied-only
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

NOISE_PREFIXES = ("sys/internal/ui/",)  # CLI preflight lookups


def parse_log(path, include_noise=False):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except ValueError:
                print(f"warning: skipping unparsable line {line_no}", file=sys.stderr)
                continue
            if rec.get("type") != "response":
                continue
            req, auth = rec.get("request") or {}, rec.get("auth") or {}
            path_ = req.get("path", "")
            if not include_noise and path_.startswith(NOISE_PREFIXES):
                continue
            error = rec.get("error") or ""
            allowed = (auth.get("policy_results") or {}).get("allowed")
            denied = "permission denied" in error or allowed is False or ("/login" in path_ and bool(error))
            rows.append({
                "time": rec.get("time", ""),
                "who": auth.get("display_name") or "(unauthenticated)",
                "policies": ",".join(auth.get("policies") or []),
                "operation": req.get("operation", ""),
                "path": path_,
                "remote": req.get("remote_address", ""),
                "result": "DENIED" if denied else ("ERROR" if error else "ALLOWED"),
                "error": error.replace("\n", " ").replace("\t", "").strip(),
            })
    return rows


def _table(rows, cols):
    out = ["| " + " | ".join(c.title() for c in cols) + " |",
           "|" + "---|" * len(cols)]
    for r in rows:
        out.append("| " + " | ".join(str(r[c]).replace("|", "\\|") for c in cols) + " |")
    return "\n".join(out)


def build_report(rows, source):
    denied = [r for r in rows if r["result"] == "DENIED"]
    root = [r for r in rows if "root" in r["policies"].split(",")]
    lines = [
        "# Vault Audit Evidence Report", "",
        f"Source log: `{source}`  ",
        f"Window: {rows[0]['time'] if rows else '-'} to {rows[-1]['time'] if rows else '-'}", "",
        "## Summary", "",
        f"- Requests: **{len(rows)}**",
        f"- Allowed: **{sum(r['result'] == 'ALLOWED' for r in rows)}**",
        f"- Denied: **{len(denied)}**",
        f"- Requests made with the root token: **{len(root)}**"
        + ("  <- review: day-to-day work should use named identities" if root else ""),
        "", "## Activity by identity (WHO)", "",
        "| Identity | Policies | Allowed | Denied |", "|---|---|---|---|",
    ]
    by_who = {}
    for r in rows:
        d = by_who.setdefault(r["who"], {"policies": r["policies"], "c": Counter()})
        d["c"][r["result"]] += 1
    for who, d in sorted(by_who.items()):
        lines.append(f"| {who} | {d['policies']} | {d['c']['ALLOWED']} | {d['c']['DENIED']} |")
    lines += ["", "## Denied requests", ""]
    lines.append(_table(denied, ["time", "who", "operation", "path", "error"])
                 if denied else "_None in this window._")
    lines += ["", "## Full trail (WHO / WHAT / WHEN / RESULT)", "",
              _table(rows, ["time", "who", "operation", "path", "result"]), ""]
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("audit_log")
    p.add_argument("-o", "--output", help="write Markdown here instead of stdout")
    p.add_argument("--denied-only", action="store_true")
    p.add_argument("--include-noise", action="store_true",
                   help="keep sys/internal/ui/* CLI preflight requests")
    args = p.parse_args(argv)

    rows = parse_log(args.audit_log, args.include_noise)
    if args.denied_only:
        rows = [r for r in rows if r["result"] == "DENIED"]
    report = build_report(rows, args.audit_log)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"wrote {args.output} ({len(rows)} requests)")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
