import urllib.request
import json

url = 'https://api.ashbyhq.com/posting-api/job-board/cursor'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))

print("=== Cursor / Anysphere Systems & Infrastructure Roles ===")
for j in data.get('jobs', []):
    t = j.get('title', '')
    if any(k in t.lower() for k in ['infrastructure', 'model routing', 'inference', 'storage', 'compute', 'client infra', 'core services']):
        print(f"  * {t}")
        print(f"    {j.get('jobUrl')}")
