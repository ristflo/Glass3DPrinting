"""Illustrative scenarios, USD assumptions; not supplier quotes or measured costs."""
from pathlib import Path
import csv
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'sources' / 'data' / 'commercial_economics.csv'

def cost(capital, years, fixed, attempts, yield_fraction, material, kwh, tariff, labour_hours, wage, quality, consumables):
    annual_fixed = capital / years + fixed
    variable = material + kwh * tariff + labour_hours * wage + quality + consumables
    return (annual_fixed / attempts + variable) / yield_fraction

base = dict(capital=100000, years=5, fixed=10000, attempts=1000, yield_fraction=.8,
            material=4, kwh=20, tariff=.15, labour_hours=1, wage=30, quality=10, consumables=5)
rows = []
for name, changes in [
    ('molten_baseline', {}), ('molten_low_utilization', {'attempts':250}),
    ('molten_high_utilization', {'attempts':2000}), ('molten_lower_yield', {'yield_fraction':.6}),
    ('molten_double_tariff', {'tariff':.30}),
    ('indirect_different_small_part', {'capital':60000, 'fixed':6000, 'attempts':2000,
       'yield_fraction':.9, 'material':5, 'kwh':2, 'labour_hours':.25, 'quality':3, 'consumables':2})]:
    args = base | changes
    rows.append(dict(scenario=name, evidence='analyst-selected illustrative assumptions',
                     **args, cost_per_accepted_part_usd=round(cost(**args), 4)))
with OUT.open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
for row in rows:
    print(row['scenario'], f"{row['cost_per_accepted_part_usd']:.2f}")
