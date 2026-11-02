import os
import sys
import json
import urllib.request
import urllib.parse
from typing import List, Dict, Any

# Top-tier infrastructure startups & scaleups:
# Focused on databases, wire protocols, agent runtimes, real-time audio/video, and search
EXPANDED_TARGETS = [
    # Top Ashby targets
    {"name": "Cartesia", "ats": "ashby", "slug": "cartesia", "domain": "cartesia.ai"},
    {"name": "Deepgram", "ats": "ashby", "slug": "deepgram", "domain": "deepgram.com"},
    {"name": "Tavily", "ats": "ashby", "slug": "tavily", "domain": "tavily.com"},
    {"name": "Modal", "ats": "ashby", "slug": "modal", "domain": "modal.com"},
    {"name": "LiveKit", "ats": "ashby", "slug": "livekit", "domain": "livekit.io"},
    {"name": "Warp", "ats": "ashby", "slug": "warp", "domain": "warp.dev"},
    {"name": "Resend", "ats": "ashby", "slug": "resend", "domain": "resend.com"},
    {"name": "Railway", "ats": "ashby", "slug": "railway", "domain": "railway.app"},
    {"name": "Inngest", "ats": "ashby", "slug": "inngest", "domain": "inngest.com"},
    {"name": "LlamaIndex", "ats": "ashby", "slug": "llamaindex", "domain": "llamaindex.ai"},
    
    # Next high-leverage infra targets
    {"name": "Dagger", "ats": "ashby", "slug": "dagger", "domain": "dagger.io"},
    {"name": "Braintrust", "ats": "ashby", "slug": "braintrust", "domain": "braintrustdata.com"},
    {"name": "TogetherAI", "ats": "greenhouse", "slug": "togetherai", "domain": "together.ai"},
    {"name": "Weights & Biases", "ats": "greenhouse", "slug": "wandb", "domain": "wandb.ai"},
    {"name": "Cohere", "ats": "greenhouse", "slug": "cohere", "domain": "cohere.com"},
    {"name": "Cursor / Anysphere", "ats": "ashby", "slug": "anysphere", "domain": "cursor.com"}
]

SYSTEMS_KEYWORDS = [
    "systems", "infrastructure", "distributed", "kernel", "network", 
    "engine", "runtime", "storage", "database", "rust", "c++", "go",
    "core", "platform", "backend", "performance", "sre"
]

discovered = []
print("=== Running Deep Ingress Crawl across Tier-1 AI & Systems Infra ===")

for target in EXPANDED_TARGETS:
    comp = target["name"]
    ats = target["ats"]
    slug = target["slug"]
    domain = target["domain"]
    
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
                        roles.append({
                            "title": title,
                            "location": j.get("location", {}).get("name", "Remote"),
                            "url": j.get("absolute_url", "")
                        })
        if roles:
            print(f"[+] {comp}: Found {len(roles)} systems engineering positions")
            discovered.append({"company": comp, "domain": domain, "roles": roles})
    except Exception:
        pass

out_path = r"D:\projects\emaillinggggggg\crawler\deep_systems_crawl_pool.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(discovered, f, indent=2)

print(f"\nDiscovered {len(discovered)} active systems organizations. Saved to {out_path}")
