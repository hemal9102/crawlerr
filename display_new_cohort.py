import json

path = r"D:\projects\emaillinggggggg\crawler\new_crawled_infra_cohort.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    comp = item["company"]
    roles = item["roles"]
    print(f"\n=== {comp} ({len(roles)} systems roles) ===")
    for r in roles[:4]:
        print(f"  * {r['title']} | {r['location']}")
        print(f"    {r['url']}")
