#!/usr/bin/env python3
"""Local, opt-in project memory and compact context packer for MDCP.

Uses only Python's standard library. It does not connect to or write to AI-provider
private memory. Keep secrets and personal data out of saved notes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_FILES = (
    "MDCP_CONTEXT.md",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "docs/UNIVERSAL_AI_ARCHITECTURE.md",
    "docs/TOKEN_EFFICIENCY_AND_MEMORY.md",
)
DB_RELATIVE = Path(".mdcp") / "memory.sqlite3"


def database(root: Path) -> sqlite3.Connection:
    folder = root / ".mdcp"
    folder.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(folder / "memory.sqlite3")
    db.execute("""CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        category TEXT NOT NULL,
        title TEXT NOT NULL,
        body TEXT NOT NULL,
        digest TEXT NOT NULL UNIQUE
    )""")
    db.commit()
    return db


def remember(root: Path, title: str, body: str, category: str) -> int:
    title, body = title.strip(), body.strip()
    if not title or not body:
        raise ValueError("title and body must not be empty")
    digest = hashlib.sha256((category + "\0" + title + "\0" + body).encode()).hexdigest()
    with database(root) as db:
        cur = db.execute(
            "INSERT OR IGNORE INTO memories(created_at,category,title,body,digest) VALUES(?,?,?,?,?)",
            (datetime.now(timezone.utc).isoformat(), category, title, body, digest),
        )
        row = db.execute("SELECT id FROM memories WHERE digest=?", (digest,)).fetchone()
        return int(row[0]) if row else int(cur.lastrowid or 0)


def search(root: Path, query: str, limit: int = 10) -> list[tuple]:
    with database(root) as db:
        return db.execute(
            """SELECT id,created_at,category,title,body FROM memories
               WHERE title LIKE ? OR body LIKE ? ORDER BY id DESC LIMIT ?""",
            (f"%{query}%", f"%{query}%", limit),
        ).fetchall()


def pack(root: Path, max_chars: int = 12000, query: str = "", files: tuple[str, ...] = DEFAULT_FILES) -> str:
    if max_chars < 500:
        raise ValueError("max_chars must be at least 500")
    chunks: list[str] = ["# MDCP Compact Project Context\n"]
    remaining = max_chars
    for rel in files:
        path = root / rel
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8", errors="replace").strip()
        if not content:
            continue
        block = f"\n## Source: {rel}\n{content}\n"
        if len(block) > remaining:
            block = block[:remaining] + "\n[truncated to context budget]\n"
        chunks.append(block)
        remaining -= len(block)
        if remaining <= 0:
            break
    if remaining > 0:
        rows = search(root, query, 8) if query else _recent(root, 8)
        if rows:
            block = "\n## Saved project memories\n"
            for _id, created, category, title, body in rows:
                item = f"\n### [{category}] {title} ({created[:10]})\n{body}\n"
                if len(item) > remaining:
                    break
                block += item
                remaining -= len(item)
            chunks.append(block)
    return "".join(chunks)[:max_chars]


def _recent(root: Path, limit: int) -> list[tuple]:
    with database(root) as db:
        return db.execute(
            "SELECT id,created_at,category,title,body FROM memories ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("remember", help="save a concise project decision")
    add.add_argument("title")
    add.add_argument("body")
    add.add_argument("--category", default="decision")
    find = sub.add_parser("search", help="search saved memories")
    find.add_argument("query")
    find.add_argument("--limit", type=int, default=10)
    build = sub.add_parser("pack", help="build a bounded context pack")
    build.add_argument("--max-chars", type=int, default=12000)
    build.add_argument("--query", default="")
    export = sub.add_parser("export", help="export memories as JSON")
    forget = sub.add_parser("forget", help="delete one memory by ID")
    forget.add_argument("id", type=int)
    args = parser.parse_args()
    root = args.root.resolve()
    if args.command == "remember":
        print(remember(root, args.title, args.body, args.category))
    elif args.command == "search":
        for row in search(root, args.query, args.limit):
            print(json.dumps(dict(id=row[0], created_at=row[1], category=row[2], title=row[3], body=row[4]), ensure_ascii=False))
    elif args.command == "pack":
        sys.stdout.write(pack(root, args.max_chars, args.query))
    elif args.command == "export":
        with database(root) as db:
            rows = db.execute("SELECT id,created_at,category,title,body FROM memories ORDER BY id").fetchall()
        print(json.dumps([dict(id=r[0], created_at=r[1], category=r[2], title=r[3], body=r[4]) for r in rows], indent=2, ensure_ascii=False))
    elif args.command == "forget":
        with database(root) as db:
            cur = db.execute("DELETE FROM memories WHERE id=?", (args.id,))
        print("deleted" if cur.rowcount else "not found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
