import unittest

from src import Delivery

class TestDelivery(unittest.TestCase):

    def test_normal_delivery(self):
        result = Delivery.calculate_delivery_cost(
            1.0, 100, "обычный"
        )

        self.assertEqual(
            result,
            (700, "2026-09-04")
        )

    def test_min_weight(self):
        result = Delivery.calculate_delivery_cost(
            0.1, 100, "обычный"
        )

        self.assertEqual(
            result,
            (700, "2026-09-04")
        )

    def test_max_weight(self):
        result = Delivery.calculate_delivery_cost(
            50.0, 100, "обычный"
        )

        self.assertEqual(
            result,
            (1050, "2026-09-04")
        )

    def test_invalid_weight_too_small(self):
        result = Delivery.calculate_delivery_cost(
            0.01, 100, "обычный"
        )

        self.assertEqual(
            result,
            (-1, "0000-00-00")
        )

    def test_invalid_weight_too_large(self):
        result = Delivery.calculate_delivery_cost(
            50.5, 100, "обычный"
        )

        self.assertEqual(
            result,
            (-1, "0000-00-00")
        )

    def test_invalid_distance_too_small(self):
        result = Delivery.calculate_delivery_cost(
            1.0, 0, "обычный"
        )

        self.assertEqual(
            result,
            (-1, "0000-00-00")
        )

    def test_invalid_distance_too_large(self):
        result = Delivery.calculate_delivery_cost(
            1.0, 50000, "обычный"
        )

        self.assertEqual(
            result,
            (-1, "0000-00-00")
        )

    def test_invalid_package_type(self):
        result = Delivery.calculate_delivery_cost(
            1.0, 100, "eqwrtthegr"
        )

        self.assertEqual(
            result,
            (-1, "0000-00-00")
        )

    def test_fragile_package(self):
        result = Delivery.calculate_delivery_cost(
            1.0, 100, "хрупкий"
        )

        self.assertEqual(
            result,
            (1000, "2026-09-04")
        )

    def test_dangerous_package(self):
        result = Delivery.calculate_delivery_cost(
            1.0, 100, "опасный"
        )

        self.assertEqual(
            result,
            (1700, "2026-09-04")
        )

    def test_weight_from_5_to_20(self):
        result = Delivery.calculate_delivery_cost(
            12.0, 100, "обычный"
        )

        self.assertEqual(
            result,
            (840, "2026-09-04")
        )

    def test_weight_more_20_kg(self):
        result = Delivery.calculate_delivery_cost(
            30.0, 100, "обычный"
        )

        self.assertEqual(
            result,
            (1050, "2026-09-04")
        )

    def test_delivery_with_express(self):
        result = Delivery.calculate_delivery_cost(
            1.0, 100, "обычный", True
        )

        self.assertEqual(
            result,
            (350, "2026-09-04") #  Tuples differ: (350, '2026-09-03') != (350, '2026-09-04')

        )

    def test_long_distance(self):
        result = Delivery.calculate_delivery_cost(
            1.0, 1000, "обычный"
        )

        self.assertEqual(
            result,
            (5200, "2026-09-05")

        )

    def test_long_distance_with_express(self):
        result = Delivery.calculate_delivery_cost(
            1.0, 1000, "обычный", True
        )

        self.assertEqual(
            result,
            (2600, "2026-09-04")
        )


if __name__ == "__main__":
    unittest.main()