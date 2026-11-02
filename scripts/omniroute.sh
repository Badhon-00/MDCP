#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
MDCP OmniRoute helper

Usage:
  ./scripts/omniroute.sh install       Install the upstream OmniRoute CLI
  ./scripts/omniroute.sh start         Start the gateway
  ./scripts/omniroute.sh doctor        Run upstream diagnostics
  ./scripts/omniroute.sh claude [args] Launch Claude Code through OmniRoute
  ./scripts/omniroute.sh codex [args]  Launch Codex through OmniRoute
  ./scripts/omniroute.sh configure     Open upstream interactive configuration

This helper does not create accounts, obtain API keys, bypass quotas or modify
existing configuration files directly. Review upstream docs first.
EOF
}

command -v npm >/dev/null 2>&1 || { echo "npm is required. Install a supported Node.js release first." >&2; exit 1; }
ACTION="${1:-help}"
shift || true

case "$ACTION" in
  install)
    npm install --global omniroute
    ;;
  start)
    command -v omniroute >/dev/null 2>&1 || { echo "Install first: $0 install"; exit 1; }
    exec omniroute "$@"
    ;;
  doctor)
    exec omniroute doctor "$@"
    ;;
  claude)
    exec omniroute run claude --model "${MDCP_MODEL:-auto/coding}" -- "$@"
    ;;
  codex)
    exec omniroute run codex --model "${MDCP_MODEL:-auto/coding}" -- "$@"
    ;;
  configure)
    exec omniroute configure "${1:-claude}"
    ;;
  help|-h|--help)
    usage
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
