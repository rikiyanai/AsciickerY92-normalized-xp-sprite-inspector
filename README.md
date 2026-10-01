# AsciickerY92 Normalized XP Sprite Inspector

This is a standalone, read-only terminal inspection toolkit for Asciicker Y9-2
REXPaint XP sprites. It includes both the normalized UV/body inspector and the
source-layer contract viewer in one repository, sharing all 115 packaged sprites.

Use it when you need to see how a packed `.xp` sprite turns into body regions,
animation frames, angles, and UV coordinates without opening the full Y9-2
runtime. The repo includes the viewer, all 115 packaged XP sprites, the reviewed
armored-player anchor data, and the parser/helpers needed to run by itself.

Choose a view:

- `./run-inspector.sh` — normalized body regions, animation frames, angles, and UV coordinates.
- `./run-viewer.sh` — raw source layers, reviewed cell roles, projections, and layer composition.

Both commands accept `--once` for non-interactive output. Python 3.11 or newer
is the only runtime dependency. Neither view changes sprites or review data.

## How an XP sprite becomes a body view

REXPaint stores an XP sprite as a cell atlas with raw layers. In the normalized
Y9-2 convention, L0 carries the color key, L1 carries engine metadata, L2 is
the base visual layer, and L3+ are ordinal visual overlays such as armor or a
helmet. The atlas repeats frame cells across animation groups and angles, with
the source metadata defining the frame geometry; a projection is an additional
atlas view when the asset provides one.

The inspector keeps those axes separate. An **animation** selects a group of
frames, a **frame** selects one time position in that group, and an **angle**
selects the directional row for that frame. A **body region** is a reviewed
frame-local rectangle such as `armor` or `helmet`. Its recorded `source_layer`
identifies which raw layer owns that region; the UV panel then reports the
atlas-global coordinates for the same cells. The composed panel shows the
ordinal L2-L4 result beside the focused region.

The packaged XP corpus, anchor map, and review notes are historical inputs for
inspection. They document how the sprites were reviewed; they do not write back
to the runtime. The complete non-duplicating inventory is in
[docs/historical-evidence/](docs/historical-evidence/).

An earlier 7×9 layer/frame browser was removed because it did not show the
UV/body relationship this repo is for.

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

This sweep is generated from the tracked corpus under `assets/sprites/`. It
pages through all 115 packaged `.xp` files and advances animation/angle ticks
while rendering the composed sprite preview. Use it to confirm the whole corpus
is present and browseable; use the focused walkthrough above to inspect the
armor/helmet body-region view.

## Included corpus and fixture

The repository tracks all 115 packaged `.xp` files under `assets/sprites/`.
Any packaged sprite/layer can be inspected with the exact dump path:

```sh
python3 scripts/xp_uv_body_viewer.py --sprite-dir assets/sprites --sprite attack-0001.xp --layer 0 --json
```

The default UV/body fixture is `player-1100.xp`. Its five raw layers include the normalized base at L2, the reviewed armor overlay at L3, and the reviewed helmet overlay at L4.

The first screen composes L2-L4 and focuses the armor region. The region grid reads the recorded source layer for that region instead of assuming that every region belongs to L2.

The walkthrough starts in the terminal UI. It shows the composed armored sprite,
the UV panel, the armor grid from source layer L3, adjacent animation frames,
and the helmet grid from L4 at another angle. The lower label names the fixture:
`player-1100.xp | L2 base + L3 armor + L4 helmet`.

## Scope

This repository is an inspector, not an authoring tool. The packaged sprites,
anchor data, and review files are inputs and remain unchanged while the
inspector runs.

Regenerate the committed artifact through its verifier:

```sh
python3 -m pip install -r docs/requirements-recording.txt
./scripts/regenerate_armored_inspector_gif.py
```

The command requires VHS 0.11.0 and recording-only `Pillow==12.1.0` from
[`docs/requirements-recording.txt`](docs/requirements-recording.txt). After
regenerating, manually inspect the composed UV/body view, L3 armor grid,
adjacent animation frames, L4 helmet grid, and changed-angle L4 grid before
committing the new GIF.

Source identities and local hardening notes are in
[docs/ATTRIBUTION.md](docs/ATTRIBUTION.md).

## Source-layer inspection

The source-layer contract viewer is now included here. The same `run-viewer.sh`
command, controls, reviewed inputs, and recordings are preserved.

### How an XP sprite becomes a layered sprite

REXPaint stores an XP sprite as a cell atlas with raw layers. In the Y9-2
source files, L0 is the color-key layer, L1 is the height/metadata layer,
L2 is the primary body accumulator, and L3+ are ordinal visual overlays such as
armor, helmet, or a weapon effect. The viewer preserves that raw-layer order
while showing a read-only inspection projection; it does not claim to compile
or author the runtime result.

The atlas has separate axes that must not be flattened. A **frame** is one time
position in the animation sequence. An **angle** is a directional row for that
frame. A **projection** is a front/rear (or equivalent) atlas view. A semantic
**body region** or role is a reviewed interpretation of selected cells on a
source layer. The final-sprite panel composes included visual layers, the
selected panel isolates the current raw layer, and the animation panel shows
the adjacent frame cells together. `n`/`p` moves frames, `.`/`,` moves angles,
`r` changes projection, and `v` demonstrates the display-only hide/show seam.

The review decisions and any hand-entered labels are historical review records.
They identify what was reviewed and why; the viewer reads them for inspection
but does not compile or mutate runtime data. The complete non-duplicating
inventory is in
[docs/historical-evidence/](docs/historical-evidence/).

The packaged corpus contains 115 reviewed XP files and 573 raw layers. The
viewer reads the layer decisions and cell-role data but cannot change them.

![Read-only player body, armor, and helmet source-layer view](docs/recordings/source-layer-contract-viewer.gif)

![Animated sweep through all tracked source layers](docs/recordings/source-layer-corpus-sweep.gif)

The focused GIF answers the main visual question: how do the reviewed source
layers compose into the final sprite? It opens the five-layer `player-1100`
asset, compares the armored composite with the selected armor or helmet layer,
and shows adjacent animation frames, angle/projection changes, hide/restore,
raw layer navigation, and navigation to another XP stem.

The corpus sweep renders every one of the 573 tracked raw layers across the 115
packaged XP files, one paged grid at a time. Use it to browse the whole
tracked source-layer corpus quickly.

### Run

For one non-interactive render:

```sh
./run-viewer.sh --once
```

Run without `--once` from a terminal for interactive navigation.

For the compact armored view shown in the recording:

```sh
./run-viewer.sh --source-key player-1100-L3 --compact
```

### What the viewer reads

- the packaged `.xp` sprite corpus
- source-layer review decisions
- per-family topology data
- reviewed cell roles

The viewer has no serialization or mutation path. It does not edit sprite files, assignments, anchors, semantic maps, or compiler/runtime state.

Excluded: `xp_core.py`, queues, comparison and coordinate-recording CLIs,
compilers, assignment saves, anchor editing, and semantic-map mutation.

See [docs/provenance.md](docs/provenance.md) for source identities, hashes, and
the visibility boundary. The reproducible capture recipe is stored
beside the GIF, and `./scripts/build-recording.sh` rebuilds the thirteen-state GIF.
Historical development records remain in
[docs/FAILURE_LOG.md](docs/FAILURE_LOG.md).

## Repository consolidation

The source-layer viewer was absorbed into this repository on October 1, 2026.
Its published history is preserved as the second parent of the consolidation
merge, and its shared XP corpus is stored only once. See
[the consolidation record](docs/consolidation.md) for the exact source commits,
retained paths, and recovery instructions.
