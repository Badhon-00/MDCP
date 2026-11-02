from __future__ import annotations
import argparse, json, sys, zipfile
from pathlib import Path
from .core import context_pack, search_repositories, run_agents
ROOT=Path(__file__).resolve().parent.parent

def main():
    p=argparse.ArgumentParser(prog="mdcp-fabric",description="Portable skills, public repository discovery and bounded parallel model analysis.")
    sub=p.add_subparsers(dest="cmd",required=True)
    s=sub.add_parser("search",help="search public GitHub repositories concurrently"); s.add_argument("queries",nargs="+"); s.add_argument("--limit",type=int,default=30); s.add_argument("--workers",type=int,default=8); s.add_argument("--output")
    c=sub.add_parser("context",help="build a bounded local context pack"); c.add_argument("root",nargs="?",default="."); c.add_argument("--max-chars",type=int,default=12000); c.add_argument("--max-files",type=int,default=100); c.add_argument("--output")
    a=sub.add_parser("analyze",help="run specialist analysis using an OpenAI-compatible endpoint"); a.add_argument("root",nargs="?",default="."); a.add_argument("--agents",type=int,default=8); a.add_argument("--max-parallel",type=int,default=8); a.add_argument("--max-files",type=int,default=100); a.add_argument("--max-chars",type=int,default=50000); a.add_argument("--roles",nargs="*"); a.add_argument("--output",default=".mdcp/reports/agent-fabric.json")
    args=p.parse_args()
    if args.cmd=="search":
        repos,errors=search_repositories(args.queries,args.limit,args.workers); result={"repositories":repos,"errors":errors}
        raw=json.dumps(result,indent=2,ensure_ascii=False); print(raw)
        if args.output: Path(args.output).write_text(raw+"\n")
    elif args.cmd=="context":
        text,manifest=context_pack(Path(args.root).resolve(),args.max_chars,args.max_files)
        if args.output:
            out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(text); print(json.dumps({"output":str(out),"files":len(manifest),"chars":len(text)}))
        else: sys.stdout.write(text)
    else:
        roles=args.roles or [r["id"] for r in json.loads((ROOT/"agents/roles.json").read_text())["roles"][:args.agents]]
        result=run_agents(Path(args.root).resolve(),roles,args.agents,args.max_parallel,args.max_files,args.max_chars)
        out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
        print(json.dumps({"output":str(out),"executed_agents":result["executed_agents"],"workers":result["workers"],"elapsed_seconds":result["elapsed_seconds"]}))
if __name__=="__main__": main()
