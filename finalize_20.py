import json

with open(r"D:\projects\HK\crawler\crawled_20_jobs.json", "r", encoding="utf-8") as f:
    orig = json.load(f)

with open(r"D:\projects\HK\crawler\crawled_20_diverse_jobs.json", "r", encoding="utf-8") as f:
    div = json.load(f)

urls = set(x["url"] for x in div)
for item in orig:
    if len(div) >= 20:
        break
    if item["url"] not in urls:
        div.append(item)
        urls.add(item["url"])

with open(r"D:\projects\HK\crawler\crawled_20_diverse_jobs.json", "w", encoding="utf-8") as f:
    json.dump(div[:20], f, indent=2)

print("Exact 20 count confirmed:", len(div[:20]))
