# Historical evidence index

This directory is an index, not a second asset owner. It points to the exact
packaged inputs and frozen review surfaces already owned by this repository.
The viewer and tests use those canonical paths directly, so this index does not
copy or rewrite the XP bytes, anchor map, or evidence corpus.

## Complete packaged surface

| Evidence | Canonical owner | Inventory |
| --- | --- | --- |
| XP inputs | [`assets/sprites/`](../../assets/sprites/) | 115 packaged `.xp` files |
| Body-region/source-layer map | [`player-1100-anchors.json`](../../docs/research/ascii/semantic_maps/player-1100-anchors.json) | 8 directional frames; reviewed `armor`→L3 and `helmet`→L4 regions |
| Review cards | [`layer_evidence_cards.jsonl`](../../docs/research/ascii/semantic_maps/layer_evidence_cards.jsonl) | source-owned card rows; query `source_key` and `hand` fields |

The anchor map gives the frame-local body-region rectangles. The evidence-card
`hand.corrected_label`, `hand.note`, and `hand.source_row_verbatim` fields retain
historical handwritten/reviewer terminology where present. Those labels are
provenance evidence and are not engine-role authority.

The normalized viewer exposes the complete packaged XP corpus through raw
sprite/layer dump mode. The default fixture exposes the complete
anchor/evidence relationship through region, angle, frame, grid, and UV
navigation. Run `./run-inspector.sh` to inspect it; run
`./run-inspector.sh --once` for a deterministic text surface.

The companion machine-readable inventory records the expected count, hashes,
and canonical evidence paths without duplicating the corpus.

## Source-layer contract inputs

The source-layer view uses the same XP files and review cards listed above,
plus the following original input owners:

| Evidence | Canonical owner |
| --- | --- |
| Frozen cell contract, 115 XP files / 573 raw layers | [`upstream_xp_cell_contract/`](../research/ascii/semantic_maps/upstream_xp_cell_contract/) |
| Layer decisions | [`source_layer_review_decisions.jsonl`](../research/ascii/semantic_maps/source_layer_review_decisions.jsonl) |
| Manual candidate review | [`manual_candidate_review.json`](../research/ascii/semantic_maps/manual_candidate_review.json) |
| Family topology | [`family_topology_contracts.json`](../research/ascii/semantic_maps/family_topology_contracts.json) |
| Source identities | [`provenance.md`](../provenance.md) |

Run `./run-viewer.sh` for interactive inspection or `./run-viewer.sh --once`
for deterministic text output. The single machine-readable manifest in this
directory binds both views, all 115 asset hashes, the frozen contract totals,
and each indexed input's SHA-256. The two original index versions remain
available in the preserved pre-consolidation Git history.
