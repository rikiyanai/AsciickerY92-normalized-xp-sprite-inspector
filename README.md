# AsciickerY92 Normalized XP Sprite Inspector

A standalone, read-only terminal inspector for the Asciicker Y9-2 normalized REXPaint XP sprite-to-UV/body contract.

It packages the real `xp_uv_body_viewer.py` surface, one reviewed armored player sprite, its anchor map, and the parser and semantic helpers needed to run independently of the parent repository.

The previous 7x9 layer/frame browser was the wrong product. It did not show the UV/body relationship, so it and its GIF were removed.

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

The GIF is the README walkthrough. It shows the composed armored sprite and UV panel, the armor grid from source layer L3, the helmet grid from L4, and the helmet grid at another angle.

## Included fixture

The default fixture is `player-1100.xp`. Its five raw layers include the normalized base at L2, the reviewed armor overlay at L3, and the reviewed helmet overlay at L4.

The first screen composes L2-L4 and focuses the armor region. The region grid reads the recorded source layer for that region instead of assuming that every region belongs to L2.

## Scope

This repository is an inspector, not an authoring tool. The packaged sprite, anchor data, and evidence files are inputs and remain unchanged while the inspector runs.

Source identities and local hardening notes are in [docs/ATTRIBUTION.md](docs/ATTRIBUTION.md).
