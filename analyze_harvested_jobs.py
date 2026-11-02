import urllib.request
import json

yoe_keywords = [
    "years of experience", "yoe", "years' experience", "minimum 5 years",
    "minimum 6 years", "minimum 7 years", "minimum 8 years", "minimum 10 years"
]

files = [
    r"D:\projects\emaillinggggggg\crawler\lever_systems_jobs.json",
    r"D:\projects\emaillinggggggg\crawler\deep_crawl_systems_pool.json",
    r"D:\projects\emaillinggggggg\crawler\indian_infra_jobs.json"
]

all_jobs = []
for fpath in files:
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            for comp in data:
                cname = comp.get("company", "")
                for r in comp.get("roles", []):
                    all_jobs.append({
                        "company": cname,
                        "title": r.get("title", ""),
                        "location": r.get("location", ""),
                        "url": r.get("url", "")
                    })
    except Exception:
        pass

# Deduplicate
seen = set()
unique_jobs = []
for j in all_jobs:
    key = (j["company"], j["title"])
    if key not in seen:
        seen.add(key)
        unique_jobs.append(j)

print(f"Total unique systems/infra roles extracted: {len(unique_jobs)}")
for j in unique_jobs[:15]:
    print(f"- [{j['company']}] {j['title']} ({j['location']})")

out_file = r"D:\projects\emaillinggggggg\crawler\consolidated_systems_crawl.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(unique_jobs, f, indent=2)

print(f"\nSaved consolidated {len(unique_jobs)} roles to {out_file}")
