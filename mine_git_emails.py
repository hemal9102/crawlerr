import urllib.request
import json
import re

repos = [
    ("SigNoz", "SigNoz/signoz"),
    ("Atlan", "atlanhq/cartography"),
    ("DevRev", "devrev/typescript-sdk"),
    ("Glance", "glance/flutter_core"),
    ("Acceldata", "acceldata/open-source-data-platform")
]

print("=== Mining Git Commit Authors & Maintainer Emails ===")

for comp, repo in repos:
    url = f"https://api.github.com/repos/{repo}/commits?per_page=25"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            authors = set()
            for c in data:
                author = c.get("commit", {}).get("author", {})
                name = author.get("name", "")
                email = author.get("email", "")
                if email and not email.endswith("noreply.github.com"):
                    authors.add((name, email))
            print(f"[+] {comp} ({repo}): Found {len(authors)} public author emails")
            for n, e in list(authors)[:5]:
                print(f"    - {n} <{e}>")
    except Exception as e:
        # Repository might be private or name differs
        pass
