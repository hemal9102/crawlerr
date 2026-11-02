import os
import sys
import json
import urllib.request
import urllib.parse
from typing import List, Dict, Any

# Target companies known specifically for:
# 1. System design whiteboard / paid work-trials (not leetcode)
# 2. Remote-first / High-compensation ($150k - $300k+ USD or Top 1% India)
# 3. Core infrastructure: Custom protocol engines, wire-level brokers, distributed DBs, WebRTC/audio streams, low-latency execution

TARGET_POOLS = [
    # Top Remote Infrastructure & Database Builders on Ashby
    {"name": "Turso", "ats": "ashby", "slug": "turso", "domain": "turso.tech"},
    {"name": "Convex", "ats": "ashby", "slug": "convex", "domain": "convex.dev"},
    {"name": "Tailscale", "ats": "ashby", "slug": "tailscale", "domain": "tailscale.com"},
    {"name": "Temporal", "ats": "ashby", "slug": "temporal", "domain": "temporal.io"},
    {"name": "ClickHouse", "ats": "ashby", "slug": "clickhouse", "domain": "clickhouse.com"},
    {"name": "Neon", "ats": "ashby", "slug": "neon", "domain": "neon.tech"},
    {"name": "PostHog", "ats": "ashby", "slug": "posthog", "domain": "posthog.com"},
    {"name": "Supabase", "ats": "ashby", "slug": "supabase", "domain": "supabase.com"},
    {"name": "Prisma", "ats": "ashby", "slug": "prisma", "domain": "prisma.io"},
    {"name": "Upstash", "ats": "ashby", "slug": "upstash", "domain": "upstash.com"},
    {"name": "Axiom", "ats": "ashby", "slug": "axiom", "domain": "axiom.co"},
    {"name": "Railway", "ats": "ashby", "slug": "railway", "domain": "railway.app"},
    
    # Greenhouse Elite Systems & High-Frequency Scaleups
    {"name": "CockroachLabs", "ats": "greenhouse", "slug": "cockroachlabs", "domain": "cockroachlabs.com"},
    {"name": "Timescale", "ats": "greenhouse", "slug": "timescale", "domain": "timescale.com"},
    {"name": "Redpanda", "ats": "greenhouse", "slug": "redpanda", "domain": "redpanda.com"},
    {"name": "ScyllaDB", "ats": "greenhouse", "slug": "scylladb", "domain": "scylladb.com"},
    {"name": "BrowserStack", "ats": "greenhouse", "slug": "browserstack", "domain": "browserstack.com"},
    {"name": "Postman", "ats": "greenhouse", "slug": "postman", "domain": "postman.com"},
    {"name": "Hasura", "ats": "greenhouse", "slug": "hasura", "domain": "hasura.io"},
    {"name": "SingleStore", "ats": "greenhouse", "slug": "singlestore", "domain": "singlestore.com"}
]

SYSTEMS_KEYWORDS = [
    "systems", "infrastructure", "distributed", "kernel", "network", 
    "engine", "runtime", "storage", "database", "rust", "c++", "go",
    "core", "platform", "backend", "performance", "protocols", "wire"
]

results = []
print("=== Crawling Elite Remote & High-Paying Systems Companies ===")

for target in TARGET_POOLS:
    comp = target["name"]
    ats = target["ats"]
    slug = target["slug"]
    domain = target["domain"]
    
    jobs = []
    try:
        if ats == "ashby":
            url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for j in data.get("jobs", []):
                    title = j.get("title", "")
                    if any(k in title.lower() for k in SYSTEMS_KEYWORDS):
                        jobs.append({
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
                        jobs.append({
                            "title": title,
                            "location": j.get("location", {}).get("name", "Remote"),
                            "url": j.get("absolute_url", "")
                        })
        if jobs:
            print(f"[+] {comp} ({ats}): Found {len(jobs)} systems roles")
            results.append({"company": comp, "domain": domain, "roles": jobs})
    except Exception as e:
        # print(f"[-] {comp} failed: {e}")
        pass

out_path = r"D:\projects\emaillinggggggg\crawler\elite_systems_cohort.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"\nCrawl complete. {len(results)} elite infrastructure companies discovered.")
