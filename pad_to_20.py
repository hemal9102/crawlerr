import os
import sys
import json
import urllib.request

ADDITIONAL_TARGETS = [
    {"name": "Supabase", "ats": "greenhouse", "slug": "supabase", "domain": "supabase.com"},
    {"name": "HashiCorp", "ats": "greenhouse", "slug": "hashicorp", "domain": "hashicorp.com"},
    {"name": "Astronomer", "ats": "greenhouse", "slug": "astronomer", "domain": "astronomer.io"},
    {"name": "Upstash", "ats": "ashby", "slug": "upstash", "domain": "upstash.com"},
    {"name": "Datadog", "ats": "greenhouse", "slug": "datadog", "domain": "datadoghq.com"}
]

SYSTEMS_KEYWORDS = [
    "systems", "infrastructure", "distributed", "kernel", "network", 
    "engine", "runtime", "storage", "database", "rust", "c++", "go",
    "core", "platform", "backend", "performance", "sre"
]

with open(r"D:\projects\HK\crawler\crawled_20_diverse_jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

for target in ADDITIONAL_TARGETS:
    if len(jobs) >= 20:
        break
    comp = target["name"]
    ats = target["ats"]
    slug = target["slug"]
    domain = target["domain"]
    
    count = 0
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
                            "company": comp,
                            "domain": domain,
                            "title": title,
                            "location": j.get("locationName", "Remote"),
                            "url": j.get("jobUrl", "")
                        })
                        count += 1
                        if count >= 2 or len(jobs) >= 20:
                            break
        elif ats == "greenhouse":
            url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for j in data.get("jobs", []):
                    title = j.get("title", "")
                    if any(k in title.lower() for k in SYSTEMS_KEYWORDS):
                        jobs.append({
                            "company": comp,
                            "domain": domain,
                            "title": title,
                            "location": j.get("location", {}).get("name", "Remote"),
                            "url": j.get("absolute_url", "")
                        })
                        count += 1
                        if count >= 2 or len(jobs) >= 20:
                            break
    except Exception:
        pass

out_file = r"D:\projects\HK\crawler\crawled_20_diverse_jobs.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(jobs[:20], f, indent=2)

print(f"Final count: {len(jobs[:20])} jobs saved to {out_file}")
