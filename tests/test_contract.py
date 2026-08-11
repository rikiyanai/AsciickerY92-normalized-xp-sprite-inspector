from __future__ import annotations

import hashlib
import importlib.util
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "run-inspector.sh"
VIEWER = ROOT / "scripts" / "xp_uv_body_viewer.py"
ANCHOR = ROOT / "docs" / "research" / "ascii" / "semantic_maps" / "player-1100-anchors.json"
SPRITE = ROOT / "assets" / "sprites" / "player-1100.xp"
EVIDENCE = ROOT / "docs" / "research" / "ascii" / "semantic_maps" / "layer_evidence_cards.jsonl"
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


if __name__ == "__main__":
    unittest.main()
