#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
command -v python3 >/dev/null 2>&1 || {
  echo "python3 is required" >&2
  exit 69
}

exec python3 "$repo_root/scripts/source_layer_contract_viewer.py" "$@"
