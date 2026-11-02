import json
import urllib.request

ADDITIONAL_INDIAN_ORGS = [
    # CleverTap (Customer Data Platform / High-Throughput Stream Processing)
    {"name": "CleverTap", "ats": "greenhouse", "slug": "clevertap", "domain": "clevertap.com"},
    # Razorpay (Core Payments Gateway / Low-Latency Ledger)
    {"name": "Razorpay", "ats": "greenhouse", "slug": "razorpay", "domain": "razorpay.com"},
    # Zepto (Ultra-Low Latency Routing & Logistics)
    {"name": "Zepto", "ats": "greenhouse", "slug": "zepto", "domain": "zepto.com"},
    # InMobi (High-Throughput Ad Server & Bidding Engines)
    {"name": "InMobi", "ats": "greenhouse", "slug": "inmobi", "domain": "inmobi.com"},
    # HyperVerge (AI Vision & Edge Inference Runtimes)
    {"name": "HyperVerge", "ats": "greenhouse", "slug": "hyperverge", "domain": "hyperverge.co"}
]

SYSTEMS_KEYWORDS = [
    "systems", "infrastructure", "distributed", "kernel", "network", 
    "engine", "runtime", "storage", "database", "rust", "c++", "go",
    "core", "platform", "backend", "performance", "sre"
]

with open(r"D:\projects\emaillinggggggg\crawler\indian_infra_jobs.json", "r", encoding="utf-8") as f:
    harvested = json.load(f)

for target in ADDITIONAL_INDIAN_ORGS:
    comp = target["name"]
    slug = target["slug"]
    domain = target["domain"]
    
    jobs = []
    try:
        url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for j in data.get("jobs", []):
                title = j.get("title", "")
                if any(k in title.lower() for k in SYSTEMS_KEYWORDS):
                    jobs.append({
                        "title": title,
                        "location": j.get("location", {}).get("name", "India"),
                        "url": j.get("absolute_url", "")
                    })
        if jobs:
            print(f"[+] {comp}: Found {len(jobs)} systems roles")
            harvested.append({"company": comp, "domain": domain, "roles": jobs})
    except Exception:
        pass

out_path = r"D:\projects\emaillinggggggg\crawler\indian_infra_jobs.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(harvested, f, indent=2)

print("Updated Indian infra pool count:", len(harvested))
