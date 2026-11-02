import urllib.request
import json
import re

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def check_greenhouse_slug(slug):
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            return len(data.get("jobs", []))
    except Exception:
        return None

def check_lever_slug(slug):
    url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            return len(data)
    except Exception:
        return None

def check_ashby_slug(slug):
    url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            return len(data.get("jobs", []))
    except Exception:
        return None

candidates = [
    "postman", "postmaninc", "postmanlabs",
    "hasura", "hasurainc",
    "browserstack",
    "razorpay", "razorpaysoftware",
    "swiggy", "bundl",
    "clevertap", "wizrocket",
    "chargebee",
    "khatabook",
    "groww",
    "zerodha", "kite",
    "juspay", "juspaytech",
    "infracloud", "infracloudio",
    "delhivery",
    "urbancompany", "urbanclap",
    "meesho",
    "dream11", "dreamsports",
    "unacademy",
    "ola", "olacabs", "olakrutrim", "krutrim",
    "lenskart",
    "shadowfax",
    "spinny",
    "cars24",
    "zepto",
    "blinkit", "grofers"
]

print("=== Probing ATS Slugs for Indian Scaleups ===")
for c in candidates:
    gh = check_greenhouse_slug(c)
    if gh is not None:
        print(f"[FOUND Greenhouse] {c}: {gh} total jobs")
    lv = check_lever_slug(c)
    if lv is not None:
        print(f"[FOUND Lever] {c}: {lv} total jobs")
    ash = check_ashby_slug(c)
    if ash is not None:
        print(f"[FOUND Ashby] {c}: {ash} total jobs")

print("Slug probe complete.")
