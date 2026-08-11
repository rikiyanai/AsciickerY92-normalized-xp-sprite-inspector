#!/usr/bin/env python3
"""Read-only layer/frame/angle terminal browser for one normalized XP sprite."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import termios
import tty
from dataclasses import dataclass
from pathlib import Path

from xp_read_model import XPFile, XPLayer, load_xp


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ASSET = ROOT / "assets" / "player-nude.xp"
DEFAULT_ASSET_SHA256 = "5054a77f6d991b58e4e3fb326e71eea1d03135fd30127348ba4ee7be1cd8e39c"
TRANSPARENT = (255, 0, 255)


@dataclass
class Selection:
    layer: int = 2
    animation: int = 1
    frame: int = 0
    angle: int = 0


def contract(xp: XPFile) -> dict[str, object]:
    raw = xp.get_metadata() or {"angles": 1, "projs": 1, "anims": [1]}
    angles = int(raw["angles"])
    projections = int(raw["projs"])
    animations = [int(value) for value in raw["anims"]] or [1]
    visual = xp.layers[min(2, len(xp.layers) - 1)]
    columns = projections * sum(animations)
    if visual.width % columns or visual.height % angles:
        raise ValueError("visual layer dimensions do not match XP animation metadata")
    return {
        "angles": angles,
        "projections": projections,
        "animations": animations,
        "frame_width": visual.width // columns,
        "frame_height": visual.height // angles,
    }


def selected_cells(xp: XPFile, meta: dict[str, object], state: Selection) -> list[list[tuple]]:
    animations = list(meta["animations"])
    animation = state.animation % len(animations)
    frame = state.frame % animations[animation]
    angle = state.angle % int(meta["angles"])
    projection = 0
    column = projection * sum(animations) + sum(animations[:animation]) + frame
    width = int(meta["frame_width"])
    height = int(meta["frame_height"])
    layer: XPLayer = xp.layers[state.layer % len(xp.layers)]
    x0 = column * width
    y0 = angle * height
    return [row[x0:x0 + width] for row in layer.data[y0:y0 + height]]


def glyph_text(glyph: int, background: tuple[int, int, int]) -> str:
    if background == TRANSPARENT and glyph in (0, 32):
        return " "
    if 0 <= glyph <= 255:
        char = bytes([glyph]).decode("cp437")
        return char if char.isprintable() else "·"
    try:
        char = chr(glyph)
    except ValueError:
        return "?"
    return char if char.isprintable() else "·"


def screen(xp: XPFile, meta: dict[str, object], state: Selection, asset: Path) -> str:
    animations = list(meta["animations"])
    state.layer %= len(xp.layers)
    state.animation %= len(animations)
    state.frame %= animations[state.animation]
    state.angle %= int(meta["angles"])
    rows = ["".join(glyph_text(cell[0], cell[2]) for cell in row)
            for row in selected_cells(xp, meta, state)]
    header = [
        "NORMALIZED XP SPRITE INSPECTOR (READ-ONLY)",
        f"asset {asset.name}  version {xp.version}  layers {len(xp.layers)}",
        f"layer {state.layer + 1}/{len(xp.layers)}  animation {state.animation + 1}/{len(animations)}  "
        f"frame {state.frame + 1}/{animations[state.animation]}  angle {state.angle + 1}/{meta['angles']}",
        f"frame {meta['frame_width']}x{meta['frame_height']}  source {xp.layers[state.layer].width}x{xp.layers[state.layer].height}",
        "j/k layer  h/l angle  n/p frame  a animation  q quit",
        "",
    ]
    return "\n".join(header + rows)


def json_receipt(xp: XPFile, meta: dict[str, object], state: Selection, asset: Path) -> dict[str, object]:
    return {
        "status": "read-only",
        "asset": str(asset.relative_to(ROOT)),
        "sha256": hashlib.sha256(asset.read_bytes()).hexdigest(),
        "xp_version": xp.version,
        "layers": [{"width": layer.width, "height": layer.height} for layer in xp.layers],
        "contract": meta,
        "selection": {
            "layer": state.layer,
            "animation": state.animation,
            "frame": state.frame,
            "angle": state.angle,
        },
    }


def interactive(xp: XPFile, meta: dict[str, object], state: Selection, asset: Path) -> int:
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        raise SystemExit("interactive mode requires a real terminal; use --once or --json")
    descriptor = sys.stdin.fileno()
    previous = termios.tcgetattr(descriptor)
    try:
        tty.setcbreak(descriptor)
        while True:
            sys.stdout.write("\x1b[2J\x1b[H" + screen(xp, meta, state, asset))
            sys.stdout.flush()
            key = os.read(descriptor, 1).decode(errors="ignore")
            if key == "q":
                return 0
            if key == "j":
                state.layer += 1
            elif key == "k":
                state.layer -= 1
            elif key == "h":
                state.angle -= 1
            elif key == "l":
                state.angle += 1
            elif key == "n":
                state.frame += 1
            elif key == "p":
                state.frame -= 1
            elif key == "a":
                state.animation += 1
                state.frame = 0
    finally:
        termios.tcsetattr(descriptor, termios.TCSADRAIN, previous)
        sys.stdout.write("\x1b[0m\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--asset", type=Path, default=DEFAULT_ASSET)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--once", action="store_true")
    mode.add_argument("--json", action="store_true")
    args = parser.parse_args()
    asset = args.asset.resolve()
    if asset != DEFAULT_ASSET.resolve():
        raise SystemExit(f"refusing unreviewed asset path: {asset}")
    if hashlib.sha256(asset.read_bytes()).hexdigest() != DEFAULT_ASSET_SHA256:
        raise SystemExit("bundled XP asset checksum mismatch")
    xp = load_xp(asset)
    meta = contract(xp)
    state = Selection(layer=min(2, len(xp.layers) - 1))
    if args.json:
        print(json.dumps(json_receipt(xp, meta, state, asset), indent=2, sort_keys=True))
        return 0
    if args.once:
        print(screen(xp, meta, state, asset))
        return 0
    return interactive(xp, meta, state, asset)


if __name__ == "__main__":
    raise SystemExit(main())
