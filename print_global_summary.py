import json

with open(r"D:\projects\emaillinggggggg\crawler\global_ashby_systems.json", "r", encoding="utf-8") as f:
    comps = json.load(f)

total = sum(len(c["roles"]) for c in comps)
print(f"Total Tier-1 Systems/Infra Roles Crawled: {total}\n")
for c in comps:
    print(f"{c['company']:<15}: {len(c['roles'])} roles")
    for r in c["roles"][:3]:
        print(f"   -> {r['title']} ({r['location']})")
