from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "part_orders.csv"
PALLET = {"length_mm": 1200, "width_mm": 1000, "height_mm": 1500, "max_mass_kg": 900}


@dataclass
class PartOrder:
    part_id: str
    length_mm: float
    width_mm: float
    height_mm: float
    mass_kg: float
    mean_weekly_demand: float
    demand_std: float


def load_orders(path: Path = DATA_PATH) -> list[PartOrder]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [
            PartOrder(
                part_id=row["part_id"],
                length_mm=float(row["length_mm"]),
                width_mm=float(row["width_mm"]),
                height_mm=float(row["height_mm"]),
                mass_kg=float(row["mass_kg"]),
                mean_weekly_demand=float(row["mean_weekly_demand"]),
                demand_std=float(row["demand_std"]),
            )
            for row in csv.DictReader(handle)
        ]


def enclosure(part: PartOrder) -> dict[str, float]:
    clearance = 38.0
    wall = 8.0 if part.mass_kg < 15.0 else 12.0
    length = part.length_mm + 2.0 * (clearance + wall)
    width = part.width_mm + 2.0 * (clearance + wall)
    height = part.height_mm + 2.0 * (clearance + wall)
    surface_area_m2 = 2.0 * (length * width + length * height + width * height) / 1_000_000.0
    material_mass_kg = surface_area_m2 * wall * 0.72
    return {
        "length_mm": length,
        "width_mm": width,
        "height_mm": height,
        "wall_mm": wall,
        "material_mass_kg": round(material_mass_kg, 2),
    }


def structural_safety_factor(part: PartOrder, box: dict[str, float]) -> float:
    section_factor = box["wall_mm"] / 8.0
    load_factor = max(1.0, part.mass_kg / 12.0)
    slenderness_penalty = max(box["height_mm"] / min(box["length_mm"], box["width_mm"]), 1.0)
    return round(2.4 * section_factor / (load_factor * 0.35 * slenderness_penalty), 2)


def pallet_count(box: dict[str, float], mass_kg: float) -> int:
    fit_length = math.floor(PALLET["length_mm"] / box["length_mm"])
    fit_width = math.floor(PALLET["width_mm"] / box["width_mm"])
    fit_height = math.floor(PALLET["height_mm"] / box["height_mm"])
    geometric_fit = max(0, fit_length * fit_width * fit_height)
    mass_fit = math.floor(PALLET["max_mass_kg"] / mass_kg)
    return max(0, min(geometric_fit, mass_fit))


def safety_stock(mean: float, std: float, service_z: float = 1.65) -> int:
    return math.ceil(mean + service_z * std)


def slotting_score(order: PartOrder, pallet_units: int) -> float:
    demand_pressure = order.mean_weekly_demand / max(1, pallet_units)
    travel_penalty = 1.0 if order.mean_weekly_demand > 80 else 1.35
    return round(demand_pressure * travel_penalty, 2)


def run_optimizer() -> None:
    for order in load_orders():
        box = enclosure(order)
        total_unit_mass = order.mass_kg + box["material_mass_kg"]
        pallet_units = pallet_count(box, total_unit_mass)
        stock = safety_stock(order.mean_weekly_demand, order.demand_std)
        score = slotting_score(order, pallet_units)
        slot = "forward pick zone" if score >= 10 else "reserve racking"

        print(
            f"{order.part_id}: enclosure={box['length_mm']:.0f}x{box['width_mm']:.0f}x{box['height_mm']:.0f} mm, "
            f"wall={box['wall_mm']:.0f} mm, safety_factor={structural_safety_factor(order, box):0.2f}"
        )
        print(
            f"  pallet_units={pallet_units}, weekly_stock_target={stock}, "
            f"slotting_score={score}, recommended_slot={slot}"
        )


if __name__ == "__main__":
    run_optimizer()
