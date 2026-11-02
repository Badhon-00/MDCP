#!/usr/bin/env python3
"""Validate the repo: JSON manifests, every skill's frontmatter, unique names, license notices.
Exit 1 on any error. Used by CI (.github/workflows/validate.yml) and by contributors locally:
  python3 scripts/validate.py
"""
import json, re, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
errors, warnings = [], []

for f in [".claude-plugin/plugin.json", ".claude-plugin/marketplace.json", "mcp/mcp.example.json"]:
    try:
        json.loads((root / f).read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"{f}: invalid JSON ({e})")

names = {}
notices = (root / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8") if (root / "THIRD_PARTY_NOTICES.md").exists() else ""
skills = sorted(p for p in (root / "skills").iterdir() if p.is_dir())
for d in skills:
    f = d / "SKILL.md"
    if not f.exists():
        errors.append(f"{d.name}: missing SKILL.md")
        continue
    text = f.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append(f"{d.name}: no frontmatter")
        continue
    fm = m.group(1)
    n = re.search(r"^name:\s*(.+)$", fm, re.M)
    desc = re.search(r"^description:\s*(.*?)(?=^\S|\Z)", fm, re.M | re.S)
    if not n:
        errors.append(f"{d.name}: frontmatter has no name")
        continue
    name = n.group(1).strip().strip("\"'")
    if name != d.name:
        warnings.append(f"{d.name}: frontmatter name '{name}' differs from folder (kept as published upstream)")
    if name in names:
        errors.append(f"{d.name}: duplicate name also used by {names[name]}")
    names[name] = d.name
    if not desc or len(desc.group(1).strip().lstrip(">|-+ \n")) < 20:
        errors.append(f"{d.name}: description missing or too short")
    elif len(desc.group(1)) > 1024:
        warnings.append(f"{d.name}: description over 1024 characters")
    if d.name not in notices and d.name != "master-developer" and not d.name.startswith("mdcp-"):
        warnings.append(f"{d.name}: not listed in THIRD_PARTY_NOTICES.md (add it, or mark as original)")

ref = root / "skills" / "master-developer" / "references"
if len(list(ref.glob("*"))) < 35:
    errors.append("master-developer/references has fewer than 35 files")

for w in warnings:
    print("warn :", w)
for e in errors:
    print("ERROR:", e)
print(f"{len(skills)} skills checked, {len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
