# Attribution and provenance

Private source repository: `rikiyanai/asciicker-Y9-2`.

| Standalone path | Source identity | SHA-256 |
| --- | --- | --- |
| `scripts/xp_read_model.py` | `pipeline-v3/scripts/xp_read_model.py` at pipeline commit `7fdecabf44175d25d3793335dee4d38e8b089a81` | `f2ed6a03d8ca906cb60581709a60ac2a9666802153da206c34462f405ac19af3` |
| `assets/player-nude.xp` | `assets/sprites/player-nude.xp` at Y9-2 commit `242ecba44f76ed1120dadf06653fd6de47017b7f` | `5054a77f6d991b58e4e3fb326e71eea1d03135fd30127348ba4ee7be1cd8e39c` |

`scripts/normalized_xp_inspector.py` is a standalone read-only adapter written
for this repository. It implements only metadata inspection and terminal
preview over the parser model above. The mutation-capable parent
`pipeline-v3/scripts/xp_uv_body_viewer.py` is intentionally excluded.

No third-party library is bundled. Python's `cp437` codec is used for terminal
preview. Public visibility remains subject to the source repository's asset
ownership decision; this repository stays private.
