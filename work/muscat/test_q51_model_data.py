"""Checks for accidentally assigning a respondent to the wrong partition."""

import unittest

import pandas as pd

from q51_model_data import KEY, TARGET, align_split, proposed_split


class SharedSplitTest(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({KEY: range(101, 181), TARGET: [0, 1, 2, 3] * 20})
        self.assignments = proposed_split(self.data)

    def test_row_order_does_not_change_partition_membership(self):
        shuffled = self.data.sample(frac=1, random_state=11)
        pd.testing.assert_frame_equal(proposed_split(shuffled), self.assignments)
        actual = align_split(shuffled, self.assignments.sample(frac=1, random_state=12))
        expected = self.assignments.set_index(KEY)["split"]
        self.assertEqual(actual.tolist(), expected.loc[shuffled[KEY]].tolist())
        self.assertEqual(actual.value_counts().to_dict(), {"train": 64, "test": 16})

    def test_rejects_missing_duplicate_and_unrecognised_assignments(self):
        duplicate = self.assignments.copy()
        duplicate.loc[1, KEY] = duplicate.loc[0, KEY]
        unknown = self.assignments.copy()
        unknown.loc[0, KEY] = 1000
        bad_partition = self.assignments.copy()
        bad_partition.loc[0, "split"] = "validation"
        for malformed in (self.assignments.iloc[1:], duplicate, unknown, bad_partition):
            with self.subTest(first_assignment=malformed.iloc[0].tolist()), self.assertRaises(ValueError):
                align_split(self.data, malformed)

    def test_training_set_must_cover_all_four_q51_answers(self):
        missing_class = self.assignments.copy()
        missing_class.loc[missing_class[KEY].isin(self.data.loc[self.data[TARGET].eq(3), KEY]), "split"] = "test"
        with self.assertRaisesRegex(ValueError, "each class"):
            align_split(self.data, missing_class)


if __name__ == "__main__":
    unittest.main()
