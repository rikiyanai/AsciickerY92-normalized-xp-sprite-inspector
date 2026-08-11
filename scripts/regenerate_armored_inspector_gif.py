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


def _require_recording_tools() -> None:
    if PIL.__version__ != RECORDING_PILLOW_VERSION:
        raise RuntimeError(
            f"recording requires Pillow {RECORDING_PILLOW_VERSION}, found {PIL.__version__}; "
            "see docs/requirements-recording.txt"
        )
    result = subprocess.run(["vhs", "--version"], text=True, capture_output=True, check=False)
    if result.returncode != 0 or result.stdout.strip() != VHS_VERSION:
        raise RuntimeError(f"recording requires {VHS_VERSION}, found {result.stdout.strip()!r}")


def _caption_raw_gif(raw_gif: Path, candidate_gif: Path) -> None:
    """Caption each composited raw frame with only Pillow's built-in font."""
    font = ImageFont.load_default(size=20)
    with Image.open(raw_gif) as image:
        frames: list[Image.Image] = []
        durations: list[int] = []
        for index in range(image.n_frames):
            image.seek(index)
            rendered = image.convert("RGBA").copy()
            draw = ImageDraw.Draw(rendered)
            draw.rectangle((0, 670, rendered.width - 1, rendered.height - 1), fill="#282a36")
            bbox = draw.textbbox((0, 0), CAPTION, font=font)
            x = (rendered.width - (bbox[2] - bbox[0])) // 2
            draw.text((x, 681 - bbox[1]), CAPTION, font=font, fill="#f8f8f2")
            frames.append(rendered.convert("P", palette=Image.Palette.ADAPTIVE))
            durations.append(image.info.get("duration", 40))
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


def _filter_transient_frames(candidate_gif: Path) -> None:
    """Drop incomplete terminal redraws before the complete-state contract."""
    contract = _load_contract_module()
    accepted = contract.decode_composited_gif(FINAL_GIF)
    candidate = contract.decode_composited_gif(candidate_gif)
    accepted_signatures = [
        _coarse_rgb(frame, accepted.width, y1=0, y2=670)
        for frame in accepted.frames
    ]
    keep = [
        index
        for index, frame in enumerate(candidate.frames)
        if min(
            _mean_absolute_difference(
                _coarse_rgb(frame, candidate.width, y1=0, y2=670),
                reference,
            )
            for reference in accepted_signatures
        ) <= 0.5
    ]
    if len(keep) < 4:
        raise RuntimeError("candidate GIF has fewer than four complete product frames")
    if len(keep) == len(candidate.frames):
        return

    with Image.open(candidate_gif) as image:
        frames: list[Image.Image] = []
        durations: list[int] = []
        for index in range(image.n_frames):
            image.seek(index)
            if index not in keep:
                continue
            frames.append(image.convert("RGBA").copy().convert("P", palette=Image.Palette.ADAPTIVE))
            durations.append(image.info.get("duration", 40))
        filtered = candidate_gif.with_name(candidate_gif.stem + ".filtered.gif")
        frames[0].save(
            filtered,
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=image.info.get("loop", 0),
            disposal=[1] * len(frames),
            optimize=False,
            include_color_table=True,
        )
    os.replace(filtered, candidate_gif)


def _verify_candidate(candidate_gif: Path) -> dict[str, object]:
    """Verify product similarity and return exact hashes for the new artifact."""
    contract = _load_contract_module()
    accepted = contract.decode_composited_gif(FINAL_GIF)
    candidate = contract.decode_composited_gif(candidate_gif)
    if (candidate.width, candidate.height) != (1320, 720):
        raise RuntimeError("candidate GIF dimensions or frame count do not match the product contract")
    if not 4 <= len(candidate.frames) <= 12:
        raise RuntimeError("candidate GIF has an implausible product-state frame count")

    accepted_signatures = [
        _coarse_rgb(frame, accepted.width, y1=0, y2=670)
        for frame in accepted.frames
    ]
    candidate_signatures = [
        _coarse_rgb(frame, candidate.width, y1=0, y2=670)
        for frame in candidate.frames
    ]
    for signature in candidate_signatures:
        if min(_mean_absolute_difference(signature, reference) for reference in accepted_signatures) > 0.5:
            raise RuntimeError("candidate GIF contains a frame outside the accepted product surface")

    accepted_contract = json.loads(GIF_CONTRACT.read_text(encoding="utf-8"))
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
        raise RuntimeError("candidate GIF cannot provide four distinct ordered semantic states")
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
        _caption_raw_gif(RAW_GIF, candidate)
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
