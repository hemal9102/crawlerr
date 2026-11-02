import json

with open(r"D:\projects\emaillinggggggg\crawler\massive_indian_jobs_harvest.json", "r", encoding="utf-8") as f:
    massive = json.load(f)

with open(r"D:\projects\emaillinggggggg\crawler\india_specific_systems_jobs.json", "r", encoding="utf-8") as f:
    india_jobs = json.load(f)

combined = []
seen = set()

for j in massive + india_jobs:
    title = j.get("title", "")
    comp = j.get("company", "")
    loc = j.get("location", "")
    url = j.get("url", "")
    key = (comp.lower(), title.lower())
    if key not in seen:
        seen.add(key)
        combined.append({
            "company": comp,
            "title": title,
            "location": loc,
            "url": url
        })

print(f"Total Unique Verified Indian Systems Roles: {len(combined)}\n")

by_company = {}
for j in combined:
    by_company.setdefault(j["company"], []).append(j)

for c, rlist in sorted(by_company.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"=== {c} ({len(rlist)} systems roles) ===")
    for r in rlist:
        print(f"  • {r['title']} | {r['location']}")
        print(f"    URL: {r['url']}")
    print()

out_dest = r"D:\projects\emaillinggggggg\crawler\all_indian_systems_engineering_roles.json"
with open(out_dest, "w", encoding="utf-8") as f:
    json.dump(combined, f, indent=2)

print(f"Saved complete inventory to {out_dest}")
