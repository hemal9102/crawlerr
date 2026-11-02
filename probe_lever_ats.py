import urllib.request
import json

lever_slugs = [
    ("Postman", "postman"),
    ("Hasura", "hasura"),
    ("BrowserStack", "browserstack"),
    ("CleverTap", "clevertap"),
    ("Chargebee", "chargebee"),
    ("Appsmith", "appsmith"),
    ("ToolJet", "tooljet"),
    ("Sarvam AI", "sarvamai"),
    ("Krutrim", "krutrim"),
    ("Groww", "groww"),
    ("CRED", "cred"),
    ("Khatabook", "khatabook"),
    ("Infracloud", "infracloud"),
    ("Acceldata", "acceldata"),
    ("Jio", "jio"),
    ("Delhivery", "delhivery"),
    ("Urban Company", "urbancompany"),
    ("Swiggy", "swiggy"),
    ("Zomato", "zomato"),
    ("Razorpay", "razorpay"),
    ("Pine Labs", "pinelabs"),
    ("Juspay", "juspay"),
    ("Setu", "setu"),
    ("Cashfree", "cashfree"),
    ("HyperVerge", "hyperverge")
]

SYSTEMS_KEYWORDS = [
    "systems", "infrastructure", "distributed", "kernel", "network", 
    "engine", "runtime", "storage", "database", "rust", "c++", "go", "golang",
    "core", "platform", "backend", "performance", "sre", "data engineering",
    "observability", "scale", "telemetry", "streaming", "pipeline"
]

print("=== Probing Lever ATS Job Boards ===")
found = []
for name, slug in lever_slugs:
    url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            roles = []
            for j in data:
                title = j.get("text", "")
                if any(k in title.lower() for k in SYSTEMS_KEYWORDS):
                    loc = j.get("categories", {}).get("location", "Remote")
                    roles.append({"title": title, "location": loc, "url": j.get("hostedUrl", "")})
            if roles:
                print(f"[+] Lever: {name} has {len(roles)} systems/infra roles!")
                found.append({"company": name, "roles": roles})
    except Exception:
        pass

out_path = r"D:\projects\emaillinggggggg\crawler\lever_systems_jobs.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(found, f, indent=2)

print(f"Done. Found {len(found)} companies on Lever.")
