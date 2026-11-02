import urllib.request
import json

url = 'https://api.github.com/search/issues?q=author:morluto+type:pr'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("Total PRs by morluto:", data.get('total_count'))
        for item in data.get('items', [])[:8]:
            print(f"[{item['state']}] {item['html_url']}")
            print(f"  Title: {item['title']}")
except Exception as e:
    print("Error:", e)
