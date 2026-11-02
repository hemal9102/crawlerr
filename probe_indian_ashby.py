import urllib.request
import json

companies = [
    # Top Indian scaleups / high-growth tech
    ("Sprinto", "sprinto"),
    ("Kula", "kula"),
    ("Sarvam AI", "sarvamai"),
    ("Darwinbox", "darwinbox"),
    ("Atlan", "atlan"),
    ("SquadStack", "squadstack"),
    ("Jupiter", "jupiter"),
    ("Fi Money", "fi"),
    ("Apna", "apna"),
    ("Kite", "zerodha"),
    ("Yellow.ai", "yellowai"),
    ("Unacademy", "unacademy"),
    ("CoinSwitch", "coinswitch"),
    ("Kudo", "kudo")
]

SYSTEMS_KEYWORDS = [
    "systems", "infrastructure", "distributed", "kernel", "network", 
    "engine", "runtime", "storage", "database", "rust", "c++", "go", "golang",
    "core", "platform", "backend", "performance", "sre", "data engineering",
    "observability", "scale", "telemetry", "streaming", "pipeline"
]

print("=== Probing Ashby for Indian Tech Scaleups ===")
found = []
for name, slug in companies:
    url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            roles = []
            for j in data.get("jobs", []):
                t = j.get("title", "")
                if any(k in t.lower() for k in SYSTEMS_KEYWORDS):
                    roles.append({"title": t, "location": j.get("locationName", "Remote / India"), "url": j.get("jobUrl", "")})
            if roles:
                print(f"[+] {name}: Found {len(roles)} roles")
                found.append({"company": name, "roles": roles})
    except Exception:
        pass

out_path = r"D:\projects\emaillinggggggg\crawler\indian_scaleups_ashby.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(found, f, indent=2)

print(f"Done. Found {len(found)} companies.")
