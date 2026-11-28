"""Check the direction of the four Q51 classes and reproduce the binary groupings."""

import unittest

import pandas as pd

from clean_q51 import make_table
from review_q51 import INPUTS


class Q51TargetTest(unittest.TestCase):
    def test_target_codes_and_skipped_responses(self):
        review = pd.DataFrame({
            "Q51_original_code": [1, 2, -1, 3, 4, -2, -5],
            "B_COUNTRY_ALPHA": "TST", "A_YEAR": 2020, "W_WEIGHT": "1", "S018": "1",
            INPUTS["Q262"]: 40, INPUTS["Q275"]: 0, INPUTS["Q279"]: "Full-time employed",
            INPUTS["Q288"]: 5, INPUTS["Q50"]: 5, INPUTS["Q47"]: "Good", INPUTS["Q54"]: "Never",
        })
        cases = [
            ("frequency", "target_frequency", [3, 2, 1, 0]),
            ("any", "target_any_shortage", [1, 1, 1, 0]),
            ("sometimes-often", "target_sometimes_or_often", [1, 1, 0, 0]),
        ]
        for definition, target, expected in cases:
            with self.subTest(definition=definition):
                result = make_table(review, definition)
                self.assertEqual(result[target].tolist(), expected)
                self.assertEqual(result["meta_source_row"].tolist(), [1, 2, 4, 5])
                self.assertEqual(result.filter(regex="^target_").columns.tolist(), [target])


if __name__ == "__main__":
    unittest.main()
