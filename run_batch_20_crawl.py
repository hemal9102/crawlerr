import os
import sys
import json
import urllib.request
from typing import List, Dict

# Crawl diversity across top systems & infra tech companies
TARGETS = [
    {"name": "Railway", "ats": "ashby", "slug": "railway", "domain": "railway.app"},
    {"name": "LiveKit", "ats": "ashby", "slug": "livekit", "domain": "livekit.io"},
    {"name": "Warp", "ats": "ashby", "slug": "warp", "domain": "warp.dev"},
    {"name": "CockroachLabs", "ats": "greenhouse", "slug": "cockroachlabs", "domain": "cockroachlabs.com"},
    {"name": "Timescale", "ats": "greenhouse", "slug": "timescale", "domain": "timescale.com"},
    {"name": "Redpanda", "ats": "greenhouse", "slug": "redpanda", "domain": "redpanda.com"},
    {"name": "ScyllaDB", "ats": "greenhouse", "slug": "scylladb", "domain": "scylladb.com"},
    {"name": "Vercel", "ats": "greenhouse", "slug": "vercel", "domain": "vercel.com"},
    {"name": "ClickHouse", "ats": "greenhouse", "slug": "clickhouse", "domain": "clickhouse.com"},
    {"name": "SingleStore", "ats": "greenhouse", "slug": "singlestore", "domain": "singlestore.com"}
]

SYSTEMS_KEYWORDS = [
    "systems", "infrastructure", "distributed", "kernel", "network", 
    "engine", "runtime", "storage", "database", "rust", "c++", "go",
    "core", "platform", "backend", "performance", "sre"
]

all_jobs = []

# First load top 2 from Resend and Modal
try:
    with open(r"D:\projects\HK\crawler\crawled_20_jobs.json", "r", encoding="utf-8") as f:
        existing = json.load(f)
    for j in existing:
        if j["company"] == "Resend" and len([x for x in all_jobs if x["company"] == "Resend"]) < 2:
            all_jobs.append(j)
        elif j["company"] == "Modal" and len([x for x in all_jobs if x["company"] == "Modal"]) < 2:
            all_jobs.append(j)
except Exception:
    pass

for target in TARGETS:
    if len(all_jobs) >= 20:
        break
    comp = target["name"]
    ats = target["ats"]
    slug = target["slug"]
    domain = target["domain"]
    
    count_for_comp = 0
    try:
        if ats == "ashby":
            url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for j in data.get("jobs", []):
                    title = j.get("title", "")
                    if any(k in title.lower() for k in SYSTEMS_KEYWORDS):
                        all_jobs.append({
                            "company": comp,
                            "domain": domain,
                            "title": title,
                            "location": j.get("locationName", "Remote"),
                            "url": j.get("jobUrl", "")
                        })
                        count_for_comp += 1
                        if count_for_comp >= 2 or len(all_jobs) >= 20:
                            break
        elif ats == "greenhouse":
            url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for j in data.get("jobs", []):
                    title = j.get("title", "")
                    if any(k in title.lower() for k in SYSTEMS_KEYWORDS):
                        all_jobs.append({
                            "company": comp,
                            "domain": domain,
                            "title": title,
                            "location": j.get("location", {}).get("name", "Remote"),
                            "url": j.get("absolute_url", "")
                        })
                        count_for_comp += 1
                        if count_for_comp >= 2 or len(all_jobs) >= 20:
                            break
    except Exception:
        pass

out_file = r"D:\projects\HK\crawler\crawled_20_diverse_jobs.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(all_jobs[:20], f, indent=2)

print(f"Captured {len(all_jobs[:20])} diverse jobs across top infra companies.")
