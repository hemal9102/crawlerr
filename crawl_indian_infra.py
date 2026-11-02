import os
import sys
import json
import urllib.request
import urllib.parse

# Elite Indian Infrastructure, Systems Engineering, DevTools & Database Scaleups
INDIAN_INFRA_TARGETS = [
    # Postman (API Platform / Runtime)
    {"name": "Postman", "ats": "greenhouse", "slug": "postman", "domain": "postman.com"},
    # BrowserStack (Distributed Cloud Browsers / Real Device Emulation)
    {"name": "BrowserStack", "ats": "greenhouse", "slug": "browserstack", "domain": "browserstack.com"},
    # Hasura (High-Performance GraphQL Engine in Haskell & Rust)
    {"name": "Hasura", "ats": "greenhouse", "slug": "hasura", "domain": "hasura.io"},
    # Dgraph Labs (Distributed Graph Database in Go)
    {"name": "Dgraph", "ats": "greenhouse", "slug": "dgraph", "domain": "dgraph.io"},
    # SigNoz (Open-Source Observability & Telemetry in Go/ClickHouse)
    {"name": "SigNoz", "ats": "ashby", "slug": "signoz", "domain": "signoz.io"},
    # DevRev (Developer CRM & Platform Infrastructure)
    {"name": "DevRev", "ats": "greenhouse", "slug": "devrev", "domain": "devrev.ai"},
    # Infracloud (Cloud Native & Kubernetes Engineering)
    {"name": "InfraCloud", "ats": "greenhouse", "slug": "infracloud", "domain": "infracloud.io"},
    # Acceldata (Data Observability & High-Throughput Ingestion)
    {"name": "Acceldata", "ats": "greenhouse", "slug": "acceldata", "domain": "acceldata.io"},
    # Jio / Glance (High-Throughput Mobile Ingress & Platform)
    {"name": "Glance", "ats": "greenhouse", "slug": "glance", "domain": "glance.com"}
]

SYSTEMS_KEYWORDS = [
    "systems", "infrastructure", "distributed", "kernel", "network", 
    "engine", "runtime", "storage", "database", "rust", "c++", "go",
    "core", "platform", "backend", "performance", "sre"
]

harvested = []
print("=== Crawling Elite Indian Systems & Infrastructure Scaleups ===")

for target in INDIAN_INFRA_TARGETS:
    comp = target["name"]
    ats = target["ats"]
    slug = target["slug"]
    domain = target["domain"]
    
    jobs_found = []
    try:
        if ats == "ashby":
            url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for j in data.get("jobs", []):
                    title = j.get("title", "")
                    if any(k in title.lower() for k in SYSTEMS_KEYWORDS):
                        jobs_found.append({
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
                        jobs_found.append({
                            "title": title,
                            "location": j.get("location", {}).get("name", "India / Remote"),
                            "url": j.get("absolute_url", "")
                        })
        
        if jobs_found:
            print(f"[+] {comp}: Found {len(jobs_found)} systems/infrastructure roles")
            harvested.append({
                "company": comp,
                "domain": domain,
                "roles": jobs_found
            })
    except Exception as e:
        # print(f"[-] {comp} failed: {e}")
        pass

out_path = r"D:\projects\emaillinggggggg\crawler\indian_infra_jobs.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(harvested, f, indent=2)

print(f"\nCrawled {len(harvested)} companies. Results saved to {out_path}")
