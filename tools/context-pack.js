#!/usr/bin/env node
// Cross-platform launcher for the Python context packer.
const { spawnSync } = require("node:child_process");
const python = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const result = spawnSync(python, [require("node:path").join(__dirname, "mdcp_memory.py"), ...process.argv.slice(2)], {
  cwd: process.cwd(), stdio: "inherit"
});
if (result.error) {
  console.error("Could not start Python:", result.error.message);
  process.exit(1);
}
process.exit(result.status ?? 1);
