#!/usr/bin/env python3
"""Generate a deterministic structural report for MDCP skills."""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRONT = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def inspect(folder):
    file = folder / "SKILL.md"
    row = {"folder": folder.name, "name": "", "description_length": 0,
           "body_characters": 0, "headings": 0, "local_links": 0,
           "broken_local_links": [], "status": "ok", "warnings": [], "errors": []}
    if not file.is_file():
        row["errors"].append("Missing SKILL.md")
    else:
        source = file.read_text(encoding="utf-8", errors="replace")
        match = FRONT.match(source)
        metadata = match.group(1) if match else ""
        body = FRONT.sub("", source, count=1) if match else source
        name = re.search(r"^name:\s*(.*?)\s*$", metadata, re.M)
        desc = re.search(r"^description:\s*(.*?)(?=^\S[^:]*:|\Z)", metadata, re.M | re.S)
        row["name"] = name.group(1).strip().strip("\\\"'") if name else ""
        description = desc.group(1).strip().strip("\\\"'") if desc else ""
        row["description_length"] = len(description)
        row["body_characters"] = len(body.strip())
        row["headings"] = len(re.findall(r"^#{1,6}\s+", body, re.M))
        if not match:
            row["errors"].append("Missing YAML frontmatter")
        if not row["name"]:
            row["errors"].append("Missing frontmatter name")
        elif row["name"] != folder.name:
            row["errors"].append("Frontmatter name does not match folder")
        if len(description) < 30:
            row["errors"].append("Description is missing or shorter than 30 characters")
        if len(body.strip()) < 120:
            row["warnings"].append("Short body; add actionable instructions")
        if row["headings"] == 0:
            row["warnings"].append("No Markdown headings")
        for raw in LINK.findall(body):
            target = raw.strip().split("#", 1)[0]
            if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("//"):
                continue
            row["local_links"] += 1
            candidate = (folder / target).resolve()
            try:
                candidate.relative_to(ROOT.resolve())
            except ValueError:
                row["broken_local_links"].append(target)
                continue
            if not candidate.exists():
                row["broken_local_links"].append(target)
        if row["broken_local_links"]:
            row["errors"].append("Broken local links: " + ", ".join(row["broken_local_links"]))
    if row["errors"]:
        row["status"] = "error"
    elif row["warnings"]:
        row["status"] = "warning"
    return row


def report(rows):
    errors = sum(x["status"] == "error" for x in rows)
    warnings = sum(x["status"] == "warning" for x in rows)
    lines = ["# MDCP Skill Health Report", "",
             "- Skills inspected: **%d**" % len(rows),
             "- Errors: **%d**" % errors, "- Warnings: **%d**" % warnings, "",
             "| Skill | Status | Description chars | Body chars | Headings | Local links |",
             "|---|---|---:|---:|---:|---:|"]
    for x in rows:
        lines.append("| %s | %s | %d | %d | %d | %d |" %
                     (x["folder"], x["status"], x["description_length"],
                      x["body_characters"], x["headings"], x["local_links"]))
    findings = [x for x in rows if x["errors"] or x["warnings"]]
    if findings:
        lines += ["", "## Findings", ""]
        for x in findings:
            lines += ["### " + x["folder"]]
            lines += ["- **Error:** " + e for e in x["errors"]]
            lines += ["- Warning: " + w for w in x["warnings"]]
            lines.append("")
    lines += ["## Scope", "",
              "This is a structural documentation check, not a security audit, quality guarantee,",
              "license review, or proof of host-platform compatibility."]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--check", action="store_true", help="Fail when structural errors exist")
    args = parser.parse_args()
    rows = [inspect(p) for p in sorted((ROOT / "skills").iterdir()) if p.is_dir()]
    errors = sum(x["status"] == "error" for x in rows)
    if args.format == "json":
        print(json.dumps({"total": len(rows), "errors": errors, "skills": rows}, indent=2))
    else:
        print(report(rows), end="")
    return 1 if args.check and errors else 0


if __name__ == "__main__":
    sys.exit(main())
