# Normalized-XP UV/Body Inspector

A standalone, read-only terminal inspector for the normalized REXPaint XP
sprite-to-UV/body contract. It packages the real `xp_uv_body_viewer.py` surface,
one reviewed armored player sprite, its anchor map, and the bounded parser/semantic
helpers needed to run independently of the parent repository.

The previous 7x9 layer/frame browser was a product substitution. It and its GIF
were removed; they did not expose any UV/body relationship.

## Run

Python 3.11 or newer is the only dependency.

```sh
./run-inspector.sh
```

The interactive screen relates three views of the selected sprite cell:

- the engine-order composition of base, armor, and helmet layers;
- the focused semantic body region and its cells across angles; and
- atlas-global UV coordinates for every cell in the frame.

Navigation includes arrow keys, `a`/`d` for angle, `w`/`s` for animation,
`,`/`.` for frame, `r`/`f` for region focus, `g` for the angle grid, `b` for a
packaged body-map band when present, and `q` to quit. Assignment, anchor save,
review-decision capture, and batch mutation are blocked in this standalone.

For deterministic non-TTY execution of the same UV/body rendering surface:

```sh
./run-inspector.sh --once
```

## Product boundary and status

This repository provides inspection, not authoring. The packaged anchor JSON,
sprite, and evidence cards are inputs and must remain byte-identical while the
program runs. Tests exercise the real screen, rejection of the historical batch
mutation interface, and direct rejection by the save and decision functions.

The replacement is **Implemented and Executed**. Automated read-only contract
checks can support **Verified** after they pass, but personal visual acceptance
is deliberately not inferred from those checks. Source identities and local
hardening are recorded in [docs/ATTRIBUTION.md](docs/ATTRIBUTION.md); failures
and revoked claims remain in [docs/FAILURE_LOG.md](docs/FAILURE_LOG.md).

The default fixture is `player-1100.xp`, whose five raw layers include the
normalized base at L2, reviewed armor overlay at L3, and reviewed helmet overlay
at L4. The first screen composes L2-L4 and focuses the armor region; the region
grid reads the focused region's recorded source layer rather than pretending all
regions belong to L2.
