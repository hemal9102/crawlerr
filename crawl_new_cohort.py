import os
import sys
import json
import urllib.request
import urllib.parse
from typing import List, Dict, Any

# Target companies specializing in Distributed Systems, GPU/AI Infra, Vector/TimeSeries DBs, Ingress Proxies
TARGETS = [
    # Top Ashby targets
    {"name": "Eppo", "ats": "ashby", "slug": "geteppo", "domain": "geteppo.com"},
    {"name": "Koyeb", "ats": "ashby", "slug": "koyeb", "domain": "koyeb.com"},
    {"name": "Speakeasy", "ats": "ashby", "slug": "speakeasy", "domain": "speakeasyapi.dev"},
    {"name": "Baseten", "ats": "ashby", "slug": "baseten", "domain": "baseten.co"},
    {"name": "OctoAI", "ats": "ashby", "slug": "octoai", "domain": "octoai.cloud"},
    {"name": "Chroma", "ats": "ashby", "slug": "chroma", "domain": "trychroma.com"},
    {"name": "Langfuse", "ats": "ashby", "slug": "langfuse", "domain": "langfuse.com"},
    {"name": "Unstructured", "ats": "ashby", "slug": "unstructured", "domain": "unstructured.io"},
    
    # Top Greenhouse targets
    {"name": "PlanetScale", "ats": "greenhouse", "slug": "planetscale", "domain": "planetscale.com"},
    {"name": "Materialize", "ats": "greenhouse", "slug": "materialize", "domain": "materialize.com"},
    {"name": "Neon", "ats": "greenhouse", "slug": "neondatabase", "domain": "neon.tech"},
    {"name": "Citus / Crunchy Data", "ats": "greenhouse", "slug": "crunchydata", "domain": "crunchydata.com"},
    {"name": "Yugabyte", "ats": "greenhouse", "slug": "yugabyte", "domain": "yugabyte.com"},
    {"name": "Confluent", "ats": "greenhouse", "slug": "confluent", "domain": "confluent.io"},
    {"name": "Tailscale", "ats": "greenhouse", "slug": "tailscale", "domain": "tailscale.com"}
]

SYSTEMS_KEYWORDS = [
    "systems", "infrastructure", "distributed", "kernel", "network", 
    "engine", "runtime", "storage", "database", "rust", "c++", "go",
    "core", "platform", "backend", "performance", "sre"
]

harvested = []
print("=== Crawling Next High-Value Systems & AI Infra Cohort ===")

for target in TARGETS:
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
                            "location": j.get("locationName", "Remote"),
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
                            "location": j.get("location", {}).get("name", "Remote"),
                            "url": j.get("absolute_url", "")
                        })
        
        if jobs_found:
            print(f"[+] {comp}: Found {len(jobs_found)} systems roles")
            harvested.append({
                "company": comp,
                "domain": domain,
                "roles": jobs_found
            })
    except Exception as e:
        # print(f"[-] {comp} failed: {e}")
        pass

out_path = r"D:\projects\emaillinggggggg\crawler\new_crawled_infra_cohort.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(harvested, f, indent=2)

print(f"\nCrawled {len(harvested)} active companies. Results saved to {out_path}")
