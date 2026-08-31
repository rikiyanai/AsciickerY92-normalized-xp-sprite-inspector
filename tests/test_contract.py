from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "run-inspector.sh"
VIEWER = ROOT / "scripts" / "xp_uv_body_viewer.py"
ANCHOR = ROOT / "docs" / "research" / "ascii" / "semantic_maps" / "player-1100-anchors.json"
SPRITE = ROOT / "assets" / "sprites" / "player-1100.xp"
EVIDENCE = ROOT / "docs" / "research" / "ascii" / "semantic_maps" / "layer_evidence_cards.jsonl"
GIF = ROOT / "docs" / "armored-inspector.gif"
TAPE = ROOT / "docs" / "armored-inspector.tape"
REGENERATOR = ROOT / "scripts" / "regenerate_armored_inspector_gif.py"
RECORDING_REQUIREMENTS = ROOT / "docs" / "requirements-recording.txt"
GIF_CONTRACT = ROOT / "docs" / "armored-inspector.contract.json"
ANSI = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_viewer():
    spec = importlib.util.spec_from_file_location("standalone_xp_uv_body_viewer", VIEWER)
    if spec is None or spec.loader is None:
        raise AssertionError("viewer module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_regenerator():
    spec = importlib.util.spec_from_file_location("standalone_gif_regenerator", REGENERATOR)
    if spec is None or spec.loader is None:
        raise AssertionError("GIF regenerator module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_gif_variant(
    source: Path,
    destination: Path,
    *,
    keep: tuple[int, ...] | None = None,
    grayscale: bool = False,
) -> None:
    from PIL import Image

    with Image.open(source) as image:
        selected = set(keep if keep is not None else range(image.n_frames))
        frames = []
        durations = []
        for index in range(image.n_frames):
            image.seek(index)
            if index not in selected:
                continue
            rendered = image.convert("RGBA").copy()
            if grayscale:
                rendered = rendered.convert("L").convert("RGBA")
            frames.append(rendered.convert("P", palette=Image.Palette.ADAPTIVE))
            durations.append(image.info.get("duration", 40))
        frames[0].save(
            destination,
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=image.info.get("loop", 0),
            disposal=[1] * len(frames),
            optimize=False,
            include_color_table=True,
        )


@dataclass(frozen=True)
class DecodedGif:
    width: int
    height: int
    frames: tuple[bytes, ...]  # fully composited RGB frames


def _gif_sub_blocks(data: bytes, cursor: int) -> tuple[bytes, int]:
    chunks: list[bytes] = []
    while True:
        if cursor >= len(data):
            raise AssertionError("truncated GIF sub-block")
        size = data[cursor]
        cursor += 1
        if size == 0:
            return b"".join(chunks), cursor
        end = cursor + size
        if end > len(data):
            raise AssertionError("truncated GIF sub-block payload")
        chunks.append(data[cursor:end])
        cursor = end


def _gif_palette(data: bytes, cursor: int, packed: int) -> tuple[list[bytes], int]:
    count = 1 << ((packed & 0x07) + 1)
    end = cursor + count * 3
    if end > len(data):
        raise AssertionError("truncated GIF palette")
    return [data[offset:offset + 3] for offset in range(cursor, end, 3)], end


def _gif_lzw_indices(payload: bytes, minimum_code_size: int) -> bytearray:
    """Decode GIF's LSB-first LZW stream into palette indices."""
    if not 2 <= minimum_code_size <= 8:
        raise AssertionError(f"unsupported GIF minimum code size: {minimum_code_size}")
    clear_code = 1 << minimum_code_size
    end_code = clear_code + 1
    # The clear and end codes reserve two table positions even though they have
    # no literal byte sequence. Keeping those slots preserves GIF code values.
    table = [bytes([value]) for value in range(clear_code)] + [b"", b""]
    code_size = minimum_code_size + 1
    next_code = end_code + 1
    bit_buffer = 0
    bit_count = 0
    payload_cursor = 0
    previous: bytes | None = None
    output = bytearray()

    while True:
        while bit_count < code_size and payload_cursor < len(payload):
            bit_buffer |= payload[payload_cursor] << bit_count
            payload_cursor += 1
            bit_count += 8
        if bit_count < code_size:
            raise AssertionError("truncated GIF LZW stream")
        code = bit_buffer & ((1 << code_size) - 1)
        bit_buffer >>= code_size
        bit_count -= code_size

        if code == clear_code:
            table = [bytes([value]) for value in range(clear_code)] + [b"", b""]
            code_size = minimum_code_size + 1
            next_code = end_code + 1
            previous = None
            continue
        if code == end_code:
            return output
        if code < len(table) and table[code]:
            entry = table[code]
        elif code == next_code and previous is not None:
            entry = previous + previous[:1]
        else:
            raise AssertionError(f"invalid GIF LZW code: {code}")
        output.extend(entry)
        if previous is not None and next_code < 4096:
            table.append(previous + entry[:1])
            next_code += 1
            if next_code == (1 << code_size) and code_size < 12:
                code_size += 1
        previous = entry


def _gif_row_order(indices: bytearray, width: int, height: int, interlaced: bool) -> bytearray:
    expected = width * height
    if len(indices) != expected:
        raise AssertionError(f"GIF image has {len(indices)} palette indices, expected {expected}")
    if not interlaced:
        return indices
    ordered = bytearray(expected)
    source_row = 0
    for start, step in ((0, 8), (4, 8), (2, 4), (1, 2)):
        for row in range(start, height, step):
            src = source_row * width
            ordered[row * width:(row + 1) * width] = indices[src:src + width]
            source_row += 1
    return ordered


def decode_composited_gif(path: Path) -> DecodedGif:
    """Dependency-free GIF89a decoder for proof-frame compositing and hashes."""
    data = path.read_bytes()
    if not data.startswith((b"GIF87a", b"GIF89a")) or len(data) < 13:
        raise AssertionError("artifact is not a complete GIF")
    width = int.from_bytes(data[6:8], "little")
    height = int.from_bytes(data[8:10], "little")
    packed = data[10]
    background_index = data[11]
    cursor = 13
    global_palette: list[bytes] = []
    if packed & 0x80:
        global_palette, cursor = _gif_palette(data, cursor, packed)
    background = global_palette[background_index] if background_index < len(global_palette) else b"\0\0\0"
    canvas = bytearray(background * (width * height))
    frames: list[bytes] = []
    disposal = 0
    transparent_index: int | None = None
    previous_disposal = 0
    previous_rect: tuple[int, int, int, int] | None = None
    previous_canvas: bytes | None = None

    while cursor < len(data):
        marker = data[cursor]
        cursor += 1
        if marker == 0x3B:  # trailer
            break
        if marker == 0x21:  # extension
            if cursor >= len(data):
                raise AssertionError("truncated GIF extension")
            label = data[cursor]
            cursor += 1
            if label == 0xF9:  # graphic control extension
                if cursor + 6 > len(data) or data[cursor] != 4:
                    raise AssertionError("malformed GIF graphic control extension")
                control = data[cursor + 1]
                disposal = (control >> 2) & 0x07
                transparent_index = data[cursor + 4] if control & 0x01 else None
                cursor += 6  # block-size + payload + terminator
            else:
                if label in {0x01, 0xFF}:  # plain text / application header
                    if cursor >= len(data):
                        raise AssertionError("truncated GIF extension header")
                    header_size = data[cursor]
                    cursor += 1 + header_size
                _, cursor = _gif_sub_blocks(data, cursor)
            continue
        if marker != 0x2C:
            raise AssertionError(f"unexpected GIF block 0x{marker:02x}")

        if previous_disposal == 2 and previous_rect is not None:
            left, top, frame_width, frame_height = previous_rect
            for row in range(top, top + frame_height):
                start = (row * width + left) * 3
                canvas[start:start + frame_width * 3] = background * frame_width
        elif previous_disposal == 3 and previous_canvas is not None:
            canvas[:] = previous_canvas

        if cursor + 9 > len(data):
            raise AssertionError("truncated GIF image descriptor")
        left = int.from_bytes(data[cursor:cursor + 2], "little")
        top = int.from_bytes(data[cursor + 2:cursor + 4], "little")
        frame_width = int.from_bytes(data[cursor + 4:cursor + 6], "little")
        frame_height = int.from_bytes(data[cursor + 6:cursor + 8], "little")
        image_packed = data[cursor + 8]
        cursor += 9
        palette = global_palette
        if image_packed & 0x80:
            palette, cursor = _gif_palette(data, cursor, image_packed)
        if cursor >= len(data):
            raise AssertionError("truncated GIF image data")
        minimum_code_size = data[cursor]
        cursor += 1
        compressed, cursor = _gif_sub_blocks(data, cursor)
        indices = _gif_row_order(
            _gif_lzw_indices(compressed, minimum_code_size),
            frame_width,
            frame_height,
            bool(image_packed & 0x40),
        )
        saved_canvas = bytes(canvas) if disposal == 3 else None
        for local_y in range(frame_height):
            target_y = top + local_y
            if target_y >= height:
                continue
            for local_x in range(frame_width):
                target_x = left + local_x
                color_index = indices[local_y * frame_width + local_x]
                if target_x >= width or color_index == transparent_index:
                    continue
                if color_index >= len(palette):
                    raise AssertionError(f"GIF palette index {color_index} is out of range")
                target = (target_y * width + target_x) * 3
                canvas[target:target + 3] = palette[color_index]
        frames.append(bytes(canvas))
        previous_disposal = disposal
        previous_rect = (left, top, frame_width, frame_height)
        previous_canvas = saved_canvas
        disposal = 0
        transparent_index = None

    if not frames:
        raise AssertionError("GIF contains no image frames")
    return DecodedGif(width=width, height=height, frames=tuple(frames))


def rgb_crop(frame: bytes, width: int, *, x: int, y: int, crop_width: int, crop_height: int) -> bytes:
    return b"".join(
        frame[((y + row) * width + x) * 3:((y + row) * width + x + crop_width) * 3]
        for row in range(crop_height)
    )


def tape_instructions(path: Path) -> tuple[str, ...]:
    return tuple(
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    )


class InspectorContract(unittest.TestCase):
    def test_once_renders_actual_uv_body_surface_without_writes(self) -> None:
        protected = [ANCHOR, SPRITE, EVIDENCE]
        before = {path: digest(path) for path in protected}
        result = subprocess.run(
            [str(LAUNCHER), "--once"],
            check=True,
            text=True,
            capture_output=True,
        )
        screen = ANSI.sub("", result.stdout)
        self.assertIn("Anchor review: player-1100-anchors.json ->", screen)
        self.assertIn("player-1100.xp layers 2-4 composed", screen)
        self.assertIn("Region: armor", screen)
        self.assertIn("UV map (atlas offset 0,0)", screen)
        self.assertIn("Regions at angle 0", screen)
        self.assertIn("standalone inspector is read-only", screen.lower())
        self.assertEqual(before, {path: digest(path) for path in protected})

    def test_historical_batch_mutation_interface_fails_closed(self) -> None:
        before = digest(ANCHOR)
        result = subprocess.run(
            [
                str(LAUNCHER),
                "--anchor-batch",
                str(ANCHOR),
                "--batch-ops",
                '[{"op":"create_region","angle":0,"region":"forbidden","cells":[[0,0]]}]',
            ],
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("anchor batch blocked", result.stderr)
        self.assertEqual(before, digest(ANCHOR))

    def test_dump_output_file_interface_is_absent(self) -> None:
        forbidden = ROOT / "forbidden-output.json"
        result = subprocess.run(
            [str(LAUNCHER), "--out", str(forbidden)],
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("unrecognized arguments: --out", result.stderr)
        self.assertFalse(forbidden.exists())

    def test_direct_save_and_decision_paths_fail_closed(self) -> None:
        viewer = load_viewer()
        state = viewer._load_anchor_state(ANCHOR)
        with self.assertRaisesRegex(RuntimeError, "read-only"):
            viewer._save_anchor(state)
        self.assertIn("blocked", viewer._commit_decision(state, "body", "forbidden").lower())

    def test_packaged_fixture_has_reviewed_base_armor_and_helmet_layers(self) -> None:
        viewer = load_viewer()
        asset = viewer._load_raw_asset(viewer._resolve_sprite_entry(str(SPRITE), SPRITE.parent))
        self.assertEqual(asset.layer_count, 5)
        state = viewer._load_anchor_state(ANCHOR)
        regions = state.anchor_data["frames"]["0"]["regions"]
        self.assertEqual({r["name"]: r.get("source_layer") for r in regions if r.get("source_layer")}, {
            "armor": 3,
            "helmet": 4,
        })

    def test_default_interactive_surface_requires_a_real_tty(self) -> None:
        result = subprocess.run([str(LAUNCHER)], text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        combined = result.stdout + result.stderr
        self.assertIn("anchor review requires a TTY", combined)

    def test_rejected_generic_proxy_is_absent(self) -> None:
        self.assertFalse((ROOT / "scripts" / "normalized_xp_inspector.py").exists())
        self.assertFalse((ROOT / "scripts" / "xp_read_model.py").exists())
        self.assertFalse((ROOT / "assets" / "player-nude.xp").exists())

    def test_viewer_contains_no_disk_write_implementation(self) -> None:
        source = VIEWER.read_text(encoding="utf-8")
        for forbidden in (
            "write_text(",
            "write_bytes(",
            "os.replace(",
            "os.unlink(",
            "NamedTemporaryFile(",
            "mkstemp(",
        ):
            self.assertNotIn(forbidden, source)

    # P0C-03: demo proof must invoke the read-only product, not a static proxy.
    def test_armored_walkthrough_recipe_uses_hidden_launcher_and_real_navigation(self) -> None:
        tape = TAPE.read_text(encoding="utf-8")
        self.assertIn("# Capture engine: VHS 0.11.0.", tape)
        self.assertEqual(tape_instructions(TAPE), (
            'Output "/tmp/p0c03-armored-inspector.raw.gif"',
            "Set FontSize 18",
            "Set Width 1320",
            "Set Height 720",
            'Set Theme "Dracula"',
            "Set TypingSpeed 1ms",
            "Hide",
            'Type "./run-inspector.sh"',
            "Enter",
            "Wait+Screen /Anchor review: player-1100-anchors.json/",
            "Show",
            "Sleep 1s",
            'Type "g"',
            "Sleep 1s",
            'Type "g"',
            "Sleep 1s",
            'Type "s"',
            "Sleep 1s",
            'Type "."',
            "Sleep 1s",
            'Type "."',
            "Sleep 1s",
            'Type "r"',
            "Sleep 1s",
            'Type "g"',
            "Sleep 1s",
            'Type "d"',
            "Sleep 1s",
            "Hide",
            'Type "q"',
        ))

    def test_regeneration_pipeline_owns_captioning_and_atomic_publish(self) -> None:
        instructions = tape_instructions(TAPE)
        self.assertEqual(instructions[0], 'Output "/tmp/p0c03-armored-inspector.raw.gif"')
        self.assertNotIn(f"Output {GIF.relative_to(ROOT)}", instructions)
        self.assertEqual(
            RECORDING_REQUIREMENTS.read_text(encoding="utf-8").splitlines()[-1],
            "Pillow==12.1.0",
        )
        source = REGENERATOR.read_text(encoding="utf-8")
        self.assertIn('RECORDING_PILLOW_VERSION = "12.1.0"', source)
        self.assertIn(
            'CAPTION = "player-1100.xp | L2 base + L3 armor + L4 helmet | read-only UV/body inspector"',
            source,
        )
        self.assertIn("ImageFont.load_default(size=20)", source)
        self.assertIn("_caption_raw_gif(RAW_GIF, candidate, keep=keep)", source)
        self.assertIn("_filter_transient_frames(candidate)", source)
        self.assertIn("candidate_contract = _verify_candidate(candidate)", source)
        self.assertIn("_publish_pair(candidate, candidate_contract_path)", source)

    def test_regeneration_gate_rejects_missing_states_and_grayscale(self) -> None:
        regenerator = load_regenerator()
        contract = json.loads(GIF_CONTRACT.read_text(encoding="utf-8"))
        indices = contract["semantic_frame_indices"]
        all_indices = tuple(range(contract["frame_count"]))
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            variants = {
                "missing composed": tuple(i for i in all_indices if i != indices["composed_uv_body"]),
                "missing changed angle": tuple(i for i in all_indices if i != indices["helmet_l4_angle_1"]),
            }
            for label, keep in variants.items():
                candidate = temp / (label.replace(" ", "-") + ".gif")
                write_gif_variant(GIF, candidate, keep=keep)
                with self.assertRaisesRegex(RuntimeError, "semantic state"):
                    regenerator._verify_candidate(candidate)

            grayscale = temp / "grayscale.gif"
            write_gif_variant(GIF, grayscale, grayscale=True)
            with self.assertRaisesRegex(RuntimeError, "accepted product surface"):
                regenerator._verify_candidate(grayscale)

    def test_pair_publish_restores_both_owners_on_second_replace_failure(self) -> None:
        regenerator = load_regenerator()
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            final_gif = temp / "final.gif"
            final_contract = temp / "final.json"
            candidate_gif = temp / "candidate.gif"
            candidate_contract = temp / "candidate.json"
            final_gif.write_bytes(b"accepted-gif")
            final_contract.write_bytes(b"accepted-contract")
            candidate_gif.write_bytes(b"candidate-gif")
            candidate_contract.write_bytes(b"candidate-contract")
            calls = 0

            def fail_second_replace(source: Path, destination: Path) -> None:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("injected receipt replace failure")
                os.replace(source, destination)

            with self.assertRaisesRegex(OSError, "injected receipt replace failure"):
                regenerator._publish_pair(
                    candidate_gif,
                    candidate_contract,
                    final_gif=final_gif,
                    final_contract=final_contract,
                    replace=fail_second_replace,
                )
            self.assertEqual(final_gif.read_bytes(), b"accepted-gif")
            self.assertEqual(final_contract.read_bytes(), b"accepted-contract")

    def test_walkthrough_states_show_l3_armor_l4_helmet_and_changed_angle(self) -> None:
        viewer = load_viewer()
        state = viewer._load_anchor_state(ANCHOR)
        asset = viewer._load_raw_asset(viewer._resolve_sprite_entry(str(SPRITE), SPRITE.parent))
        layer_index = int(state.anchor_data["semantic_layer"])
        state.anim_lengths = list(asset.entry.meta.anim_lengths)
        state.region_focus = next(
            index
            for index, region in enumerate(state.regions_at_angle())
            if int(region.get("source_layer", layer_index)) > layer_index
        )
        cell_data = viewer._load_composed_frame_cell_data_from_xp(state, asset, layer_index)
        full_screen = ANSI.sub("", viewer._anchor_compose_screen(
            state, cell_data, asset=asset, layer_index=layer_index,
            layer_label="layers 2-4 composed",
        ))
        self.assertIn("Region: armor", full_screen)
        self.assertIn("UV map (atlas offset 0,0)", full_screen)

        viewer._handle_anchor_key(state, "g", cell_data)
        armor_grid = ANSI.sub("", viewer._anchor_compose_screen(
            state, cell_data, asset=asset, layer_index=layer_index,
            layer_label="layers 2-4 composed",
        ))
        self.assertIn("Region grid: armor  source L3", armor_grid)

        viewer._handle_anchor_key(state, "g", cell_data)
        viewer._handle_anchor_key(state, "r", cell_data)
        viewer._handle_anchor_key(state, "g", cell_data)
        viewer._handle_anchor_key(state, "d", cell_data)
        helmet_cells = viewer._load_composed_frame_cell_data_from_xp(state, asset, layer_index)
        helmet_grid = ANSI.sub("", viewer._anchor_compose_screen(
            state, helmet_cells, asset=asset, layer_index=layer_index,
            layer_label="layers 2-4 composed",
        ))
        self.assertIn("Region grid: helmet  source L4", helmet_grid)
        self.assertIn("*ang 1", helmet_grid)

    def test_animation_controls_reach_adjacent_frames(self) -> None:
        viewer = load_viewer()
        state = viewer._load_anchor_state(ANCHOR)
        asset = viewer._load_raw_asset(viewer._resolve_sprite_entry(str(SPRITE), SPRITE.parent))
        state.anim_lengths = list(asset.entry.meta.anim_lengths)
        cell_data = viewer._load_composed_frame_cell_data_from_xp(
            state, asset, int(state.anchor_data["semantic_layer"])
        )
        self.assertEqual(state.current_anim, 0)
        self.assertTrue(viewer._handle_anchor_key(state, "s", cell_data))
        self.assertEqual(state.current_anim, 1)
        self.assertEqual(state.current_frame, 0)
        self.assertTrue(viewer._handle_anchor_key(state, ".", cell_data))
        self.assertEqual(state.current_frame, 1)
        self.assertTrue(viewer._handle_anchor_key(state, ".", cell_data))
        self.assertEqual(state.current_frame, 2)

    def test_historical_evidence_index_binds_packaged_inputs(self) -> None:
        index = json.loads((ROOT / "docs/historical-evidence/manifest.json").read_text())
        paths = sorted((ROOT / "assets/sprites").glob("*.xp"))
        self.assertEqual(index["xp_assets"]["expected_count"], len(paths))
        self.assertEqual(index["xp_assets"]["expected_count"], 115)
        indexed_paths = {entry["path"]: entry["sha256"] for entry in index["xp_assets"]["paths"]}
        self.assertIn("assets/sprites/player-1100.xp", indexed_paths)
        self.assertEqual(digest(ROOT / "assets/sprites/player-1100.xp"), indexed_paths["assets/sprites/player-1100.xp"])
        self.assertEqual(
            {str(path.relative_to(ROOT)) for path in paths},
            set(indexed_paths),
        )
        for entry in index["source_owned_evidence"]:
            self.assertEqual(digest(ROOT / entry["path"]), entry["sha256"])

    def test_every_packaged_xp_has_a_viewable_raw_layer_dump(self) -> None:
        for path in sorted((ROOT / "assets/sprites").glob("*.xp")):
            result = subprocess.run(
                [
                    sys.executable,
                    str(VIEWER),
                    "--sprite-dir",
                    str(ROOT / "assets/sprites"),
                    "--sprite",
                    path.name,
                    "--layer",
                    "0",
                    "--json",
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            payload = json.loads(result.stdout)
            self.assertEqual(payload["source_asset"], path.name)
            self.assertEqual(payload["layer_index"], 0)

    def test_armored_walkthrough_gif_composites_to_golden_product_states(self) -> None:
        self.assertTrue(GIF.is_file())
        contract = json.loads(GIF_CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(contract["schema_id"], "normalized-xp.armored-inspector-gif.v1")
        self.assertEqual(contract["frame_count"], 8)
        self.assertEqual(
            tuple(contract["semantic_frame_indices"]),
            (
                "composed_uv_body",
                "armor_l3_grid",
                "animation_group_selected",
                "animation_frame_1",
                "animation_frame_2",
                "projection_changed",
                "helmet_l4_grid",
                "helmet_l4_angle_1",
            ),
        )
        self.assertEqual(digest(GIF), contract["gif_sha256"])
        self.assertGreaterEqual(GIF.stat().st_size, 350_000)
        self.assertLessEqual(GIF.stat().st_size, 900_000)

        artifact = decode_composited_gif(GIF)
        self.assertEqual(
            (artifact.width, artifact.height, len(artifact.frames)),
            (contract["width"], contract["height"], contract["frame_count"]),
        )
        # All frames must remain product screens. Together with per-frame proof
        # bands, these fingerprints reject a restored shell or launcher frame.
        self.assertEqual(
            tuple(hashlib.sha256(frame).hexdigest() for frame in artifact.frames),
            tuple(contract["frame_sha256"]),
        )
        self.assertEqual(
            tuple(
                hashlib.sha256(rgb_crop(
                    frame, artifact.width, x=0, y=670, crop_width=1320, crop_height=50,
                )).hexdigest()
                for frame in artifact.frames
            ),
            tuple(contract["caption_sha256"]),
        )
        frame_indices = contract["semantic_frame_indices"]
        self.assertEqual(
            {
                name: hashlib.sha256(artifact.frames[index]).hexdigest()
                for name, index in frame_indices.items()
            },
            contract["semantic_frame_sha256"],
        )
        self.assertEqual(
            {
                name: hashlib.sha256(rgb_crop(
                    artifact.frames[index], artifact.width,
                    x=0, y=670, crop_width=1320, crop_height=50,
                )).hexdigest()
                for name, index in frame_indices.items()
            },
            contract["semantic_caption_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
