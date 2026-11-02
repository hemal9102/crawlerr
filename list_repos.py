import urllib.request
import json

req = urllib.request.Request('https://api.github.com/users/hemal9102/repos', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    repos = json.loads(resp.read().decode('utf-8'))
    for r in repos:
        print(f"{r['name']}: {r['html_url']}")
