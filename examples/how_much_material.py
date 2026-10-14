"""How much material do I need?

Usage:
    python examples/how_much_material.py --length 50 --width 12 --depth 3 --material crushed-stone-57
    python examples/how_much_material.py --list

Length and width in feet, depth in inches. Prints cubic yards and US tons,
plus the order amount with the default waste allowance for that material.
"""
import argparse
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

# default allowance by category (see data/waste-allowances.csv)
ALLOWANCE = {
    "gravel": 0.05, "river-rock": 0.05, "landscape-rock": 0.05,
    "crushed-stone": 0.10, "base": 0.20, "sand": 0.05,
    "soil": 0.10, "fill": 0.15, "rip-rap": 0.10,
}


def load():
    with open(DATA / "aggregate-bulk-densities.csv", newline="") as f:
        return {row["id"]: row for row in csv.DictReader(f)}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--length", type=float, help="length in feet")
    p.add_argument("--width", type=float, help="width in feet")
    p.add_argument("--depth", type=float, help="depth in inches")
    p.add_argument("--material", default="gravel-general", help="material id from the CSV")
    p.add_argument("--list", action="store_true", help="list material ids and exit")
    a = p.parse_args()
    materials = load()
    if a.list:
        for mid, row in materials.items():
            print(f"{mid:26} {row['lb_per_ft3']:>4} lb/ft3  {row['material']}")
        return
    if None in (a.length, a.width, a.depth):
        p.error("--length, --width and --depth are required")
    row = materials[a.material]
    ft3 = a.length * a.width * a.depth / 12
    yd3 = ft3 / 27
    tons = ft3 * float(row["lb_per_ft3"]) / 2000
    extra = ALLOWANCE.get(row["category"], 0.10)
    print(f"{row['material']}: {a.length:g} x {a.width:g} ft at {a.depth:g} in deep")
    print(f"  volume  {yd3:.2f} yd3 ({ft3:.1f} ft3)")
    print(f"  weight  {tons:.2f} US tons")
    print(f"  order   {tons * (1 + extra):.2f} tons with {extra:.0%} allowance")


if __name__ == "__main__":
    main()
