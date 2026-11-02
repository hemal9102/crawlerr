import json

path = r"D:\projects\emaillinggggggg\crawler\elite_systems_cohort.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("=" * 90)
print("ELITE SYSTEMS & TAKE-HOME INFRASTRUCTURE COHORT")
print("=" * 90)

for item in data:
    comp = item["company"]
    roles = item["roles"]
    print(f"\n>>> {comp} ({len(roles)} relevant systems roles)")
    for r in roles[:3]:
        print(f"  * {r['title']} [{r['location']}]")
        print(f"    {r['url']}")
