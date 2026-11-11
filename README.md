# ERPNext Industrial MES & OEE Telemetry System 🏭⚙️

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![ERPNext](https://img.shields.io/badge/ERPNext-v14%20%7C%20v15-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

An enterprise-grade Manufacturing Execution System (MES), CNC machine sensor telemetry tracker, and Overall Equipment Effectiveness (OEE) analytics engine for **ERPNext Manufacturing** (designed for heavy automotive, aerospace, and precision engineering plants).

---

## 🚀 Key Features

- **Automated OEE Calculation**: Tracks Availability, Performance, and Quality metrics against Six Big Losses and World-Class OEE (85%+) benchmarks.
- **Unplanned Machine Downtime Tracking**: Captures root-cause downtime logs (tool jam, motor overheat, lack of raw material, maintenance).
- **Quality Rejection & Scrap Analysis**: Distinguishes sound finished parts from scrap defects and computes rupee scrap cost impact per shift.
- **Workstation Job Card Integration**: Feeds live machine telemetry data directly into ERPNext `Work Order` and `Job Card` DocTypes.

---

## 📦 Installation & Setup

```bash
git clone https://github.com/shyampandey1104/erpnext-mes-shop-floor-execution.git
cd erpnext-mes-shop-floor-execution
pip install -r requirements.txt
```

---

## 🛠️ Usage Example

```python
from mes.engine import ShopFloorMESEngine, ShiftProductionLog

engine = ShopFloorMESEngine()

shift_data = ShiftProductionLog(
    machine_id="CNC-VMC-01",
    machine_name="Doosan VMC Machining Center",
    shift_name="MORNING_SHIFT",
    total_planned_shift_minutes=480.0,
    planned_downtime_minutes=30.0,
    unplanned_downtime_minutes=25.0,
    ideal_cycle_time_seconds=45.0,
    total_parts_produced=550,
    rejected_scrap_parts=12
)

oee = engine.calculate_oee(shift_data, part_scrap_value=350.0)
print(f"OEE: {oee.overall_oee_pct}% | Status: {oee.world_class_benchmark_status} | Scrap Cost: ₹{oee.scrap_cost_impact}")
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 📄 License
MIT License. Created with ❤️ by [Shyam Pandey](https://github.com/shyampandey1104).
