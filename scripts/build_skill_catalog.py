#!/usr/bin/env python3
"""Build a searchable JSON catalog from MDCP skill frontmatter."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
OUTPUT = ROOT / "site" / "catalog.json"

CATEGORY_RULES = [
    ("AI Agents & MCP", ("agent", "mcp", "claude", "codex", "llm", "prompt", "skill")),
    ("Backend & APIs", ("api", "backend", "server", "database", "auth", "node", "python")),
    ("Frontend & UI", ("frontend", "react", "next", "css", "design", "ui", "web", "three")),
    ("Security", ("security", "audit", "hardening", "crypto", "privacy")),
    ("DevOps & Workflow", ("devops", "deploy", "docker", "git", "workflow", "testing", "automation")),
]

def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.S)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        item = re.match(r"^(name|description):\s*(.*?)\s*$", line)
        if item:
            result[item.group(1)] = item.group(2).strip().strip('"').strip("'")
    return result

def category(name: str, description: str) -> str:
    haystack = f"{name} {description}".lower()
    for label, terms in CATEGORY_RULES:
        if any(term in haystack for term in terms):
            return label
    return "Developer Tools"

def main() -> None:
    items = []
    for file in sorted(SKILLS.glob("*/SKILL.md")):
        meta = frontmatter(file.read_text(encoding="utf-8"))
        name = meta.get("name") or file.parent.name
        description = meta.get("description", "")
        items.append({
            "name": name,
            "description": description,
            "category": category(name, description),
            "path": f"skills/{file.parent.name}/SKILL.md",
            "url": f"https://github.com/Badhon-00/MDCP/blob/main/skills/{file.parent.name}/SKILL.md",
            "raw": f"https://raw.githubusercontent.com/Badhon-00/MDCP/main/skills/{file.parent.name}/SKILL.md",
        })
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps({
        "repository": "Badhon-00/MDCP",
        "generated_from": "skills/*/SKILL.md",
        "count": len(items),
        "skills": items,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(items)} skills -> {OUTPUT.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
