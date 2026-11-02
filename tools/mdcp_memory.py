#!/usr/bin/env python3
"""Opt-in local project memory and bounded context packer. Standard library only."""
import argparse, hashlib, json, sqlite3, sys
from datetime import datetime, timezone
from pathlib import Path

FILES=("MDCP_CONTEXT.md","AGENTS.md","CLAUDE.md","GEMINI.md","docs/UNIVERSAL_AI_ARCHITECTURE.md","docs/TOKEN_EFFICIENCY_AND_MEMORY.md")

def connect(root):
    folder=Path(root)/".mdcp"; folder.mkdir(parents=True,exist_ok=True)
    db=sqlite3.connect(folder/"memory.sqlite3")
    db.execute("CREATE TABLE IF NOT EXISTS memories(id INTEGER PRIMARY KEY, created TEXT NOT NULL, category TEXT NOT NULL, title TEXT NOT NULL, body TEXT NOT NULL, digest TEXT UNIQUE NOT NULL)")
    db.commit(); return db

def remember(root,title,body,category="decision"):
    title,body=title.strip(),body.strip()
    if not title or not body: raise ValueError("title and body are required")
    digest=hashlib.sha256((category+"\0"+title+"\0"+body).encode()).hexdigest()
    with connect(root) as db:
        db.execute("INSERT OR IGNORE INTO memories(created,category,title,body,digest) VALUES(?,?,?,?,?)",(datetime.now(timezone.utc).isoformat(),category,title,body,digest))
        row=db.execute("SELECT id FROM memories WHERE digest=?",(digest,)).fetchone()
    return row[0]

def pack(root,max_chars=12000,query=""):
    if max_chars<500: raise ValueError("max_chars must be >= 500")
    chunks=["# Compact MDCP Context\n"]; remaining=max_chars
    for rel in FILES:
        p=Path(root)/rel
        if not p.is_file(): continue
        block=f"\n## {rel}\n{p.read_text(encoding='utf-8',errors='replace').strip()}\n"
        if len(block)>remaining: block=block[:remaining]+"\n[truncated]\n"
        chunks.append(block); remaining-=len(block)
        if remaining<=0: break
    with connect(root) as db:
        if query: rows=db.execute("SELECT created,category,title,body FROM memories WHERE title LIKE ? OR body LIKE ? ORDER BY id DESC LIMIT 8",(f"%{query}%",f"%{query}%")).fetchall()
        else: rows=db.execute("SELECT created,category,title,body FROM memories ORDER BY id DESC LIMIT 8").fetchall()
    for created,cat,title,body in rows:
        item=f"\n### [{cat}] {title} ({created[:10]})\n{body}\n"
        if len(item)>remaining: break
        chunks.append(item); remaining-=len(item)
    return "".join(chunks)[:max_chars]

def main():
    p=argparse.ArgumentParser(); p.add_argument("--root",type=Path,default=Path.cwd()); sub=p.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("remember"); a.add_argument("title"); a.add_argument("body"); a.add_argument("--category",default="decision")
    a=sub.add_parser("pack"); a.add_argument("--max-chars",type=int,default=12000); a.add_argument("--query",default="")
    a=sub.add_parser("search"); a.add_argument("query"); a.add_argument("--limit",type=int,default=10)
    sub.add_parser("export")
    a=sub.add_parser("forget"); a.add_argument("id",type=int)
    x=p.parse_args(); root=x.root.resolve()
    if x.cmd=="remember": print(remember(root,x.title,x.body,x.category))
    elif x.cmd=="pack": sys.stdout.write(pack(root,x.max_chars,x.query))
    else:
        with connect(root) as db:
            if x.cmd=="search": rows=db.execute("SELECT id,created,category,title,body FROM memories WHERE title LIKE ? OR body LIKE ? ORDER BY id DESC LIMIT ?",(f"%{x.query}%",f"%{x.query}%",x.limit)).fetchall()
            elif x.cmd=="export": rows=db.execute("SELECT id,created,category,title,body FROM memories ORDER BY id").fetchall()
            else: rows=[]; cur=db.execute("DELETE FROM memories WHERE id=?",(x.id,)); print("deleted" if cur.rowcount else "not found")
        if x.cmd in ("search","export"): print(json.dumps(rows,indent=2,ensure_ascii=False))
if __name__=="__main__": main()
