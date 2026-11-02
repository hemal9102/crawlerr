import json
import urllib.request

EXTRA_SYSTEMS_TARGETS = [
    # Turso (ChiselStrike / libsql distributed database in Rust/C)
    {"name": "Turso", "ats": "greenhouse", "slug": "chiselstrike", "domain": "turso.tech"},
    # Convex (Reactive backend and distributed database in Rust)
    {"name": "Convex", "ats": "greenhouse", "slug": "convex", "domain": "convex.dev"},
    # Axiom (High-performance serverless log engine in Go/Rust)
    {"name": "Axiom", "ats": "greenhouse", "slug": "axiom", "domain": "axiom.co"},
    # DragonflyDB (In-memory cache engine in C++)
    {"name": "DragonflyDB", "ats": "ashby", "slug": "dragonflydb", "domain": "dragonflydb.io"},
    # Prisma (Database ORM & Query Engine in Rust)
    {"name": "Prisma", "ats": "greenhouse", "slug": "prisma", "domain": "prisma.io"},
    # Upstash (Serverless Redis & Kafka engine)
    {"name": "Upstash", "ats": "greenhouse", "slug": "upstash", "domain": "upstash.com"}
]

SYSTEMS_KEYWORDS = [
    "systems", "infrastructure", "distributed", "kernel", "network", 
    "engine", "runtime", "storage", "database", "rust", "c++", "go",
    "core", "platform", "backend", "performance"
]

with open(r"D:\projects\emaillinggggggg\crawler\elite_systems_cohort.json", "r", encoding="utf-8") as f:
    existing = json.load(f)

for target in EXTRA_SYSTEMS_TARGETS:
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
            existing.append({"company": comp, "domain": domain, "roles": jobs})
    except Exception:
        pass

out_path = r"D:\projects\emaillinggggggg\crawler\elite_systems_cohort.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(existing, f, indent=2)

print("Total elite systems companies in cohort:", len(existing))
