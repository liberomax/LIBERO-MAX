import json
import unittest
from collections import Counter
from pathlib import Path

from libero_max.manifest import validate_manifest


RELEASE = Path(__file__).parents[1] / "benchmark" / "max8000"


class Max8000ReleaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((RELEASE / "libero_max_8000.json").read_text())

    def test_release_has_unique_balanced_cases(self):
        manifest = self.manifest
        self.assertEqual(validate_manifest(manifest), [])
        self.assertEqual(manifest["benchmark_version"], "3.0.0")
        self.assertEqual(manifest["protocol"]["profile"], "official")
        cases = manifest["cases"]
        self.assertEqual(len(cases), 8000)
        self.assertEqual(len({case["case_id"] for case in cases}), 8000)
        events = Counter(case["scenario"]["change_type"] for case in cases)
        self.assertEqual(len(events), 8)
        self.assertEqual(set(events.values()), {1000})
        source_events = Counter(
            (case.get("substrate_variant", {}).get("benchmark") == "LIBERO-PRO",
             case["scenario"]["change_type"])
            for case in cases
        )
        for event in events:
            self.assertEqual(source_events[(False, event)], 700)
            self.assertEqual(source_events[(True, event)], 300)

    def test_pro_cases_use_the_pinned_source(self):
        source = json.loads((RELEASE / "pro_source_lock.json").read_text())
        self.assertEqual(
            source["pro_runtime_revision_tested"],
            "2b910b5b5f53016bef9907632f6f840f1ce2229c",
        )
        self.assertIn(source["dataset_revision"],
                      self.manifest["protocol"]["source_benchmark_commit"])
        cases = [case for case in self.manifest["cases"]
                 if case.get("substrate_variant", {}).get("benchmark") == "LIBERO-PRO"]
        self.assertEqual(len(cases), 2400)
        self.assertEqual({case["substrate_category"] for case in cases},
                         {"LIBERO-PRO/" + category for category in source["included_categories"]})


if __name__ == "__main__":
    unittest.main()
