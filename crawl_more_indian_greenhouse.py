import urllib.request
import json
import re

SYSTEMS_KEYWORDS = [
    "systems", "infrastructure", "distributed", "kernel", "network", 
    "engine", "runtime", "storage", "database", "rust", "c++", "go", "golang",
    "core", "platform", "backend", "performance", "sre", "data engineering",
    "observability", "scale", "telemetry", "streaming", "pipeline"
]

greenhouse_boards = [
    ("Swiggy", "swiggy"),
    ("Razorpay", "razorpay"),
    ("Urban Company", "urbancompany"),
    ("Delhivery", "delhivery"),
    ("Hasura", "hasura"),
    ("BrowserStack", "browserstack"),
    ("Postman", "postman"),
    ("Chargebee", "chargebee"),
    ("CleverTap", "clevertap"),
    ("Khatabook", "khatabook"),
    ("Infracloud", "infracloud"),
    ("Groww", "groww"),
    ("Ola", "ola"),
    ("Krutrim", "olakrutrim")
]

harvested = []
print("=== Crawling Indian Tech Scaleups on Greenhouse ===")
for name, slug in greenhouse_boards:
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            jobs = data.get("jobs", [])
            matched = []
            for j in jobs:
                title = j.get("title", "")
                loc = j.get("location", {}).get("name", "")
                if any(k in title.lower() for k in SYSTEMS_KEYWORDS):
                    matched.append({
                        "company": name,
                        "title": title,
                        "location": loc,
                        "url": j.get("absolute_url", "")
                    })
            if matched:
                print(f"[+] {name}: Found {len(matched)} systems roles")
                harvested.extend(matched)
    except Exception:
        pass

out_path = r"D:\projects\emaillinggggggg\crawler\indian_scaleups_greenhouse.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(harvested, f, indent=2)

print(f"Total new roles harvested: {len(harvested)}")
