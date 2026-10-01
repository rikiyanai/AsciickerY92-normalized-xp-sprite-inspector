# Provenance

The three Python modules were extracted from private pipeline-v3 commit `7fdecabf44175d25d3793335dee4d38e8b089a81`, where the read-only XP parser was isolated. Their extracted SHA-256 identities were:

| File | SHA-256 before standalone root adjustment |
| --- | --- |
| `source_layer_contract_viewer.py` | `bf306419987d5cfc3367bd78cdf416ad27e2f7399f68f1b8bbac29ca640f489b` |
| `source_layer_contract_read_model.py` | `94c0441d0378b2646d5acbbbd5e71ffba4380909e3991ad861e9dbeca092fcce` |
| `xp_read_model.py` | `f2ed6a03d8ca906cb60581709a60ac2a9666802153da206c34462f405ac19af3` |

The standalone adjustment changes `REPO_ROOT` from a nested pipeline checkout to this repository root. The viewer also adds a local `--compact` read-only display that limits the animation panel to three adjacent frames while keeping the selected raw layer, composition, assigned-cell count, and read-only boundary visible together.

The viewer does not write artifacts or change the parser, XP bytes, ledger decisions, compiler state, or runtime state. It is therefore a maintained standalone inspection surface rather than a byte-identical copy of the original viewer module.

All 115 XP files and all contract data other than the three derived files below were copied byte-for-byte from the Y9-2 checkout observed at `242ecba44f76ed1120dadf06653fd6de47017b7f`.

The frozen manifest's former absolute Desktop source path was replaced with the non-resolving `historical-source:` provenance label. The source-state SHA-256 inside that record was preserved. The manifest hash changed from `80de2a53...` to `1c2cfcae...`; the dependent family-freeze hash was updated to `36f73a64...`, and `compiler_cutover.json` was updated to bind that derived freeze. No review decision, source key, XP byte, count, or authority field was changed.

This repository is published as a standalone inspection tool derived through Asciicker Y9-2. The upstream Asciicker project is credited in the repository README.

The complete packaged-input and hand-label inventory is maintained as an
index in [`docs/historical-evidence/`](historical-evidence/). It points to the
115 existing XP files, frozen manifest, family freeze, and review-decision
owners without duplicating or mutating the frozen corpus. The recording recipe
now captures seven full-canvas held states, including three adjacent animation
frames, before assembling the fast-review GIF at 0.55 seconds per state.
