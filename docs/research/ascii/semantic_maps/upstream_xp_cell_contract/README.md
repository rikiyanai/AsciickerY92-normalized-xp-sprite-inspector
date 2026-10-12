# Upstream XP Full-Cell Contract Ledger

This directory contains the full-cell review ledger for the finite actor-visual XP corpus. The generated ledger records proposals and reviewed source-layer decisions; it is not runtime authority and does not replace the original XP files or hand-review records.

`manifest.json` binds six family JSONL shards to the source-state SHA-256 and reports complete layer and cell coverage. Each JSONL row represents one reviewed raw XP layer.

## Cell addressing

Every raw atlas coordinate is covered exactly once. `cell_values` stores exact `(glyph, fg, bg)` values together with the engine cell type, render operation, semantic contributions, and review state. Render behavior and semantic attribution are separate fields.

Each `cell_spans` entry is:

```text
[angle, frame, local_y, local_x_start, length, cell_value_index]
```

Atlas coordinates derive from `frame_geometry`:

```text
atlas_x = frame * frame_width + local_x
atlas_y = angle * frame_height + local_y
```

The compact span encoding is lossless and includes transparent cells. `source_xp.raw_layer_sha256` pins the expanded raw layer bytes.

## Review states

- `layer_role_reviewed_cell_semantics_unverified`: the layer has one reviewed candidate role, but cell-level meaning still needs review.
- `reviewed_composite_cell_assignment_pending`: the layer contains multiple roles and no single role is assigned to every visible cell.
- `rejected_fragment_needs_contract`: the layer is a known fragment whose final source contract remains unresolved.
- `unresolved_hand_evidence`: the corresponding hand-review decision was deliberately withheld.

`review_queue.json` groups all 573 raw layers into 203 exact-fingerprint units. `cell_role_decisions.jsonl` stores the reviewed full-cell assignments. `cell_review_state_decisions.jsonl` records manual findings that reject an incorrect normalized single-role candidate without rewriting the original ledger.

The six-family review covers all 203 exact-fingerprint units, all 573 raw layers, and 6,807,104 raw cells with no pending review units. Composite and contextual layers are kept distinct from clean equipment masks so body, armor, helmet, shield, rider, sword, and crossbow contributions are not collapsed into one layer-wide label.

`semantic_honesty_audit.json` records the corpus-wide equipment review. `family_contract_freeze.json` binds the reviewed cell-role decisions, ledger manifest, topology contracts, source-state hash, and related audit records. Runtime authority remains false; these files describe reviewed source data for inspection and downstream compilation.

## Validation

The ledger is checked in this repository by the test suite: the manifest must
resolve to exactly the 115 packaged XP files, and every file in
`assets/sprites/` must match the SHA-256 recorded for it in the ledger.

```bash
python3 -m unittest discover -s tests -p 'test_source_layer_contract.py' -v
```

The scripts that originally generated the ledger
(`build_upstream_xp_cell_contract_ledger.py` and
`build_upstream_xp_cell_review_queue.py`) live in the private `pipeline-v3`
pipeline and are not shipped here, so the ledger is a frozen, read-only
snapshot in this repository.
