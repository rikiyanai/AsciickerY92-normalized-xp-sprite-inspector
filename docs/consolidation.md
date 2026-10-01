# Source-layer viewer consolidation

On October 1, 2026, the operator requested that the public source-layer viewer
be absorbed into the normalized XP sprite inspector and its separate GitHub
repository be deleted.

## Preserved identities

- Destination: `rikiyanai/AsciickerY92-normalized-xp-sprite-inspector`,
  original main `3f87bcbbf3cfb5d784dc9643f6e5858f15ba4510`.
- Source: `rikiyanai/AsciickerY92-source-layer-contract-viewer`,
  original main `7fed3cceccb1bbea0aab4d12bab608c5ac1a9f38`.
- The consolidation is a two-parent merge, not a copied snapshot or rewritten
  history. Every source main commit remains reachable from destination main.
- All 115 shared XP assets and the shared review-card file were byte-identical
  at intake and are stored at their existing paths without duplication.

## Retained surfaces

The normalized entry point remains `run-inspector.sh`; the source-layer entry
point remains `run-viewer.sh`. Source parser/read-model modules, frozen review
inputs, recording builder, tape and both GIFs retain their original bytes.
The parser is renamed from `scripts/xp_read_model.py` to
`scripts/source_layer_xp_read_model.py` and the source viewer's import follows
that name. This avoids reviving the destination's retired generic-proxy
filename; the normalized guard is unchanged. Other imported runtime paths
are unchanged. Source tests move from `tests/test_contract.py` to
`tests/test_source_layer_contract.py`, with only the unified evidence-index
lookup adapted to the destination's hashed-entry format.

`docs/FAILURE_LOG.md` retains both original development logs. The README
exposes both views. `docs/historical-evidence/manifest.json` is one combined
index, retaining all asset hashes and source frozen-contract fields, with
hashed references to both sets of inputs. CI discovers both test modules.

## Recovery and deletion boundary

The source repository's original main tree can be recovered from destination
history using `git show 7fed3cceccb1bbea0aab4d12bab608c5ac1a9f38:<path>`.
To reconstruct the former checkout in a new, explicitly chosen directory,
clone the destination and check out that source commit.

Before deletion, inspect both entry points, run both test suites, verify
the unchanged imported blobs, push the merge to destination main, and read
back its exact SHA and source-commit ancestry from GitHub. At intake GitHub
reported no source issues, forks, stars, releases, wiki, Pages or discussions;
its only remote branch was main. The local source checkout is not a deletion
target and remains a recovery copy.

GitHub repository deletion removes the old URL and repository-specific
settings/Actions records; the preserved Git history does not recreate those
service records. The private life-log receipt owns the deletion response
and final readback, not this pre-deletion migration contract.
