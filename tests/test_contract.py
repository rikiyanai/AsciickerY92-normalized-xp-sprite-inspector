from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "normalized_xp_inspector.py"
ASSET = ROOT / "assets" / "player-nude.xp"


class InspectorContract(unittest.TestCase):
    def test_exact_json_contract(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--json"],
            check=True,
            text=True,
            capture_output=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "read-only")
        self.assertEqual(payload["sha256"], hashlib.sha256(ASSET.read_bytes()).hexdigest())
        self.assertEqual(payload["contract"]["angles"], 8)
        self.assertEqual(payload["contract"]["animations"], [1, 8])
        self.assertEqual(payload["contract"]["frame_width"], 7)
        self.assertEqual(payload["contract"]["frame_height"], 9)

    def test_once_is_read_only(self) -> None:
        before = {path: path.stat().st_mtime_ns for path in ROOT.rglob("*") if path.is_file()}
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--once"],
            check=True,
            text=True,
            capture_output=True,
        )
        after = {path: path.stat().st_mtime_ns for path in ROOT.rglob("*") if path.is_file()}
        self.assertEqual(before, after)
        self.assertIn("NORMALIZED XP SPRITE INSPECTOR (READ-ONLY)", result.stdout)
        self.assertIn("layer 3/3", result.stdout)

    def test_unreviewed_asset_is_rejected(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--asset", "/tmp/not-reviewed.xp", "--json"],
            text=True,
            capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("refusing unreviewed asset path", result.stderr)


if __name__ == "__main__":
    unittest.main()
