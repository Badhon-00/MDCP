#!/usr/bin/env python3
import argparse, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(); p.add_argument("--output",default="dist/mdcp-skills.zip"); args=p.parse_args()
out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
    for skill in (ROOT/"skills").glob("*/SKILL.md"):
        folder=skill.parent
        for f in folder.rglob("*"):
            if f.is_file(): z.write(f,f.relative_to(ROOT))
    for name in ["THIRD_PARTY_NOTICES.md","docs/CROSS_PLATFORM_SKILLS.md","AGENTS.md"]:
        f=ROOT/name
        if f.exists(): z.write(f,f.relative_to(ROOT))
print(f"Created {out}")
