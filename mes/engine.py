"""Manufacturing Execution System (MES), Real-Time Machine Telemetry & OEE Analytics Engine."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ShiftProductionLog(BaseModel):
    machine_id: str
    machine_name: str
    shift_name: str           # SHIFT_A, SHIFT_B, NIGHT
    total_planned_shift_minutes: float = 480.0  # 8 hours = 480 mins
    unplanned_downtime_minutes: float = 0.0     # breakdown, tool jam
    planned_downtime_minutes: float = 30.0      # tea break, shift handover
    ideal_cycle_time_seconds: float             # design speed per part
    total_parts_produced: int
    rejected_scrap_parts: int
    downtime_reasons: List[Dict[str, Any]] = Field(default_factory=list)


class OEEMetricsResult(BaseModel):
    machine_id: str
    machine_name: str
    availability_pct: float
    performance_pct: float
    quality_pct: float
    overall_oee_pct: float
    world_class_benchmark_status: str  # WORLD_CLASS (>=85%), ACCEPTABLE (>=70%), CRITICAL_DEFICIENT (<70%)
    good_parts_count: int
    scrap_cost_impact: float


class ShopFloorMESEngine:
    """Computes Six Big Losses, Workstation OEE, and Shift Rejection Analytics."""

    def calculate_oee(self, log: ShiftProductionLog, part_scrap_value: float = 120.0) -> OEEMetricsResult:
        # 1. Operating Time & Availability
        planned_production_time = log.total_planned_shift_minutes - log.planned_downtime_minutes
        if planned_production_time <= 0:
            raise ValueError("Planned production time must be positive.")

        operating_time = planned_production_time - log.unplanned_downtime_minutes
        availability = max(0.0, min(1.0, operating_time / planned_production_time))

        # 2. Performance = (Total Parts * Ideal Cycle Time in seconds) / (Operating Time in seconds)
        operating_time_seconds = operating_time * 60.0
        if operating_time_seconds > 0:
            performance = (log.total_parts_produced * log.ideal_cycle_time_seconds) / operating_time_seconds
            performance = max(0.0, min(1.0, performance))
        else:
            performance = 0.0

        # 3. Quality = Good Parts / Total Parts
        good_parts = max(0, log.total_parts_produced - log.rejected_scrap_parts)
        if log.total_parts_produced > 0:
            quality = good_parts / log.total_parts_produced
        else:
            quality = 1.0

        # OEE = A * P * Q
        oee = availability * performance * quality
        oee_pct = round(oee * 100.0, 2)

        if oee_pct >= 85.0:
            status = "WORLD_CLASS_OEE"
        elif oee_pct >= 70.0:
            status = "ACCEPTABLE_PRODUCTIVITY"
        else:
            status = "CRITICAL_DEFICIENT_ACTION_REQUIRED"

        scrap_cost = log.rejected_scrap_parts * part_scrap_value

        return OEEMetricsResult(
            machine_id=log.machine_id,
            machine_name=log.machine_name,
            availability_pct=round(availability * 100.0, 2),
            performance_pct=round(performance * 100.0, 2),
            quality_pct=round(quality * 100.0, 2),
            overall_oee_pct=oee_pct,
            world_class_benchmark_status=status,
            good_parts_count=good_parts,
            scrap_cost_impact=round(scrap_cost, 2)
        )
