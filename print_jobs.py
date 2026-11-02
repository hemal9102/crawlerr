import json

with open(r"D:\projects\HK\crawler\clean_validated_jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

for idx, j in enumerate(jobs, 1):
    comp = j.get('company')
    title = j.get('title')
    loc = j.get('location')
    yoe = j.get('required_yoe')
    url = j.get('url')
    print(f"{idx:02d}. [{comp}] {title}")
    print(f"    Required YoE: {yoe} | Loc: {loc}")
    print(f"    {url}")
