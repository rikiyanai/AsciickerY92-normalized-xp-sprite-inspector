#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
viewer="$repo_dir/scripts/xp_uv_body_viewer.py"
anchor="$repo_dir/docs/research/ascii/semantic_maps/player-1100-anchors.json"
sprites="$repo_dir/assets/sprites"

if [ "$#" -eq 0 ]; then
  exec python3 "$viewer" --sprite-dir "$sprites" --anchor-review "$anchor"
fi
if [ "$#" -eq 1 ] && [ "$1" = "--once" ]; then
  exec python3 "$viewer" --sprite-dir "$sprites" --anchor-once "$anchor"
fi
exec python3 "$viewer" --sprite-dir "$sprites" "$@"
