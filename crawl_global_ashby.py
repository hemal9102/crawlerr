import urllib.request
import json

SYSTEMS_KEYWORDS = [
    "systems", "infrastructure", "distributed", "kernel", "network", 
    "engine", "runtime", "storage", "database", "rust", "c++", "go", "golang",
    "core", "platform", "backend", "performance", "sre", "data engineering",
    "observability", "scale", "telemetry", "streaming", "pipeline"
]

boards = [
    ("PostHog", "https://api.ashbyhq.com/posting-api/job-board/posthog"),
    ("Resend", "https://api.ashbyhq.com/posting-api/job-board/resend"),
    ("QuickNode", "https://api.ashbyhq.com/posting-api/job-board/quicknode"),
    ("Tavily", "https://api.ashbyhq.com/posting-api/job-board/tavily"),
    ("LangChain", "https://api.ashbyhq.com/posting-api/job-board/langchain"),
    ("Dagger", "https://api.ashbyhq.com/posting-api/job-board/dagger"),
    ("Neon", "https://api.ashbyhq.com/posting-api/job-board/neon"),
    ("LlamaIndex", "https://api.ashbyhq.com/posting-api/job-board/llamaindex"),
    ("Chroma", "https://api.ashbyhq.com/posting-api/job-board/chroma"),
    ("Together AI", "https://api.ashbyhq.com/posting-api/job-board/togetherai"),
    ("Anyscale", "https://api.ashbyhq.com/posting-api/job-board/anyscale"),
    ("Modal", "https://api.ashbyhq.com/posting-api/job-board/modal"),
    ("Baseten", "https://api.ashbyhq.com/posting-api/job-board/baseten")
]

found = []
print("=== Crawling Global Tier-1 Systems & Infra (Ashby) ===")
for name, url in boards:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            roles = []
            for j in data.get("jobs", []):
                t = j.get("title", "")
                if any(k in t.lower() for k in SYSTEMS_KEYWORDS):
                    roles.append({"title": t, "location": j.get("locationName", "Remote"), "url": j.get("jobUrl", "")})
            if roles:
                print(f"[+] {name}: {len(roles)} systems/infra roles")
                found.append({"company": name, "roles": roles})
    except Exception:
        pass

out_path = r"D:\projects\emaillinggggggg\crawler\global_ashby_systems.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(found, f, indent=2)

print(f"Done. Saved to {out_path}")
