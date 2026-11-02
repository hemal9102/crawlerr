import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*"
}

SYSTEMS_KEYWORDS = [
    "systems", "infrastructure", "infra", "distributed", "kernel", "network", 
    "engine", "runtime", "storage", "database", "rust", "c++", "go", "golang",
    "core", "platform", "backend", "performance", "sre", "data engineering",
    "observability", "scale", "telemetry", "streaming", "pipeline", "devops",
    "cloud", "architect", "data platform"
]

# 1. Test Greenhouse boards for Indian unicorns & devtools
greenhouse_slugs = [
    ("Swiggy", "swiggy"),
    ("Razorpay", "razorpay"),
    ("Urban Company", "urbancompany"),
    ("Hasura", "hasura"),
    ("Postman", "postman"),
    ("CleverTap", "clevertap"),
    ("Chargebee", "chargebee"),
    ("BrowserStack", "browserstack"),
    ("Khatabook", "khatabook"),
    ("Groww", "groww"),
    ("Ola", "ola"),
    ("Krutrim", "olakrutrim"),
    ("Infracloud", "infracloud"),
    ("Delhivery", "delhivery"),
    ("Pine Labs", "pinelabs"),
    ("Cars24", "cars24"),
    ("Zetwerk", "zetwerk"),
    ("ShareChat", "sharechat"),
    ("Licious", "licious"),
    ("PharmEasy", "pharmeasy"),
    ("Lenskart", "lenskart"),
    ("Spinny", "spinny"),
    ("Acko", "acko"),
    ("Digit Insurance", "godigit"),
    ("Moglix", "moglix")
]

# 2. Test Lever boards
lever_slugs = [
    ("CRED", "cred"),
    ("Acceldata", "acceldata"),
    ("Juspay", "juspay"),
    ("Setu", "setu"),
    ("Cashfree", "cashfree"),
    ("HyperVerge", "hyperverge"),
    ("Dunzo", "dunzo"),
    ("Kite", "zerodha"),
    ("CoinDCX", "coindcx"),
    ("Klub", "klubworks"),
    ("Jar", "jar"),
    ("OneCode", "onecode")
]

# 3. Test Ashby boards
ashby_slugs = [
    ("SigNoz", "signoz"),
    ("Atlan", "atlan"),
    ("ToolJet", "tooljet"),
    ("Sarvam AI", "sarvamai"),
    ("Sprinto", "sprinto"),
    ("Kula", "kula"),
    ("Darwinbox", "darwinbox"),
    ("SquadStack", "squadstack"),
    ("Jupiter", "jupiter"),
    ("Fi Money", "fi"),
    ("Apna", "apna"),
    ("Yellow.ai", "yellowai"),
    ("Unacademy", "unacademy"),
    ("CoinSwitch", "coinswitch")
]

all_harvested = []
print("=== Starting Massive Crawl of Indian Tech Companies (Greenhouse, Lever, Ashby) ===")

# Crawl Greenhouse
for name, slug in greenhouse_slugs:
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=4, context=ctx) as resp:
            data = json.loads(resp.read().decode())
            jobs = data.get("jobs", [])
            for j in jobs:
                title = j.get("title", "")
                loc = j.get("location", {}).get("name", "India")
                if any(k in title.lower() for k in SYSTEMS_KEYWORDS):
                    all_harvested.append({
                        "company": name,
                        "board": "greenhouse",
                        "title": title,
                        "location": loc,
                        "url": j.get("absolute_url", "")
                    })
    except Exception:
        pass

# Crawl Lever
for name, slug in lever_slugs:
    url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=4, context=ctx) as resp:
            data = json.loads(resp.read().decode())
            for j in data:
                title = j.get("text", "")
                loc = j.get("categories", {}).get("location", "India")
                if any(k in title.lower() for k in SYSTEMS_KEYWORDS):
                    all_harvested.append({
                        "company": name,
                        "board": "lever",
                        "title": title,
                        "location": loc,
                        "url": j.get("hostedUrl", "")
                    })
    except Exception:
        pass

# Crawl Ashby
for name, slug in ashby_slugs:
    url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=4, context=ctx) as resp:
            data = json.loads(resp.read().decode())
            for j in data.get("jobs", []):
                title = j.get("title", "")
                loc = j.get("locationName", "India / Remote")
                if any(k in title.lower() for k in SYSTEMS_KEYWORDS):
                    all_harvested.append({
                        "company": name,
                        "board": "ashby",
                        "title": title,
                        "location": loc,
                        "url": j.get("jobUrl", "")
                    })
    except Exception:
        pass

# Deduplicate
seen = set()
unique_results = []
for j in all_harvested:
    key = (j["company"], j["title"], j["location"])
    if key not in seen:
        seen.add(key)
        unique_results.append(j)

out_file = r"D:\projects\emaillinggggggg\crawler\massive_indian_jobs_harvest.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(unique_results, f, indent=2)

print(f"\n[MASSIVE CRAWL COMPLETE] Extracted {len(unique_results)} active Indian systems/infra engineering roles.")
by_comp = {}
for j in unique_results:
    c = j["company"]
    by_comp[c] = by_comp.get(c, 0) + 1

for c, count in sorted(by_comp.items(), key=lambda x: x[1], reverse=True):
    print(f"  {c:<20}: {count} roles")
