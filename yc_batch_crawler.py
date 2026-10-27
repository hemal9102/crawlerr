#!/usr/bin/env python3
"""
TENSIX High-Yield YC Batch Crawler & Multi-Variable MailOps Recon
Crawls Hacker News YC launch batches across recent cohorts (W24, S24, W23),
evaluates the 8 MailOps variables, and compiles high-bleed targets.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import time

sys.path.append(r"D:\projects\HK\crawler")
from mailops_scorer import score_and_package_domain

def crawl_yc_cohorts(queries=["Launch YC", "YC W24", "YC S24", "YC W23"], max_pages=3):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) TENSIX-Crawler/2.0"}
    discovered_domains = {}

    print(f"[*] Initiating Multi-Cohort YC Crawl across queries: {queries}")
    
    for q in queries:
        for page in range(max_pages):
            url = f"https://hn.algolia.com/api/v1/search?query={urllib.parse.quote(q)}&tags=story&page={page}&hitsPerPage=50"
            req = urllib.request.Request(url, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    hits = data.get("hits", [])
                    for h in hits:
                        story_url = h.get("url") or ""
                        title = h.get("title") or ""
                        author = h.get("author") or ""
                        if story_url:
                            parsed = urllib.parse.urlparse(story_url)
                            netloc = parsed.netloc.lower()
                            if netloc:
                                parts = netloc.split(":")[0].split(".")
                                if len(parts) >= 2:
                                    root_domain = ".".join(parts[-2:])
                                    ignored = (
                                        "github.com", "medium.com", "youtube.com", "substack.com", 
                                        "ycombinator.com", "techcrunch.com", "twitter.com", "x.com", 
                                        "linkedin.com", "notion.site", "google.com"
                                    )
                                    if root_domain not in ignored and root_domain not in discovered_domains:
                                        discovered_domains[root_domain] = {
                                            "domain": root_domain,
                                            "title": title,
                                            "hn_author": author,
                                            "source_query": q
                                        }
            except Exception as e:
                print(f"[-] Error querying Algolia for '{q}' page {page}: {e}")
            time.sleep(0.5)

    print(f"[+] Total unique candidate startup domains extracted: {len(discovered_domains)}")
    return list(discovered_domains.values())

def audit_and_compile():
    candidates = crawl_yc_cohorts()
    high_priority_targets = []
    monitored_targets = []

    print(f"\n[*] Commencing Multi-Variable DNS & Sprawl Forensics on {len(candidates)} domains...\n")
    
    for idx, c in enumerate(candidates):
        domain = c["domain"]
        try:
            profile = score_and_package_domain(domain, biz_type="B2B SaaS / YC Startup")
            profile["title"] = c["title"]
            profile["hn_author"] = c["hn_author"]

            if profile["is_priority_lead"]:
                print(f"[!] [BLEEDING TARGET] [{idx+1}/{len(candidates)}] {domain} (Score: {profile['bleed_score']}/100)")
                print(f"    - Lookups: {profile['spf_lookups']}/10 | DMARC: {profile['dmarc_policy']}")
                print(f"    - Vendors ({profile['vendor_count']}): {', '.join(profile['detected_vendors'])}")
                print(f"    - Tripwire: ${profile['tripwire_service']['price_usd']} | Retainer: ${profile['retainer_service']['price_usd_monthly']}/mo")
                print()
                high_priority_targets.append(profile)
            else:
                monitored_targets.append(profile)
        except Exception as e:
            continue

    # Persist the actionable high-priority pipeline
    out_file = r"D:\projects\HK\tensix\data\yc_high_priority_mailops_leads.json"
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(high_priority_targets, f, indent=2)

    print("=" * 70)
    print(f"[+] CRAWL & FORENSICS COMPLETE!")
    print(f"[+] Total Scanned: {len(candidates)}")
    print(f"[!] HIGH-PRIORITY ACTIONABLE TARGETS: {len(high_priority_targets)}")
    print(f"[+] High-priority targets saved to: {out_file}")
    print("=" * 70)

if __name__ == "__main__":
    audit_and_compile()
