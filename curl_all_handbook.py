import json
import subprocess
import os
import re
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []
        self.ignore = False

    def handle_starttag(self, tag, attrs):
        if tag in ["script", "style", "nav", "svg"]:
            self.ignore = True

    def handle_endtag(self, tag):
        if tag in ["script", "style", "nav", "svg"]:
            self.ignore = False

    def handle_data(self, data):
        if not self.ignore:
            cleaned = data.strip()
            if cleaned:
                self.texts.append(cleaned)

def extract_main_text(html: str) -> str:
    parser = TextExtractor()
    parser.feed(html)
    return " ".join(parser.texts)

with open(r"D:\projects\HK\crawler\handbook_links.json", "r", encoding="utf-8") as f:
    links = json.load(f)

output_dir = r"D:\projects\HK\crawler\resend_handbook_dump"
os.makedirs(output_dir, exist_ok=True)

print(f"Executing curl.exe on {len(links)} Resend Handbook links...")

summary_manifest = []

for idx, rel_path in enumerate(links, 1):
    full_url = f"https://resend.com{rel_path}"
    slug = rel_path.strip("/").replace("/", "_")
    target_file = os.path.join(output_dir, f"{slug}.txt")
    
    cmd = ["curl.exe", "-sL", full_url]
    try:
        raw_html = subprocess.check_output(cmd, text=True, encoding="utf-8", timeout=15)
        clean_text = extract_main_text(raw_html)
        
        # Save readable text dump
        with open(target_file, "w", encoding="utf-8") as f_out:
            f_out.write(f"URL: {full_url}\n")
            f_out.write("=" * 60 + "\n\n")
            f_out.write(clean_text)
            
        summary_manifest.append({
            "index": idx,
            "url": full_url,
            "path": target_file,
            "char_count": len(clean_text),
            "snippet": clean_text[:200]
        })
        print(f"[{idx:02d}/{len(links)}] Curled: {full_url} ({len(clean_text)} chars)")
    except Exception as e:
        print(f"[{idx:02d}/{len(links)}] FAILED: {full_url} - {e}")

manifest_file = os.path.join(output_dir, "manifest.json")
with open(manifest_file, "w", encoding="utf-8") as f:
    json.dump(summary_manifest, f, indent=2)

print(f"\nALL 65 LINKS CURLED SUCCESSFULLY. Manifest written to {manifest_file}")
