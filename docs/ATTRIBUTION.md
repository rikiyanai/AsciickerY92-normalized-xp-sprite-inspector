# Attribution and provenance

Private source repository: `rikiyanai/asciicker-Y9-2`.

The product surface is `pipeline-v3/scripts/xp_uv_body_viewer.py` from the
`pipeline-v3` worktree at commit `9e585bfd68d24b8e8ab442fb467592ec837ef8b0`.
Its upstream SHA-256 before standalone hardening is
`15f1de8f39e9c0a8bc7b098a47d8895d51ae227b17e245e6865b7b57fcbbd279`.
The latest source-owning commit for that path is
`d33756a8738966e8b4570a1e6b42972a720b275b`.

The following bounded dependencies come from the Y9-2 tree at
`a6db2cdc2961e78eea02e79d39b5487d8940c1e9`:

| Standalone path | SHA-256 |
| --- | --- |
| `scripts/cli_style.py` | `6c088459ca6dc308b4fd927ecef1fcd0976c4824debce4dcdc89a89a60ba939c` |
| `scripts/pipeline/xp_core.py` | `3fb74fe296a395313247e53e1c4595602ffb3677554ebf5cd2b2e054d969ef1f` |
| `scripts/pipeline/xp_assets_browser_layer_2_only.py` | `959bde94b509895786df02963a25c20779ca6af7eb3e077b97dc37907bc114f3` |
| `scripts/pipeline/bundle_wizard/semantic_dict.py` | `8a3e4da69fe30b42e1fd704db0ece66df3bc1b3f40bf96db1cea5336befb0afb` |
| `scripts/pipeline/sprite_errors.py` | `615e36bfc0b2b0b8049633fe385f0d4018af0bbdd16a6f0422f2936048704004` |
| `assets/sprites/player-1100.xp` | `9895deede51b6bfe2a0a054b165005d41154962cd1aee37490b04467018de37c` |
| `docs/research/ascii/semantic_maps/player-1100-anchors.json` | `e10427b489055f3eb3c9a8feaab7fb82d74b6877cf326ae5b844603d472e5027` |
| `docs/research/ascii/semantic_maps/layer_evidence_cards.jsonl` | `c39875a33f3f0100be7a53ba1a050ce4b48f57cb585de25e9fd4bcafe9fd00d3` |

Standalone hardening changes are deliberately local and reviewable:

- package-relative source and asset discovery;
- one-shot rendering of the actual anchor-review UV/body screen;
- engine-order composition of the reviewed L2 base, L3 armor, and L4 helmet
  layers in `player-1100.xp`, with region grids bound to each region's recorded
  source layer;
- fail-closed save, assignment, review-decision, and batch-mutation paths; and
- a launcher whose default target is the packaged reviewed anchor map.

The complete packaged-input and hand-label inventory is maintained as an
index in [`docs/historical-evidence/`](historical-evidence/). It points to the
existing XP, anchor, and evidence-card owners and intentionally duplicates no
frozen corpus.

The walkthrough recipe uses the real anchor-review frame controls to expose
three adjacent frames, the L3 armor grid, the L4 helmet grid, and an angle
change. Its generated GIF is captioned and contract-checked after VHS capture;
the caption is presentation evidence and does not alter the product surface.

No third-party Python library is bundled. Public visibility remains subject to
the parent repository's asset-ownership decision; this repository stays private.
