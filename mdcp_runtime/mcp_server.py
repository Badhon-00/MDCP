"""Optional MCP stdio server. Run as python -m mdcp_runtime.mcp_server."""
from __future__ import annotations

import json
import os
from pathlib import Path

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:
    raise SystemExit('MDCP MCP server requires the optional dependency: pip install "mdcp-agent-fabric[mcp]"') from exc

from .skills import discover_skills, skill_context
from .tasks import TaskRunner

mcp = FastMCP("MDCP Agent Runtime", json_response=True)
runner = TaskRunner.from_env()
repo_root = Path(os.getenv("MDCP_REPO_ROOT", Path.cwd())).expanduser().resolve()


@mcp.tool()
def mdcp_task_start(task: str, context: str = "") -> dict:
    """Start a durable API-backed task. It continues while this MCP server stays running."""
    selected_skills = skill_context(repo_root, task)
    combined_context = "\n\n".join(part for part in (context, selected_skills) if part)
    task_id = runner.submit(task, combined_context)
    return {
        "task_id": task_id,
        "status": "queued",
        "skills_attached": bool(selected_skills),
        "note": "Poll mdcp_task_status for completion. This worker returns model output; it does not edit files or run shell commands.",
    }


@mcp.tool()
def mdcp_task_status(task_id: str) -> dict:
    """Read the persisted status and result of an MDCP task."""
    result = runner.status(task_id)
    return result or {"error": "task_not_found", "task_id": task_id}


@mcp.tool()
def mdcp_task_resume(task_id: str) -> dict:
    """Retry a failed or cancelled task using the configured provider fallback chain."""
    return {"task_id": task_id, "resumed": runner.resume(task_id)}


@mcp.tool()
def mdcp_task_cancel(task_id: str) -> dict:
    """Request cancellation of a queued or running task."""
    return {"task_id": task_id, "cancel_requested": runner.cancel(task_id)}


@mcp.tool()
def mdcp_skill_search(query: str = "", limit: int = 10) -> list[dict]:
    """Find relevant MDCP skills by name or description without executing them."""
    return discover_skills(repo_root, query, limit)


@mcp.tool()
def mdcp_plugin_manifest() -> dict:
    """Read the repository's Claude plugin manifest as metadata."""
    manifest = repo_root / ".claude-plugin" / "plugin.json"
    if not manifest.is_file():
        return {"error": "plugin_manifest_not_found"}
    return json.loads(manifest.read_text(encoding="utf-8"))


if __name__ == "__main__":
    mcp.run(transport="stdio")
