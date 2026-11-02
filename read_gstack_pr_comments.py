import urllib.request
import json

url = 'https://api.github.com/repos/garrytan/gstack/issues/5/comments'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        comments = json.loads(resp.read().decode('utf-8'))
        for c in comments:
            user = c.get('user', {}).get('login')
            body = c.get('body')
            print(f"{user}: {body}")
except Exception as e:
    print("Error:", e)
