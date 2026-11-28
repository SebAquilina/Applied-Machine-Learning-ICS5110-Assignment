"""Regression checks for the four-class evaluation and separate recurring-shortage alert."""

import unittest

from q51_performance import alert_counts, choose_alert, multiclass_scores


class PerformanceTest(unittest.TestCase):
    def test_alert_uses_both_recurring_classes_and_costs_misses_twice(self):
        result = alert_counts([0, 1, 2, 3, 3], [0.8, 0.1, 0.2, 0.7, 0.4], 0.5)
        self.assertEqual((result["hits"], result["misses"], result["false_alarms"]), (1, 2, 1))
        self.assertEqual(result["correct_negatives"], 1)
        self.assertEqual(result["illustrative_cost"], 5)

    def test_equal_alert_cost_uses_the_higher_cutoff(self):
        _, threshold = choose_alert([3, 0], [0.86, 0.24])
        self.assertEqual(threshold, 0.85)

    def test_four_class_metrics_include_zero_recall_and_ordinal_distance(self):
        scores = multiclass_scores([0, 1, 2, 3], [0, 0, 0, 0])
        self.assertEqual(scores["accuracy"], 0.25)
        self.assertEqual(scores["macro_recall"], 0.25)
        self.assertAlmostEqual(scores["macro_f1"], 0.10)
        self.assertEqual(scores["mean_absolute_class_error"], 1.5)


if __name__ == "__main__":
    unittest.main()
