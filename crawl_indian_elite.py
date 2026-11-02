import os
import sys
import json
import urllib.request
import urllib.parse

# Elite Indian Infrastructure, DevTools, Systems Engineering & High-Scale FinTech
INDIAN_HIGH_TECH_COMPANIES = [
    # DevTools & Systems Platforms
    {"name": "Appsmith", "ats": "greenhouse", "slug": "appsmith", "domain": "appsmith.com"},
    {"name": "ToolJet", "ats": "ashby", "slug": "tooljet", "domain": "tooljet.com"},
    {"name": "SigNoz", "ats": "ashby", "slug": "signoz", "domain": "signoz.io"},
    {"name": "Kite / Zerodha", "ats": "direct", "slug": "zerodha", "domain": "zerodha.com"},
    {"name": "Groww", "ats": "greenhouse", "slug": "groww", "domain": "groww.in"},
    {"name": "Khatabook", "ats": "greenhouse", "slug": "khatabook", "domain": "khatabook.com"},
    {"name": "CRED", "ats": "greenhouse", "slug": "cred", "domain": "cred.club"},
    {"name": "Sarvam AI", "ats": "ashby", "slug": "sarvamai", "domain": "sarvam.ai"},
    {"name": "Krutrim / Ola", "ats": "greenhouse", "slug": "krutrim", "domain": "olakrutrim.com"},
    {"name": "Kula", "ats": "ashby", "slug": "kula", "domain": "kula.ai"},
    {"name": "Sprinto", "ats": "ashby", "slug": "sprinto", "domain": "sprinto.com"},
    {"name": "Chargebee", "ats": "greenhouse", "slug": "chargebee", "domain": "chargebee.com"},
    {"name": "CleverTap", "ats": "greenhouse", "slug": "clevertap", "domain": "clevertap.com"}
]

SYSTEMS_KEYWORDS = [
    "systems", "infrastructure", "distributed", "kernel", "network", 
    "engine", "runtime", "storage", "database", "rust", "c++", "go",
    "core", "platform", "backend", "performance", "sre", "data engineering"
]

harvested = []
print("=== Crawling Elite Indian High-Tech Systems & Infrastructure Companies ===")

for comp in INDIAN_HIGH_TECH_COMPANIES:
    name = comp["name"]
    ats = comp["ats"]
    slug = comp["slug"]
    domain = comp["domain"]
    
    roles = []
    try:
        if ats == "ashby":
            url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for j in data.get("jobs", []):
                    title = j.get("title", "")
                    if any(k in title.lower() for k in SYSTEMS_KEYWORDS):
                        roles.append({
                            "title": title,
                            "location": j.get("locationName", "India / Remote"),
                            "url": j.get("jobUrl", "")
                        })
        elif ats == "greenhouse":
            url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for j in data.get("jobs", []):
                    title = j.get("title", "")
                    if any(k in title.lower() for k in SYSTEMS_KEYWORDS):
                        roles.append({
                            "title": title,
                            "location": j.get("location", {}).get("name", "India / Remote"),
                            "url": j.get("absolute_url", "")
                        })
        if roles:
            print(f"[+] {name} ({ats}): Found {len(roles)} systems roles")
            harvested.append({"company": name, "domain": domain, "roles": roles})
    except Exception:
        pass

out_path = r"D:\projects\emaillinggggggg\crawler\indian_elite_crawl_results.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(harvested, f, indent=2)

print(f"\nCrawled {len(harvested)} active Indian companies. Results saved to {out_path}")
