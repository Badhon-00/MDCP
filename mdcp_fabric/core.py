from __future__ import annotations
import concurrent.futures, hashlib, json, os, re, time, urllib.parse, urllib.request
from pathlib import Path
from datetime import datetime, timezone

MAX_WORKERS = 64
SKIP_DIRS = {".git","node_modules","vendor","dist","build","coverage","__pycache__",".venv","venv",".next",".nuxt","target",".idea",".mdcp"}
SECRET_PARTS = {".env","id_rsa","id_ed25519","credentials","secrets"}
TEXT_SUFFIXES = {".py",".js",".jsx",".ts",".tsx",".mjs",".cjs",".json",".yaml",".yml",".toml",".ini",".md",".mdx",".html",".css",".scss",".sql",".go",".rs",".java",".kt",".swift",".php",".rb",".sh",".ps1",".c",".h",".cpp",".cs",".xml",".gradle",".dockerfile"}
ROLES_PATH = Path(__file__).resolve().parent.parent / "agents" / "roles.json"
PROMPT_PATH = Path(__file__).resolve().parent.parent / "agents" / "SYSTEM_PROMPT.md"

def _safe_path(p: Path) -> bool:
    name=p.name.lower()
    if any(x in name for x in SECRET_PARTS) or name.endswith((".pem",".key",".p12",".pfx")): return False
    return p.suffix.lower() in TEXT_SUFFIXES or name in {"dockerfile","makefile","procfile"}

def inventory(root: Path, max_files=160, max_file_bytes=24000):
    out=[]
    for base, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
        for name in sorted(names):
            p=Path(base)/name
            if not _safe_path(p): continue
            try:
                size=p.stat().st_size
                if size<=0 or size>max_file_bytes: continue
                raw=p.read_bytes()
                text=raw.decode("utf-8")
                if "\x00" in text: continue
                out.append({"path":p.relative_to(root).as_posix(),"size":size,"sha256":hashlib.sha256(raw).hexdigest(),"text":text})
            except (OSError,UnicodeError): continue
            if len(out)>=max_files: return out
    return out

def context_pack(root: Path, max_chars=12000, max_files=100):
    files=inventory(root,max_files=max_files)
    chunks=[f"# MDCP Context Pack\nRoot: {root.resolve()}\nGenerated: {datetime.now(timezone.utc).isoformat()}\n"]
    used=sum(map(len,chunks))
    for f in files:
        header=f"\n## {f['path']} (sha256:{f['sha256'][:12]})\n"
        room=max_chars-used-len(header)
        if room<=0: break
        body=f["text"][:room]
        chunks.append(header+body)
        used+=len(header)+len(body)
        if len(body)<len(f["text"]): break
    return "".join(chunks), [{"path":f["path"],"sha256":f["sha256"],"size":f["size"]} for f in files]

def _github_search(query, token=None, timeout=15):
    params=urllib.parse.urlencode({"q":query,"sort":"stars","order":"desc","per_page":30})
    req=urllib.request.Request("https://api.github.com/search/repositories?"+params,headers={"Accept":"application/vnd.github+json","User-Agent":"MDCP-Agent-Fabric/0.3"})
    if token: req.add_header("Authorization","Bearer "+token)
    with urllib.request.urlopen(req,timeout=timeout) as res: return json.loads(res.read().decode())

def search_repositories(queries, limit=30, workers=8):
    workers=max(1,min(int(workers),MAX_WORKERS))
    token=os.getenv("GITHUB_TOKEN")
    results={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures={pool.submit(_github_search,q,token):q for q in queries}
        for fut in concurrent.futures.as_completed(futures):
            q=futures[fut]
            try:
                payload=fut.result()
                for item in payload.get("items",[]):
                    results[item["full_name"].lower()]={"name":item["full_name"],"url":item["html_url"],"description":item.get("description") or "","stars":item.get("stargazers_count",0),"language":item.get("language"),"updated_at":item.get("updated_at"),"query":q}
            except Exception as exc:
                results["error:"+q]={"query":q,"error":str(exc)}
    repos=[v for k,v in results.items() if not k.startswith("error:")]
    repos.sort(key=lambda x:(x["stars"],x["updated_at"] or ""),reverse=True)
    return repos[:limit],[v for k,v in results.items() if k.startswith("error:")]

def _chat_completion(base_url, api_key, model, system, user, timeout=90):
    url=base_url.rstrip("/")+"/chat/completions"
    payload={"model":model,"temperature":0.1,"messages":[{"role":"system","content":system},{"role":"user","content":user}]}
    data=json.dumps(payload).encode()
    req=urllib.request.Request(url,data=data,headers={"Content-Type":"application/json","Authorization":"Bearer "+api_key,"User-Agent":"MDCP-Agent-Fabric/0.3"})
    with urllib.request.urlopen(req,timeout=timeout) as res: body=json.loads(res.read().decode())
    return body["choices"][0]["message"]["content"]

def run_agents(root: Path, roles, agents=8, max_parallel=8, max_files=100, max_chars=50000):
    base=os.getenv("MDCP_LLM_BASE_URL","").strip()
    key=os.getenv("MDCP_LLM_API_KEY","").strip()
    model=os.getenv("MDCP_LLM_MODEL","").strip()
    if not base or not key or not model: raise RuntimeError("Set MDCP_LLM_BASE_URL, MDCP_LLM_API_KEY and MDCP_LLM_MODEL.")
    roles_data=json.loads(ROLES_PATH.read_text())
    known={r["id"]:r for r in roles_data["roles"]}
    selected=[known[r] for r in roles if r in known]
    if not selected: raise ValueError("No valid roles selected.")
    n=min(max(1,int(agents)),len(selected),MAX_WORKERS)
    parallel=max(1,min(int(max_parallel),n,MAX_WORKERS))
    files=inventory(root,max_files=max_files)
    # Share bounded inventory; cap aggregate prompt size to avoid accidental huge context uploads.
    excerpts=[]; used=0
    for f in files:
        block=f"\n### {f['path']}\n{f['text'][:5000]}\n"
        if used+len(block)>max_chars: break
        excerpts.append(block); used+=len(block)
    prompt= PROMPT_PATH.read_text()
    evidence="".join(excerpts)
    def one(role):
        task=json.dumps({"role":role["id"],"focus":role["focus"],"repository_files":evidence},ensure_ascii=False)
        try:
            raw=_chat_completion(base,key,model,prompt,task)
            try: parsed=json.loads(raw)
            except json.JSONDecodeError: parsed={"role":role["id"],"summary":"Model response was not valid JSON","raw_excerpt":raw[:6000],"findings":[]}
            return {"role":role["id"],"ok":True,"result":parsed}
        except Exception as exc: return {"role":role["id"],"ok":False,"error":str(exc)}
    started=time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as pool:
        outputs=list(pool.map(one,selected[:n]))
    return {"generated_at":datetime.now(timezone.utc).isoformat(),"model":model,"workers":parallel,"requested_agents":agents,"executed_agents":len(outputs),"files_considered":len(files),"elapsed_seconds":round(time.monotonic()-started,2),"results":outputs}
