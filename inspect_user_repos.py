import urllib.request
import json

req = urllib.request.Request('https://api.github.com/users/hemal9102/repos', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        repos = json.loads(resp.read().decode('utf-8'))
        for r in repos:
            print(f"{r['name']}:")
            print(f"  stars: {r['stargazers_count']}")
            print(f"  desc: {r.get('description')}")
            print(f"  lang: {r.get('language')}")
            print(f"  url: {r['html_url']}")
except Exception as e:
    print('Error:', e)
