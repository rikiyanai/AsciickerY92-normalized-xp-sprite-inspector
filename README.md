# AsciickerY92 Normalized XP Sprite Inspector

A standalone, read-only terminal inspector for the Asciicker Y9-2 normalized REXPaint XP sprite-to-UV/body contract.

It packages the real `xp_uv_body_viewer.py` surface, the full 115-file XP
corpus, the reviewed armored player anchor map, and the parser and semantic helpers needed to run
independently of the parent repository.

## How an XP sprite becomes a body view

REXPaint stores an XP sprite as a cell atlas with raw layers. In the normalized
Y9-2 convention, L0 carries the color key, L1 carries engine metadata, L2 is
the base visual layer, and L3+ are ordinal visual overlays such as armor or a
helmet. The atlas repeats frame cells across animation groups and angles, with
the source metadata defining the frame geometry; a projection is an additional
atlas view when the asset provides one.

This inspector keeps those axes separate. An **animation** selects a group of
frames, a **frame** selects one time position in that group, and an **angle**
selects the directional row for that frame. A **body region** is a reviewed
frame-local rectangle such as `armor` or `helmet`. Its recorded `source_layer`
identifies which raw layer owns that region; the UV panel then reports the
atlas-global coordinates for the same cells. The composed panel shows the
ordinal L2-L4 result beside the focused region, so a region label is not being
inferred from a filename or promoted to runtime authority.

The packaged XP corpus, anchor map, and evidence cards are historical inputs. Their
hand-entered labels and review notes remain evidence, not compiler/runtime
truth. The complete non-duplicating inventory is in
[docs/historical-evidence/](docs/historical-evidence/).

The previous 7x9 layer/frame browser was a product substitution. It and its GIF
were removed; they did not expose any UV/body relationship.

## Run

Python 3.11 or newer is the only dependency.

```sh
./run-inspector.sh
```

The interactive screen shows three related views of the selected sprite cell:

- the engine-order composition of base, armor, and helmet layers;
- the selected body region and its cells across angles; and
- atlas-global UV coordinates for every cell in the frame.

Use the arrow keys to navigate. Use `a`/`d` for angle, `w`/`s` for animation, `,`/`.` for frame, `r`/`f` for region focus, `g` for the angle grid, `b` for a packaged body-map band, and `q` to quit.

This standalone inspector is read-only. It cannot save assignments, anchors, review decisions, or batch mutations.

For deterministic non-TTY output of the same UV/body view:

```sh
./run-inspector.sh --once
```

## Walkthrough

![Animated walkthrough of the armored UV/body inspector](docs/armored-inspector.gif)

The GIF shows the composed armored sprite and UV panel, the armor grid from
source layer L3, adjacent animation-frame progression, the helmet grid from L4,
and the helmet grid at another angle. It is intentionally paced at 0.18 seconds
per frame for fast review.

## Corpus sweep

![Animated sweep through every packaged XP sprite](docs/xp-corpus-sweep.gif)

This README-visible sweep is generated from the tracked corpus under
`assets/sprites/`. It pages through all 115 packaged `.xp` files and advances
animation/angle ticks while rendering the composed sprite preview. It is a
corpus-breadth demo; the UV/body proof above remains the focused source-layer
ownership demo.

## Included corpus and fixture

The repository tracks all 115 packaged `.xp` files under `assets/sprites/`.
Any packaged sprite/layer can be inspected with the exact dump path:

```sh
python3 scripts/xp_uv_body_viewer.py --sprite-dir assets/sprites --sprite attack-0001.xp --layer 0 --json
```

The default UV/body fixture is `player-1100.xp`. Its five raw layers include the normalized base at L2, the reviewed armor overlay at L3, and the reviewed helmet overlay at L4.

The first screen composes L2-L4 and focuses the armor region. The region grid reads the recorded source layer for that region instead of assuming that every region belongs to L2.

The recording starts directly in the alternate-screen product UI (the startup
command is deliberately hidden). It shows the composed armored sprite with its
UV panel, the armor grid (`source L3`), three adjacent animation frames selected
with the viewer's real `.` control, and the helmet grid (`source L4`) after
navigation to another angle. A persistent lower-canvas label names the fixture
and layer ownership—`player-1100.xp | L2 base + L3 armor + L4 helmet`—without
cropping or modifying the product screen. The capture uses a short one-second
settle between states; the final GIF is intentionally paced for quick review.

## Scope

This repository is an inspector, not an authoring tool. The packaged sprite, anchor data, and evidence files are inputs and remain unchanged while the inspector runs.

Regenerate the committed artifact through its verifier:

```sh
python3 -m pip install -r docs/requirements-recording.txt
./scripts/regenerate_armored_inspector_gif.py
```

The command requires VHS 0.11.0 and recording-only `Pillow==12.1.0` from
[`docs/requirements-recording.txt`](docs/requirements-recording.txt). The tape
creates only `/tmp/p0c03-armored-inspector.raw.gif`; the script captions a
temporary candidate with Pillow's built-in font, dependency-freely verifies the
candidate's dimensions, every frame, every caption band, and the required
product states against the accepted artifact, then publishes the GIF and its
exact hash receipt only after those semantic/perceptual checks pass.

The committed artifact remains byte-bound by
[`docs/armored-inspector.contract.json`](docs/armored-inspector.contract.json): it
LZW-decodes and composites the GIF without image libraries, then checks its
1320×720 canvas, every recorded product frame and caption band, plus eight
semantic state fingerprints. VHS timing and rasterization are not byte-stable;
the regenerator therefore applies a bounded visual-similarity gate before it
writes the new exact receipt. Manually inspect the composed UV/body view, L3
armor grid, adjacent animation frames, L4 helmet grid, and changed-angle L4
grid after any intentional regeneration.

Source identities and local hardening notes are in
[docs/ATTRIBUTION.md](docs/ATTRIBUTION.md).
