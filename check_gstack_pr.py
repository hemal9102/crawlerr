import urllib.request
import json

url = 'https://api.github.com/repos/garrytan/gstack/pulls?state=all'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        prs = json.loads(resp.read().decode('utf-8'))
        for p in prs:
            user = p.get('user', {}).get('login')
            if user == 'morluto':
                print(f"PR #{p['number']}: {p['title']} ({p['state']})")
                print(f"Created: {p['created_at']}")
                print(f"Body: {p.get('body', '')[:300]}")
except Exception as ex:
    print('Error:', ex)
