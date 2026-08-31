# Historical evidence index

This directory is an index, not a second asset owner. It points to the exact
packaged inputs and frozen review surfaces already owned by this repository.
The viewer and tests use those canonical paths directly, so this index does not
copy or rewrite the XP bytes, anchor map, or evidence corpus.

## Complete packaged surface

| Evidence | Canonical owner | Inventory |
| --- | --- | --- |
| XP input | [`assets/sprites/`](../../assets/sprites/) | 1 file: `player-1100.xp` |
| Body-region/source-layer map | [`player-1100-anchors.json`](../../docs/research/ascii/semantic_maps/player-1100-anchors.json) | 8 directional frames; reviewed `armor`→L3 and `helmet`→L4 regions |
| Review cards | [`layer_evidence_cards.jsonl`](../../docs/research/ascii/semantic_maps/layer_evidence_cards.jsonl) | source-owned card rows; query `source_key` and `hand` fields |

The anchor map gives the frame-local body-region rectangles. The evidence-card
`hand.corrected_label`, `hand.note`, and `hand.source_row_verbatim` fields retain
historical handwritten/reviewer terminology where present. Those labels are
provenance evidence and are not engine-role authority.

The normalized viewer exposes the complete packaged XP input through its
default fixture and the complete anchor/evidence relationship through region,
angle, frame, grid, and UV navigation. Run `./run-inspector.sh` to inspect it;
run `./run-inspector.sh --once` for a deterministic text surface.

The companion machine-readable inventory records the expected count, hashes,
and canonical evidence paths without duplicating the corpus.
