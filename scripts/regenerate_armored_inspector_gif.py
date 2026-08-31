#!/usr/bin/env python3
"""Regenerate the captioned P0C-03 proof GIF without risking the accepted one."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from itertools import combinations
from pathlib import Path

import PIL
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
TAPE = ROOT / "docs" / "armored-inspector.tape"
RAW_GIF = Path("/tmp/p0c03-armored-inspector.raw.gif")
FINAL_GIF = ROOT / "docs" / "armored-inspector.gif"
GIF_CONTRACT = ROOT / "docs" / "armored-inspector.contract.json"
RECORDING_PILLOW_VERSION = "12.1.0"
VHS_VERSION = "vhs version 0.11.0"
CAPTION = "player-1100.xp | L2 base + L3 armor + L4 helmet | read-only UV/body inspector"
GIF_FRAME_DURATION_MS = 550
EXPECTED_STATE_COUNT = 7
EXPECTED_STABLE_RUN_COUNT = 9
BOOTSTRAP_SEMANTIC_NAMES = (
    "composed_uv_body",
    "armor_l3_grid",
    "animation_frame_1",
    "animation_frame_2",
    "animation_frame_3",
    "helmet_l4_grid",
    "helmet_l4_angle_1",
)


def _require_recording_tools() -> None:
    if PIL.__version__ != RECORDING_PILLOW_VERSION:
        raise RuntimeError(
            f"recording requires Pillow {RECORDING_PILLOW_VERSION}, found {PIL.__version__}; "
            "see docs/requirements-recording.txt"
        )
    result = subprocess.run(["vhs", "--version"], text=True, capture_output=True, check=False)
    if result.returncode != 0 or result.stdout.strip() != VHS_VERSION:
        raise RuntimeError(f"recording requires {VHS_VERSION}, found {result.stdout.strip()!r}")


def _caption_raw_gif(
    raw_gif: Path,
    candidate_gif: Path,
    *,
    keep: tuple[int, ...] | None = None,
) -> None:
    """Caption each composited raw frame with only Pillow's built-in font."""
    font = ImageFont.load_default(size=20)
    with Image.open(raw_gif) as image:
        frames: list[Image.Image] = []
        durations: list[int] = []
        selected_indices = keep if keep is not None else tuple(range(image.n_frames))
        for index in selected_indices:
            image.seek(index)
            rendered = image.convert("RGBA").copy()
            draw = ImageDraw.Draw(rendered)
            draw.rectangle((0, 670, rendered.width - 1, rendered.height - 1), fill="#282a36")
            bbox = draw.textbbox((0, 0), CAPTION, font=font)
            x = (rendered.width - (bbox[2] - bbox[0])) // 2
            draw.text((x, 681 - bbox[1]), CAPTION, font=font, fill="#f8f8f2")
            frames.append(rendered.convert("P", palette=Image.Palette.ADAPTIVE))
            durations.append(GIF_FRAME_DURATION_MS)
        frames[0].save(
            candidate_gif,
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=image.info.get("loop", 0),
            disposal=[1] * len(frames),
            optimize=False,
            include_color_table=True,
        )


def _load_contract_module():
    path = ROOT / "tests" / "test_contract.py"
    spec = importlib.util.spec_from_file_location("p0c03_contract", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load P0C-03 artifact contract")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _coarse_rgb(frame: bytes, width: int, *, y1: int, y2: int) -> bytes:
    image = Image.frombytes("RGB", (width, 720), frame)
    return image.crop((0, y1, width, y2)).resize((33, 20)).tobytes()


def _mean_absolute_difference(left: bytes, right: bytes) -> float:
    return sum(abs(a - b) for a, b in zip(left, right, strict=True)) / len(left)


def _stable_raw_frame_indices(raw_gif: Path) -> tuple[int, ...]:
    """Select stable decoded canvases from the canonical VHS capture."""
    contract = _load_contract_module()
    capture = contract.decode_composited_gif(raw_gif)
    runs: list[tuple[int, int]] = []
    start = 0
    previous = None
    for index, frame in enumerate(capture.frames + (b"",)):
        current = contract.hashlib.sha256(
            _coarse_rgb(frame, capture.width, y1=0, y2=670)
        ).digest() if frame else None
        if current != previous:
            if previous is not None:
                runs.append((start, index - 1))
            start = index
            previous = current
    stable_runs = [run for run in runs if run[1] - run[0] + 1 >= 12]
    if len(stable_runs) != EXPECTED_STABLE_RUN_COUNT:
        raise RuntimeError(
            "canonical tape did not produce the expected stable-state sequence: "
            f"expected {EXPECTED_STABLE_RUN_COUNT}, found {len(stable_runs)}"
        )
    # The third stable run is the deliberate return to the composed view before
    # entering the animation group. It is a setup redraw, not another proof state.
    keep_runs = (0, 1, 3, 4, 5, 7, 8)
    return tuple(stable_runs[index][0] for index in keep_runs)


def _filter_transient_frames(candidate_gif: Path) -> None:
    """Reject a captioned candidate that is not the selected proof sequence."""
    contract = _load_contract_module()
    candidate = contract.decode_composited_gif(candidate_gif)
    if len(candidate.frames) != EXPECTED_STATE_COUNT:
        raise RuntimeError(
            "candidate GIF does not contain the expected semantic state sequence"
        )
    fingerprints = {
        contract.hashlib.sha256(
            _coarse_rgb(frame, candidate.width, y1=0, y2=670)
        ).digest()
        for frame in candidate.frames
    }
    if len(fingerprints) != EXPECTED_STATE_COUNT:
        raise RuntimeError("candidate GIF does not contain distinct semantic animation states")

    with Image.open(candidate_gif) as image:
        if image.n_frames != EXPECTED_STATE_COUNT:
            raise RuntimeError("captioned candidate GIF frame count is not stable")


def _verify_candidate(candidate_gif: Path) -> dict[str, object]:
    """Verify product similarity and return exact hashes for the new artifact."""
    contract = _load_contract_module()
    accepted = contract.decode_composited_gif(FINAL_GIF)
    candidate = contract.decode_composited_gif(candidate_gif)
    accepted_contract = json.loads(GIF_CONTRACT.read_text(encoding="utf-8"))
    if (candidate.width, candidate.height) != (1320, 720):
        raise RuntimeError("candidate GIF dimensions or frame count do not match the product contract")
    if not 4 <= len(candidate.frames) <= 12:
        raise RuntimeError("candidate GIF has an implausible product-state frame count")

    candidate_signatures = [
        _coarse_rgb(frame, candidate.width, y1=0, y2=670)
        for frame in candidate.frames
    ]
    bootstrap = int(accepted_contract["frame_count"]) != len(candidate.frames)
    if bootstrap:
        if len(candidate.frames) != EXPECTED_STATE_COUNT:
            raise RuntimeError("candidate GIF does not contain the expected semantic state sequence")
        semantic_names = list(BOOTSTRAP_SEMANTIC_NAMES)
        semantic_indices = {name: index for index, name in enumerate(semantic_names)}
    else:
        accepted_signatures = [
            _coarse_rgb(frame, accepted.width, y1=0, y2=670)
            for frame in accepted.frames
        ]
        for signature in candidate_signatures:
            if min(_mean_absolute_difference(signature, reference) for reference in accepted_signatures) > 0.5:
                raise RuntimeError("candidate GIF contains a frame outside the accepted product surface")
        semantic_names = list(accepted_contract["semantic_frame_indices"])
        semantic_references = [
            accepted_signatures[int(accepted_contract["semantic_frame_indices"][name])]
            for name in semantic_names
        ]
        assignments = []
        for indices in combinations(range(len(candidate_signatures)), len(semantic_names)):
            differences = tuple(
                _mean_absolute_difference(reference, candidate_signatures[index])
                for reference, index in zip(semantic_references, indices, strict=True)
            )
            assignments.append((sum(differences), differences, indices))
        if not assignments:
            raise RuntimeError("candidate GIF cannot provide distinct ordered semantic states")
        _, differences, indices = min(assignments)
        if any(difference > 0.5 for difference in differences):
            raise RuntimeError("candidate GIF is missing a distinct ordered semantic state")
        semantic_indices = dict(zip(semantic_names, indices, strict=True))

    for frame in candidate.frames:
        caption = Image.frombytes("RGB", (candidate.width, candidate.height), frame).crop((0, 670, 1320, 720))
        luminance = caption.convert("L").tobytes()
        bright = sum(value >= 220 for value in luminance)
        dark_ratio = sum(value < 100 for value in luminance) / len(luminance)
        if bright < 800 or dark_ratio < 0.90:
            raise RuntimeError("candidate GIF is missing the persistent ownership caption")

    frame_hashes = [contract.hashlib.sha256(frame).hexdigest() for frame in candidate.frames]
    caption_hashes = [
        contract.hashlib.sha256(contract.rgb_crop(
            frame, candidate.width, x=0, y=670, crop_width=1320, crop_height=50,
        )).hexdigest()
        for frame in candidate.frames
    ]
    return {
        "schema_id": "normalized-xp.armored-inspector-gif.v1",
        "gif_sha256": contract.digest(candidate_gif),
        "width": candidate.width,
        "height": candidate.height,
        "frame_count": len(candidate.frames),
        "frame_sha256": frame_hashes,
        "caption_sha256": caption_hashes,
        "semantic_frame_indices": semantic_indices,
        "semantic_frame_sha256": {
            name: frame_hashes[index] for name, index in semantic_indices.items()
        },
        "semantic_caption_sha256": {
            name: caption_hashes[index] for name, index in semantic_indices.items()
        },
    }


def _publish_pair(
    candidate_gif: Path,
    candidate_contract: Path,
    *,
    final_gif: Path = FINAL_GIF,
    final_contract: Path = GIF_CONTRACT,
    replace=os.replace,
) -> None:
    """Publish both proof owners, restoring both if either replace fails."""
    backup_gif = candidate_gif.with_name(".accepted-gif.backup")
    backup_contract = candidate_contract.with_name(".accepted-contract.backup")
    shutil.copy2(final_gif, backup_gif)
    shutil.copy2(final_contract, backup_contract)
    try:
        replace(candidate_gif, final_gif)
        replace(candidate_contract, final_contract)
    except Exception:
        replace(backup_gif, final_gif)
        replace(backup_contract, final_contract)
        raise
    backup_gif.unlink()
    backup_contract.unlink()


def main() -> int:
    _require_recording_tools()
    subprocess.run(["vhs", str(TAPE)], cwd=ROOT, check=True)
    if not RAW_GIF.is_file():
        raise RuntimeError(f"VHS did not produce raw artifact: {RAW_GIF}")
    with tempfile.TemporaryDirectory(dir=FINAL_GIF.parent, prefix=".p0c03-gif-") as temp_dir:
        candidate = Path(temp_dir) / FINAL_GIF.name
        candidate_contract_path = Path(temp_dir) / GIF_CONTRACT.name
        keep = _stable_raw_frame_indices(RAW_GIF)
        _caption_raw_gif(RAW_GIF, candidate, keep=keep)
        _filter_transient_frames(candidate)
        candidate_contract = _verify_candidate(candidate)
        candidate_contract_path.write_text(
            json.dumps(candidate_contract, indent=2) + "\n", encoding="utf-8"
        )
        _publish_pair(candidate, candidate_contract_path)
    print(f"regenerated {FINAL_GIF.relative_to(ROOT)} from {RAW_GIF}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
