import json

path = r"D:\projects\emaillinggggggg\crawler\indian_infra_jobs.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    comp = item["company"]
    roles = item["roles"]
    print(f"\n=== {comp} ({len(roles)} systems roles) ===")
    for r in roles[:5]:
        print(f"  * {r['title']} | {r['location']}")
        print(f"    {r['url']}")
