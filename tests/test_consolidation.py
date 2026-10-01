from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ConsolidationContract(unittest.TestCase):
    def test_both_entry_points_run_outside_the_checkout_without_input_writes(self) -> None:
        inputs = sorted((ROOT / "assets/sprites").glob("*.xp"))
        inputs += sorted((ROOT / "docs/research").rglob("*"))
        inputs = [path for path in inputs if path.is_file()]

        def fingerprints() -> dict[str, str]:
            return {
                str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in inputs
            }

        before = fingerprints()
        with tempfile.TemporaryDirectory() as directory:
            for command, marker in (
                ("run-inspector.sh", "UV"),
                ("run-viewer.sh", "SOURCE LAYER CONTRACT VIEWER (READ-ONLY)"),
            ):
                with self.subTest(command=command):
                    result = subprocess.run(
                        [str(ROOT / command), "--once"],
                        cwd=directory,
                        check=True,
                        capture_output=True,
                        text=True,
                        timeout=60,
                    )
                    self.assertIn(marker, result.stdout)
            self.assertEqual(list(Path(directory).iterdir()), [])
        self.assertEqual(fingerprints(), before)

    def test_one_index_exposes_both_input_sets_and_frozen_contract(self) -> None:
        manifest = json.loads(
            (ROOT / "docs/historical-evidence/manifest.json").read_text()
        )
        self.assertEqual(manifest["xp_assets"]["expected_count"], 115)
        self.assertEqual(len(manifest["xp_assets"]["paths"]), 115)
        self.assertEqual(manifest["frozen_contract"]["raw_layers"], 573)
        evidence = {entry["path"] for entry in manifest["source_owned_evidence"]}
        prefix = "docs/research/ascii/semantic_maps/"
        self.assertTrue({
            prefix + "player-1100-anchors.json",
            prefix + "layer_evidence_cards.jsonl",
            prefix + "manual_candidate_review.json",
            prefix + "source_layer_review_decisions.jsonl",
            prefix + "family_topology_contracts.json",
            "docs/provenance.md",
        }.issubset(evidence))


if __name__ == "__main__":
    unittest.main()
