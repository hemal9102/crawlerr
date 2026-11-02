import os
import sys
import json
import urllib.request
import urllib.parse

# Elite Systems, Infra, High-Throughput Fintech, and AI Runtime companies in India and globally
EXPANDED_TARGETS = [
    # Top Tier Systems / Infra / AI / Fintech
    {"name": "Sarvam AI", "ats": "ashby", "slug": "sarvamai", "domain": "sarvam.ai"},
    {"name": "ToolJet", "ats": "ashby", "slug": "tooljet", "domain": "tooljet.com"},
    {"name": "SigNoz", "ats": "ashby", "slug": "signoz", "domain": "signoz.io"},
    {"name": "DevRev", "ats": "greenhouse", "slug": "devrev", "domain": "devrev.ai"},
    {"name": "Glance", "ats": "greenhouse", "slug": "glance", "domain": "glance.com"},
    {"name": "Chargebee", "ats": "greenhouse", "slug": "chargebee", "domain": "chargebee.com"},
    {"name": "CleverTap", "ats": "greenhouse", "slug": "clevertap", "domain": "clevertap.com"},
    {"name": "BrowserStack", "ats": "greenhouse", "slug": "browserstack", "domain": "browserstack.com"},
    {"name": "Hasura", "ats": "greenhouse", "slug": "hasura", "domain": "hasura.io"},
    {"name": "Postman", "ats": "greenhouse", "slug": "postman", "domain": "postman.com"},
    {"name": "InfraCloud", "ats": "greenhouse", "slug": "infracloud", "domain": "infracloud.io"},
    {"name": "Khatabook", "ats": "greenhouse", "slug": "khatabook", "domain": "khatabook.com"},
    {"name": "CRED", "ats": "greenhouse", "slug": "cred", "domain": "cred.club"},
    {"name": "Groww", "ats": "greenhouse", "slug": "groww", "domain": "groww.in"},
    {"name": "Kula", "ats": "ashby", "slug": "kula", "domain": "kula.ai"},
    {"name": "Sprinto", "ats": "ashby", "slug": "sprinto", "domain": "sprinto.com"},
    {"name": "ChaosNative", "ats": "direct", "slug": "chaosnative", "domain": "chaosnative.com"},
    {"name": "Acceldata", "ats": "greenhouse", "slug": "acceldata", "domain": "acceldata.io"},
    {"name": "HyperVerge", "ats": "direct", "slug": "hyperverge", "domain": "hyperverge.co"},
    {"name": "Appsmith", "ats": "greenhouse", "slug": "appsmith", "domain": "appsmith.com"}
]

SYSTEMS_KEYWORDS = [
    "systems", "infrastructure", "distributed", "kernel", "network", 
    "engine", "runtime", "storage", "database", "rust", "c++", "go", "golang",
    "core", "platform", "backend", "performance", "sre", "data engineering",
    "observability", "scale", "telemetry", "streaming", "pipeline"
]

all_harvested = []
print("=== Starting Deep Crawl Across Elite Systems & High-Scale Infra Scaleups ===")

for target in EXPANDED_TARGETS:
    comp = target["name"]
    ats = target["ats"]
    slug = target["slug"]
    domain = target["domain"]
    
    roles = []
    try:
        if ats == "ashby":
            url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for j in data.get("jobs", []):
                    title = j.get("title", "")
                    if any(k in title.lower() for k in SYSTEMS_KEYWORDS):
                        roles.append({
                            "title": title,
                            "location": j.get("locationName", "Remote / Hybrid"),
                            "url": j.get("jobUrl", "")
                        })
        elif ats == "greenhouse":
            url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for j in data.get("jobs", []):
                    title = j.get("title", "")
                    if any(k in title.lower() for k in SYSTEMS_KEYWORDS):
                        roles.append({
                            "title": title,
                            "location": j.get("location", {}).get("name", "Remote / Hybrid"),
                            "url": j.get("absolute_url", "")
                        })
        
        if roles:
            print(f"[+] {comp} ({ats}): Found {len(roles)} relevant systems/infra roles")
            all_harvested.append({
                "company": comp,
                "domain": domain,
                "count": len(roles),
                "roles": roles
            })
    except Exception as e:
        # Silently skip if board not public or 404
        pass

out_path = r"D:\projects\emaillinggggggg\crawler\deep_crawl_systems_pool.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(all_harvested, f, indent=2)

print(f"\n[DONE] Successfully harvested {len(all_harvested)} companies. Results written to {out_path}")
