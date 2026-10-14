# Aggregate Bulk Densities

Typical bulk densities for 51 landscaping and construction aggregates: gravel, crushed stone, river rock, landscape rock, rip rap, sand, topsoil and fill dirt. Each one is given in imperial and metric units, with how many square feet one ton covers at common depths.

The figures are the ones used by the free calculators at [stonegravelcalculator.com](https://stonegravelcalculator.com/). The full method, unit conversions and limits are documented on the [methodology and material densities page](https://stonegravelcalculator.com/methodology/).

## Files

| File | What it holds |
|---|---|
| `data/aggregate-bulk-densities.csv` | One row per material, all units |
| `data/aggregate-bulk-densities.json` | The same data as JSON, with source and unit notes |
| `data/waste-allowances.csv` | Default extra to order for each material type, and why |
| `examples/how_much_material.py` | Small script: area and depth in, cubic yards and tons out |

## Columns

| Column | Meaning |
|---|---|
| `id` | Stable slug for the material |
| `material` | Material name (`in` = inches) |
| `category` | gravel, crushed-stone, base, river-rock, landscape-rock, rip-rap, sand, soil, fill |
| `lb_per_ft3` | Pounds per cubic foot (the base value; every other column is derived from it) |
| `lb_per_yd3` | Pounds per cubic yard (`lb_per_ft3 × 27`) |
| `us_tons_per_yd3` | US short tons per cubic yard (`lb_per_yd3 ÷ 2,000`) |
| `kg_per_m3` | Kilograms per cubic metre (`lb_per_ft3 × 16.0185`) |
| `tonnes_per_m3` | Metric tonnes per cubic metre |
| `sq_ft_per_us_ton_at_2in` … `_6in` | Area one US ton covers at 2, 3, 4 and 6 inches deep |

## Sample

| Material | lb/ft³ | tons/yd³ | kg/m³ | sq ft per ton at 2″ | at 4″ |
|---|---|---|---|---|---|
| Pea gravel (3/8 in) | 96 | 1.30 | 1,538 | 125 | 63 |
| Crushed stone #57 (3/4 in, clean) | 105 | 1.42 | 1,682 | 114 | 57 |
| Crusher run / #411 / ABC | 125 | 1.69 | 2,002 | 96 | 48 |
| River rock, 1-3 in | 100 | 1.35 | 1,602 | 120 | 60 |
| Lava rock | 50 | 0.68 | 801 | 240 | 120 |
| Concrete / sharp sand | 105 | 1.42 | 1,682 | 114 | 57 |
| Screened topsoil (moist) | 90 | 1.22 | 1,442 | 133 | 67 |

## The formula

```
volume (ft³)  = length (ft) × width (ft) × depth (in) ÷ 12
volume (yd³)  = volume (ft³) ÷ 27
weight (tons) = volume (ft³) × lb_per_ft3 ÷ 2,000
order         = weight × (1 + allowance)
```

Example: a 12 × 50 ft driveway topped with 3 in of #57 stone is 150 ft³, or 5.56 yd³. At 105 lb/ft³ that is 7.9 tons, or about 8.7 tons with a 10% allowance.

```bash
python examples/how_much_material.py --length 50 --width 12 --depth 3 --material crushed-stone-57
```

## Use it in code

Python:

```python
import csv
with open("data/aggregate-bulk-densities.csv") as f:
    density = {row["id"]: float(row["lb_per_ft3"]) for row in csv.DictReader(f)}
print(density["pea-gravel"])  # 96.0
```

JavaScript (Node 22+):

```js
import data from "./data/aggregate-bulk-densities.json" with { type: "json" };
const pea = data.materials.find(m => m.id === "pea-gravel");
console.log(pea.us_tons_per_yd3); // 1.3
```

## Limits

These are typical values for loose, dry-to-moist material as delivered. Real loads vary by quarry, rock type, grading and moisture: wet sand can be 20–30% heavier than dry sand, and compacted base takes up less volume than loose. For a large order, ask your supplier for the density of their product and use that instead.

## Calculators that use this data

- [Gravel calculator](https://stonegravelcalculator.com/) (tons, cubic yards and bags)
- [Crushed stone calculator](https://stonegravelcalculator.com/crushed-stone-calculator/)
- [Pea gravel calculator](https://stonegravelcalculator.com/pea-gravel-calculator/)
- [Sand calculator](https://stonegravelcalculator.com/sand-calculator/)
- [Topsoil calculator](https://stonegravelcalculator.com/topsoil-calculator/)
- [Stone and gravel weight calculator](https://stonegravelcalculator.com/stone-weight-calculator/)

## Licence and citation

Data released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). You can use it in commercial and non-commercial work. Please credit it as:

> Aggregate bulk densities, Stone & Gravel Calculator, https://stonegravelcalculator.com/methodology/

Found a value that is off for your region? Open an issue with the material, the value you see and where it comes from (supplier sheet, DOT spec, lab test).
