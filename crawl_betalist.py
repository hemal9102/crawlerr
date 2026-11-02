import urllib.request
import ssl
import json
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

def crawl_betalist_full():
    url = "https://betalist.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    print(f"[+] Fetching live feed from {url}...")
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # Each startup row has class 'startup-row'
    rows = soup.find_all(class_=lambda c: c and 'startup-row' in c)
    print(f"[+] Found {len(rows)} startup entries on BetaList.")
    
    startups = []
    seen = set()
    
    for r in rows:
        link = r.find('a', href=lambda h: h and h.startswith('/startups/'))
        if not link:
            continue
            
        href = link.get('href')
        slug = href.replace('/startups/', '').strip('/')
        
        if slug in seen:
            continue
        seen.add(slug)
        
        # Extract title and pitch text
        # Usually inside div text
        texts = [t.strip() for t in r.stripped_strings if t.strip()]
        
        name = slug.replace('-', ' ').title()
        pitch = ""
        
        if len(texts) >= 1:
            name = texts[0]
        if len(texts) >= 2:
            pitch = ' '.join(texts[1:])
            
        startups.append({
            "name": name,
            "slug": slug,
            "betalist_url": f"https://betalist.com{href}",
            "pitch": pitch
        })
        
    out_file = r'D:\projects\HK\crawler\betalist_startups.json'
    with open(out_file, 'w', encoding='utf-8') as fp:
        json.dump(startups, fp, indent=2, ensure_ascii=False)
        
    print(f"[+] Successfully extracted {len(startups)} startups!")
    print(f"[+] Output saved to: {out_file}\n")
    
    print(f"{'#':<3} | {'STARTUP NAME':<25} | {'PITCH / DESCRIPTION'}")
    print("-" * 90)
    for i, s in enumerate(startups, 1):
        print(f"{i:<3} | {s['name'][:24]:<25} | {s['pitch'][:55]}")

if __name__ == '__main__':
    crawl_betalist_full()
