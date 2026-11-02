import re
import subprocess
import json
from html.parser import HTMLParser

# First fetch the handbook HTML to find all internal /handbook/ links
raw_html = subprocess.check_output(["curl.exe", "-sL", "https://resend.com/handbook"], text=True, encoding="utf-8")

links = sorted(list(set(re.findall(r'href="(/handbook/[^"]+)"', raw_html))))
print(f"Discovered {len(links)} handbook sub-links:")
for l in links:
    print(" -", l)

with open(r"D:\projects\HK\crawler\handbook_links.json", "w", encoding="utf-8") as f:
    json.dump(links, f, indent=2)
