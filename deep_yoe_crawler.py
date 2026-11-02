import os
import sys
import json
import urllib.request
import urllib.parse
from job_filter import is_hard_blocked_job, parse_years_of_experience

COMPANIES = [
    {"name": "Resend", "ats": "ashby", "slug": "resend", "domain": "resend.com"},
    {"name": "Modal", "ats": "ashby", "slug": "modal", "domain": "modal.com"},
    {"name": "Railway", "ats": "ashby", "slug": "railway", "domain": "railway.app"},
    {"name": "LiveKit", "ats": "ashby", "slug": "livekit", "domain": "livekit.io"},
    {"name": "Warp", "ats": "ashby", "slug": "warp", "domain": "warp.dev"},
    {"name": "Supabase", "ats": "greenhouse", "slug": "supabase", "domain": "supabase.com"},
    {"name": "Vercel", "ats": "greenhouse", "slug": "vercel", "domain": "vercel.com"},
    {"name": "CockroachLabs", "ats": "greenhouse", "slug": "cockroachlabs", "domain": "cockroachlabs.com"},
    {"name": "Timescale", "ats": "greenhouse", "slug": "timescale", "domain": "timescale.com"},
    {"name": "ScyllaDB", "ats": "greenhouse", "slug": "scylladb", "domain": "scylladb.com"}
]

SYSTEMS_KEYWORDS = [
    "systems", "infrastructure", "distributed", "kernel", "network", 
    "engine", "runtime", "storage", "database", "rust", "c++", "go",
    "backend", "platform"
]

validated_jobs = []

print("=== Running Deep Body YoE & Title Filter Crawl ===")

for comp in COMPANIES:
    if len(validated_jobs) >= 20:
        break
    ats = comp["ats"]
    slug = comp["slug"]
    name = comp["name"]
    domain = comp["domain"]
    
    try:
        if ats == "ashby":
            url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for j in data.get("jobs", []):
                    title = j.get("title", "")
                    desc = j.get("descriptionHtml", "")
                    
                    if not any(k in title.lower() for k in SYSTEMS_KEYWORDS):
                        continue
                        
                    blocked, reason = is_hard_blocked_job(title, desc, max_allowed_yoe=4)
                    if blocked:
                        # Log filtered job
                        # print(f"  [BLOCKED] {name} - {title}: {reason}")
                        continue
                        
                    yoe = parse_years_of_experience(desc)
                    validated_jobs.append({
                        "company": name,
                        "domain": domain,
                        "title": title,
                        "required_yoe": yoe if yoe is not None else "Unspecified / Open",
                        "location": j.get("locationName", "Remote"),
                        "url": j.get("jobUrl", "")
                    })
                    if len(validated_jobs) >= 20:
                        break
                        
        elif ats == "greenhouse":
            # For Greenhouse, fetch individual job description content
            url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for j in data.get("jobs", []):
                    title = j.get("title", "")
                    if not any(k in title.lower() for k in SYSTEMS_KEYWORDS):
                        continue
                        
                    # Fetch detailed body for greenhouse job
                    job_id = j.get("id")
                    detail_url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs/{job_id}"
                    req_detail = urllib.request.Request(detail_url, headers={"User-Agent": "Mozilla/5.0"})
                    try:
                        with urllib.request.urlopen(req_detail, timeout=5) as detail_resp:
                            detail_data = json.loads(detail_resp.read().decode("utf-8"))
                            desc = detail_data.get("content", "")
                    except Exception:
                        desc = ""
                        
                    blocked, reason = is_hard_blocked_job(title, desc, max_allowed_yoe=4)
                    if blocked:
                        continue
                        
                    yoe = parse_years_of_experience(desc)
                    validated_jobs.append({
                        "company": name,
                        "domain": domain,
                        "title": title,
                        "required_yoe": yoe if yoe is not None else "Unspecified / Open",
                        "location": j.get("location", {}).get("name", "Remote"),
                        "url": j.get("absolute_url", "")
                    })
                    if len(validated_jobs) >= 20:
                        break
    except Exception as e:
        pass

out_path = r"D:\projects\HK\crawler\clean_validated_jobs.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(validated_jobs, f, indent=2)

print(f"DONE: Harvested {len(validated_jobs)} clean jobs with STRICT YoE <= 4 or Unspecified.")
