import json

with open(r"D:\projects\emaillinggggggg\crawler\consolidated_systems_crawl.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

# Filter for India locations / remote
india_keywords = ["india", "bengaluru", "bangalore", "delhi", "ncr", "remote", "mumbai", "pune", "hyderabad", "gurugram", "gurgaon"]

india_jobs = []
for j in jobs:
    loc = j.get("location", "").lower()
    comp = j.get("company", "")
    title = j.get("title", "")
    # Acceldata, DevRev, Glance, SigNoz, CRED
    # Exclude Kitchener (Canada), US-only, UK-only
    if any(k in loc for k in ["kitchener", "united states", "london", "argentina", "california", "us, sf"]):
        continue
    
    # Include if location mentions Indian tech hubs or Remote, or is an Indian engineering role
    india_jobs.append(j)

print(f"Total Indian Systems/Infra Roles: {len(india_jobs)}\n")

by_comp = {}
for j in india_jobs:
    c = j["company"]
    by_comp.setdefault(c, []).append(j)

for comp, rlist in by_comp.items():
    print(f"=== {comp} ({len(rlist)} roles) ===")
    for r in rlist:
        print(f"  • {r['title']} | Location: {r['location']}")
        print(f"    URL: {r['url']}")
    print()

out_file = r"D:\projects\emaillinggggggg\crawler\india_specific_systems_jobs.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(india_jobs, f, indent=2)

print(f"Saved to {out_file}")
