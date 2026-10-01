from __future__ import annotations

import subprocess
import sys
import unittest
import hashlib
import json
import os
import struct
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def _read_sub_blocks(payload: bytes, offset: int) -> tuple[bytes, int]:
    blocks = bytearray()
    while True:
        size = payload[offset]
        offset += 1
        if size == 0:
            return bytes(blocks), offset
        blocks.extend(payload[offset:offset + size])
        offset += size


def _decode_gif_lzw(encoded: bytes, minimum_code_size: int) -> bytes:
    clear_code = 1 << minimum_code_size
    end_code = clear_code + 1
    code_size = minimum_code_size + 1
    dictionary = {index: bytes([index]) for index in range(clear_code)}
    next_code = end_code + 1
    previous = None
    output = bytearray()
    bit_offset = 0

    def read_code(width: int) -> int | None:
        nonlocal bit_offset
        if bit_offset + width > len(encoded) * 8:
            return None
        value = 0
        for bit in range(width):
            value |= ((encoded[(bit_offset + bit) // 8] >> ((bit_offset + bit) % 8)) & 1) << bit
        bit_offset += width
        return value

    while (code := read_code(code_size)) is not None:
        if code == clear_code:
            dictionary = {index: bytes([index]) for index in range(clear_code)}
            code_size = minimum_code_size + 1
            next_code = end_code + 1
            previous = None
            continue
        if code == end_code:
            break
        entry = dictionary.get(code)
        if entry is None:
            if previous is None or code != next_code:
                raise AssertionError("GIF LZW stream has an invalid code")
            entry = previous + previous[:1]
        output.extend(entry)
        if previous is not None and next_code < 4096:
            dictionary[next_code] = previous + entry[:1]
            next_code += 1
            if next_code == (1 << code_size) and code_size < 12:
                code_size += 1
        previous = entry
    return bytes(output)


def _deinterlace_gif_indices(indices: bytes, width: int, height: int) -> bytes:
    rows = [b"" for _ in range(height)]
    offset = 0
    for first_row, step in ((0, 8), (4, 8), (2, 4), (1, 2)):
        for y in range(first_row, height, step):
            rows[y] = indices[offset:offset + width]
            offset += width
    return b"".join(rows)


def _decode_gif_samples(
    payload: bytes,
    wanted_frames: set[int],
) -> tuple[int, dict[int, bytes], list[int]]:
    """Decode/composite GIF frames and retain every frame's hold duration."""
    assert payload[:6] == b"GIF89a"
    width, height = struct.unpack("<HH", payload[6:10])
    packed, background_index = payload[10], payload[11]
    offset = 13

    def color_table(size: int) -> list[bytes]:
        nonlocal offset
        colors = [payload[index:index + 3] for index in range(offset, offset + size * 3, 3)]
        offset += size * 3
        return colors

    global_palette = color_table(1 << ((packed & 0x07) + 1)) if packed & 0x80 else []
    background = global_palette[background_index] if global_palette else b"\x00\x00\x00"
    canvas = bytearray(background * (width * height))
    previous_disposal = 0
    previous_rect = (0, 0, 0, 0)
    previous_canvas = None
    pending_disposal = 0
    pending_transparency = None
    pending_delay = 0
    frame_number = 0
    samples: dict[int, bytes] = {}
    frame_delays: list[int] = []

    while offset < len(payload):
        marker = payload[offset]
        offset += 1
        if marker == 0x3B:
            break
        if marker == 0x21:
            label = payload[offset]
            offset += 1
            if label == 0xF9:
                assert payload[offset] == 4
                control = payload[offset + 1]
                pending_delay = struct.unpack("<H", payload[offset + 2:offset + 4])[0]
                pending_transparency = payload[offset + 4] if control & 1 else None
                pending_disposal = (control >> 2) & 0x07
                offset += 6
            else:
                _, offset = _read_sub_blocks(payload, offset)
            continue
        assert marker == 0x2C

        if previous_disposal == 2:
            left, top, image_width, image_height = previous_rect
            for y in range(top, top + image_height):
                canvas[(y * width + left) * 3:(y * width + left + image_width) * 3] = background * image_width
        elif previous_disposal == 3 and previous_canvas is not None:
            canvas[:] = previous_canvas

        left, top, image_width, image_height, image_packed = struct.unpack("<HHHHB", payload[offset:offset + 9])
        offset += 9
        assert (left, top, image_width, image_height) == (0, 0, width, height), (
            "each accepted GIF state must store a complete rendered canvas"
        )
        palette = color_table(1 << ((image_packed & 0x07) + 1)) if image_packed & 0x80 else global_palette
        minimum_code_size = payload[offset]
        offset += 1
        encoded, offset = _read_sub_blocks(payload, offset)
        indices = _decode_gif_lzw(encoded, minimum_code_size)
        assert len(indices) == image_width * image_height
        if image_packed & 0x40:
            indices = _deinterlace_gif_indices(indices, image_width, image_height)
        previous_canvas = canvas[:] if pending_disposal == 3 else None
        for y in range(image_height):
            for x in range(image_width):
                index = indices[y * image_width + x]
                if index != pending_transparency:
                    pixel = ((top + y) * width + left + x) * 3
                    canvas[pixel:pixel + 3] = palette[index]
        previous_rect = (left, top, image_width, image_height)
        previous_disposal = pending_disposal
        pending_disposal = 0
        pending_transparency = None
        if frame_number in wanted_frames:
            samples[frame_number] = bytes(canvas)
        frame_delays.append(pending_delay)
        pending_delay = 0
        frame_number += 1
    return frame_number, samples, frame_delays


class SourceLayerContract(unittest.TestCase):
    def test_frozen_corpus_totals_and_read_only_screen(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/source_layer_contract_viewer.py"), "--once"],
            check=True,
            text=True,
            capture_output=True,
        )
        self.assertIn("SOURCE LAYER CONTRACT VIEWER (READ-ONLY)", result.stdout)
        self.assertIn("115 XP / 573 raw layers", result.stdout)
        self.assertIn("6,807,104", result.stdout)
        self.assertIn("3,340,170", result.stdout)

    def test_manifest_resolves_exactly_115_xp_files(self) -> None:
        from source_layer_contract_viewer import ContractData

        data = ContractData()
        self.assertEqual(len(data.stems()), 115)
        for stem in data.stems():
            self.assertTrue((ROOT / "assets/sprites" / f"{stem}.xp").is_file())

    def test_every_frozen_xp_asset_matches_its_ledger_hash(self) -> None:
        from source_layer_contract_viewer import ContractData

        data = ContractData()
        verified_paths: set[Path] = set()
        for stem in data.stems():
            source_key = data.layer_keys_for_stem(stem)[0]
            asset_path = ROOT / data.source_xp_path(source_key)
            actual_hash = hashlib.sha256(asset_path.read_bytes()).hexdigest()
            self.assertEqual(actual_hash, data.source_xp_sha256(source_key), source_key)
            verified_paths.add(asset_path)
        self.assertEqual(len(verified_paths), 115)

    def test_xp_loader_rejects_a_same_name_asset_with_wrong_bytes(self) -> None:
        from source_layer_contract_viewer import ContractData, ContractDataError, ViewerState

        data = ContractData()
        layer_keys = data.layer_keys_for_stem("player-1100")
        with tempfile.TemporaryDirectory() as directory:
            sprites = Path(directory)
            asset = sprites / "player-1100.xp"
            asset.write_bytes((ROOT / "assets/sprites/player-1100.xp").read_bytes() + b"changed")
            state = ViewerState("player-1100", layer_keys, sprites=sprites)
            with self.assertRaisesRegex(ContractDataError, "source XP hash mismatch"):
                state.xp_for_key("player-1100-L3", data)

    def test_corrupt_asset_cli_returns_controlled_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sprites = Path(directory)
            asset = sprites / "player-1100.xp"
            asset.write_bytes((ROOT / "assets/sprites/player-1100.xp").read_bytes() + b"changed")
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/source_layer_contract_viewer.py"),
                    "--sprites",
                    str(sprites),
                    "--source-key",
                    "player-1100-L3",
                    "--compact",
                    "--once",
                ],
                text=True,
                capture_output=True,
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn("FAIL: source XP hash mismatch", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_manifest_has_no_live_absolute_desktop_owner(self) -> None:
        path = ROOT / "docs/research/ascii/semantic_maps/upstream_xp_cell_contract/manifest.json"
        payload = json.loads(path.read_text())
        self.assertEqual(
            payload["source_final"]["path"],
            "historical-source:/bundle_layer_audit_20260520/verifier_state_backups/state_FINAL_20260521-163326.json",
        )
        self.assertNotIn("/" + "Users/", path.read_text())

    def test_compact_armored_contract_surface_is_readable_and_complete(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/source_layer_contract_viewer.py"),
                "--source-key",
                "player-1100-L3",
                "--compact",
                "--once",
            ],
            check=True,
            text=True,
            capture_output=True,
            env={**os.environ, "COLUMNS": "110", "LINES": "36"},
        )
        screen = result.stdout
        self.assertIn("FINAL SPRITE", screen)
        self.assertIn("SELECTED L3", screen)
        self.assertIn("FROZEN SOURCE-LAYER CONTRACT", screen)
        self.assertIn("L2 player_body [shown]", screen)
        self.assertIn("L3 player_armor_regular [shown]", screen)
        self.assertIn("L4 player_helmet_regular [shown]", screen)
        self.assertIn("11/11 visible cells assigned · 0 unresolved", screen)
        self.assertEqual(screen.count("FRAME "), 3)
        gif_path = ROOT / "docs/recordings/source-layer-contract-viewer.gif"
        self.assertTrue(gif_path.is_file())
        gif = gif_path.read_bytes()
        self.assertEqual(gif[:6], b"GIF89a")
        self.assertEqual(struct.unpack("<HH", gif[6:10]), (1000, 700))
        self.assertIn(
            "docs/recordings/source-layer-contract-viewer.gif",
            (ROOT / "README.md").read_text(),
        )

    def test_recording_recipe_captures_only_thirteen_fast_rendered_states(self) -> None:
        tape = (ROOT / "docs/recordings/source-layer-contract-viewer.tape").read_text()
        self.assertIn('Set Width 1000', tape)
        self.assertIn('Set Height 700', tape)
        startup = 'Type "./run-viewer.sh --source-key player-1100-L3 --compact" Enter'
        wait = 'Wait+Screen /SOURCE LAYER CONTRACT VIEWER/'
        first_hide = tape.index('Hide')
        startup_at = tape.index(startup)
        wait_at = tape.index(wait)
        show_at = tape.index('Show')
        self.assertLess(first_hide, startup_at)
        self.assertLess(startup_at, wait_at)
        self.assertLess(wait_at, show_at)
        self.assertNotIn(startup, tape[show_at:])
        self.assertNotIn("Output ", tape)
        self.assertEqual(tape.count('Screenshot "@@BUILD_DIR@@/'), 13)
        interaction_sequence = [
            'Type "n"',
            'Type "n"',
            'Type "."',
            'Type "r"',
            'Type "]"',
            'Type "v"',
            'Type "v"',
            'Type "]"',
            'Type "]"',
            'Type "]"',
            'Type "."',
            'Type "n"',
            'Type "}"',
        ]
        positions = []
        cursor = show_at
        for action in interaction_sequence:
            cursor = tape.index(action, cursor) + len(action)
            positions.append(cursor)
        self.assertEqual(positions, sorted(positions))

    def test_every_decoded_gif_frame_matches_an_accepted_viewer_state(self) -> None:
        gif = (ROOT / "docs/recordings/source-layer-contract-viewer.gif").read_bytes()
        accepted_frames = set(range(13))
        frame_count, samples, frame_delays = _decode_gif_samples(gif, accepted_frames)
        self.assertEqual(frame_count, 13)
        self.assertEqual(set(samples), accepted_frames)
        self.assertEqual(frame_delays, [18] * 13)
        self.assertEqual(
            {frame: hashlib.sha256(image).hexdigest() for frame, image in samples.items()},
            {
                # Armor frames 1-3, angle/projection changes, helmet hide/restore,
                # raw L0/L1/L2 layer navigation, angle/frame change, and next XP.
                0: "fef8a80bd692ce3c719561f0c7d0da3415ad513ca4c82d9fa723adf613fe2f0d",
                1: "334ec1296f2349fb9db3d9bbc64a10285ea9e0a12ba87e834d6ad1aec4a0b86f",
                2: "9a30bced2ec4bced4e75c3fdf78ce91c6d38f9b5d4aee81e394adbebc55f9bfc",
                3: "8dc1db88e3a07ae3ba0e7c01a1ecaafb451bd8bb86104f5ca68ee0d7e3dc7762",
                4: "756c1d241d0bb0afa2aec09a9e377f192a79a2beb81e430c903def1fa3a17b6b",
                5: "a0fc11126782eedc8dd1406ba9a7bd499aa5dec966b5897b5e475d7ab7689620",
                6: "1126d5632653db1642464bc4c3b7f1c2a5cbe09737011f1b28ab9ebc0d28babe",
                7: "a0fc11126782eedc8dd1406ba9a7bd499aa5dec966b5897b5e475d7ab7689620",
                8: "9ea98f74201e043250592e7167077963a7ed450d986092fca2ca550dda5ae33e",
                9: "14cd474a8a4c371e4ab90f53a1afd39ada53f645e65c2fa294e1d11b755a0410",
                10: "37f740e0a1db3d70e716e7c0406111e162daaaa5e3720f7d3cebc4b3b745d5c5",
                11: "7a4f332e04fff8837557faa636d9d66f90de87eb76770dfa3c3c4e8da1dff50b",
                12: "448f3f4bf1bc55f3787dc66641b23284f0fe95b95e9df280e30f2614906d91e8",
            },
        )

    def test_historical_evidence_index_binds_complete_corpus(self) -> None:
        index = json.loads((ROOT / "docs/historical-evidence/manifest.json").read_text())
        paths = sorted((ROOT / "assets/sprites").glob("*.xp"))
        self.assertEqual(index["xp_assets"]["expected_count"], len(paths))
        self.assertEqual(index["xp_assets"]["expected_count"], 115)
        self.assertEqual(index["frozen_contract"]["raw_layers"], 573)
        for entry in index["source_owned_evidence"]:
            self.assertTrue((ROOT / entry["path"]).is_file(), entry["path"])

    def test_compact_surface_reports_layer_hide_state(self) -> None:
        from source_layer_contract_viewer import (
            ContractData,
            ViewerState,
            compose_screen,
            handle_key,
        )

        data = ContractData()
        layer_keys = data.layer_keys_for_stem("player-1100")
        state = ViewerState(
            "player-1100",
            layer_keys,
            corpus_layer_keys=data.corpus_layer_map(),
        )
        state.layer_idx = layer_keys.index("player-1100-L3")
        state.compact = True
        self.assertTrue(handle_key(state, "v", data))
        screen = compose_screen(state, data)
        self.assertIn("L3 player_armor_regular [hidden]", screen)
        self.assertIn("HIDDEN-FROM-STACK", screen)

    def test_angle_navigation_wraps_state_to_selected_atlas_rows(self) -> None:
        from source_layer_contract_viewer import ContractData, ViewerState, handle_key, slice_frame

        data = ContractData()
        layer_keys = data.layer_keys_for_stem("player-1100")
        state = ViewerState("player-1100", layer_keys, corpus_layer_keys=data.corpus_layer_map())
        state.layer_idx = layer_keys.index("player-1100-L3")
        info = data.join(state.current_key)
        xp = state.xp_for_key(state.current_key, data)
        layer = xp.layers[info["raw_layer_index"]]
        rows = slice_frame(layer, info["frame_wh"], 0, 0)["rows"]

        for _ in range(rows * 2 + 3):
            self.assertTrue(handle_key(state, ".", data))
        self.assertEqual(state.angle, 3)
        self.assertLess(state.angle, rows)

        for _ in range(4):
            self.assertTrue(handle_key(state, ",", data))
        self.assertEqual(state.angle, rows - 1)
        self.assertLess(state.angle, rows)


if __name__ == "__main__":
    unittest.main()
