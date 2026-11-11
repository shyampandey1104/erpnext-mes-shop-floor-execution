import unittest
from mes.engine import ShopFloorMESEngine, ShiftProductionLog


class TestShopFloorMES(unittest.TestCase):
    def setUp(self):
        self.engine = ShopFloorMESEngine()

    def test_oee_calculation(self):
        # 8-hr shift (480 mins), 30 mins planned break, 30 mins breakdown -> Operating = 420 mins
        # Ideal cycle = 30 seconds per part -> In 420 mins (25,200s), max ideal parts = 840 parts
        # Produced = 800 parts, 20 rejected -> Good = 780
        log = ShiftProductionLog(
            machine_id="CNC-MILL-04",
            machine_name="Mazak 5-Axis CNC Mill",
            shift_name="SHIFT_A",
            total_planned_shift_minutes=480.0,
            planned_downtime_minutes=30.0,
            unplanned_downtime_minutes=30.0,  # Availability = 420/450 = 93.33%
            ideal_cycle_time_seconds=30.0,
            total_parts_produced=800,
            rejected_scrap_parts=20,
            downtime_reasons=[{"reason": "Tool insert replacement", "duration_mins": 30.0}]
        )
        res = self.engine.calculate_oee(log, part_scrap_value=250.0)
        self.assertAlmostEqual(res.availability_pct, 93.33, places=1)
        self.assertGreater(res.performance_pct, 90.0)
        self.assertEqual(res.good_parts_count, 780)
        self.assertEqual(res.scrap_cost_impact, 5000.0)
        self.assertIn(res.world_class_benchmark_status, ("WORLD_CLASS_OEE", "ACCEPTABLE_PRODUCTIVITY"))


if __name__ == "__main__":
    unittest.main()
