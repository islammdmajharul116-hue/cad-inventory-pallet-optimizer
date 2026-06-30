# AI-Driven Stochastic Inventory Optimizer and Automated CAD Pallet Configurator

This project is a runnable prototype for connecting physical packaging geometry to warehouse and logistics optimization. It simulates CAD-driven enclosure resizing, structural mass checks, stochastic inventory demand, pallet packing, and warehouse slotting.

## Why It Matters

Supply chain disruptions often force changes in part geometry, packaging materials, and shipping configurations. Those changes can break pallet density, warehouse slotting, and forklift travel efficiency.

## What Is Included

- `src/cad_inventory_pallet_optimizer.py` - geometry, inventory, and pallet prototype
- `data/part_orders.csv` - sample part dimensions and demand uncertainty
- `requirements.txt` - no external packages required
- `GITHUB_NOTES.md` - how to publish this project to GitHub

## Run

```bash
python src/cad_inventory_pallet_optimizer.py
```

## Engineering Concepts Demonstrated

- CAD-style enclosure parameter generation
- Mass and structural safety estimation
- Stochastic demand safety stock
- 3D pallet density approximation
- Warehouse slotting score
- Forklift travel reduction logic

## Real-World Extension

Replace the enclosure generator with a CAD API adapter for SOLIDWORKS, Fusion 360, FreeCAD, or Onshape. Replace the slotting logic with live WMS and ERP data.
