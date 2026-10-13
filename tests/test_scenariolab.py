import unittest
from scenariolab import audit


class AuditTests(unittest.TestCase):
    def test_feasible_change(self):
        result = audit([[1, 2], [3, 4]], [[1, 3], [3, 4]],
                       {"immutable_features": [0], "bounds": {"1": [0, 5]}, "max_l1_change": 1})
        self.assertTrue(result["feasible"])
        self.assertEqual(result["l1_change"], 1)

    def test_all_violations(self):
        result = audit([[1]], [[9]], {"immutable_features": [0], "bounds": {"0": [0, 5]}, "max_l1_change": 2})
        self.assertEqual({x["kind"] for x in result["violations"]}, {"immutable", "bounds", "budget"})

    def test_bad_shape_and_nonfinite(self):
        for candidate in ([], [[1], [2]], [[float("nan")]], [[True]]):
            with self.assertRaises(ValueError):
                audit([[1]], candidate, {})

    def test_invalid_constraints(self):
        for constraints in ({"immutable_features": [3]}, {"bounds": {"0": [9, 2]}}, {"max_l1_change": -1}):
            with self.assertRaises(ValueError):
                audit([[1]], [[1]], constraints)

    def test_no_change(self):
        result = audit([[2]], [[2]], {})
        self.assertEqual(result["changed_points"], 0)
        self.assertTrue(result["feasible"])
