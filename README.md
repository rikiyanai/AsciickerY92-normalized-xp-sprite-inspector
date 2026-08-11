# Normalized XP Sprite Inspector

A standalone, read-only terminal inspector for the normalized REXPaint XP
sprite contract. It ships one hash-pinned `player-nude.xp` demonstration asset
and exposes layer, animation, frame, and angle navigation without any save or
mutation command.

**Status: product-boundary hold.** The current executable is a generic
layer/frame/angle browser. It does not provide the UV/body inspection semantics
implied by this repository's name and original candidate description. The prior
GIF was removed because it demonstrated only the narrowed proxy.

## Run

Python 3.11 or newer is the only dependency.

```sh
./run-inspector.sh
```

Controls: `j`/`k` change layer, `h`/`l` change angle, `n`/`p` change frame,
`a` changes animation, and `q` exits. For deterministic output or automation:

```sh
./run-inspector.sh --once
./run-inspector.sh --json
```

Both commands read the bundled asset and write nothing. The JSON mode prints
the exact source hash, XP version, raw layer dimensions, animation lengths,
frame dimensions, and selected coordinates.

## Boundary

This extraction contains a parser-only XP reader and a new read-only viewer.
It does not contain the parent viewer's decision capture, anchor editing,
semantic-map writes, compiler, runtime, or unrelated sprite library.

Source identities and the deliberate rewrite boundary are recorded in
[docs/ATTRIBUTION.md](docs/ATTRIBUTION.md).
