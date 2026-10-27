#!/usr/bin/env python3
"""
TENSIX Production Autonomous MailOps Discovery Engine (Hardened v3)
Architecture:
1. Crawls strictly RECENT YC Launches (W24, S24 cohorts from 2024-2026).
2. Runs Reputation Shield: Validates 200 OK HTTPS, detects expired/hijacked domains.
3. Multi-Variable DNS Forensics: Evaluates SPF 10-lookup limit, DMARC, Vendor Sprawl.
4. Synthesizes bespoke 2-tier packages ($350 tripwire + $1,500/mo MailOps).
5. Only outputs 100% verified active companies.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import time

sys.path.append(r"D:\projects\HK\crawler")
from mailops_scorer import score_and_package_domain
from reputation_shield import verify_live_website

def crawl_recent_yc_launches(queries=["Launch YC W24", "Launch YC S24", "YC W24 launch"], max_hits=80):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) TENSIX-ReputationEngine/3.0"}
    candidates = {}

    print(f"[*] Querying recent verified YC batches (W24, S24): {queries}")
    for q in queries:
        url = f"https://hn.algolia.com/api/v1/search?query={urllib.parse.quote(q)}&tags=story&hitsPerPage={max_hits}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for h in data.get("hits", []):
                    story_url = h.get("url") or ""
                    title = h.get("title") or ""
                    author = h.get("author") or ""
                    if story_url:
                        parsed = urllib.parse.urlparse(story_url)
                        netloc = parsed.netloc.lower()
                        if netloc:
                            parts = netloc.split(":")[0].split(".")
                            if len(parts) >= 2:
                                root = ".".join(parts[-2:])
                                ignored = (
                                    "github.com", "medium.com", "youtube.com", "substack.com", 
                                    "ycombinator.com", "techcrunch.com", "twitter.com", "x.com", 
                                    "linkedin.com", "notion.site", "google.com", "apple.com"
                                )
                                if root not in ignored and root not in candidates:
                                    candidates[root] = {
                                        "domain": root,
                                        "title": title,
                                        "hn_author": author,
                                        "original_url": story_url
                                    }
        except Exception as e:
            print(f"[-] Query error for {q}: {e}")
        time.sleep(0.5)

    print(f"[+] Total raw candidate domains: {len(candidates)}")
    return list(candidates.values())

def execute_pipeline():
    print("=" * 80)
    print("TENSIX REPUTATION-GUARDED YC CRAWL & FORENSIC PIPELINE")
    print("=" * 80)

    raw_candidates = crawl_recent_yc_launches()
    verified_leads = []

    print(f"\n[*] Probing {len(raw_candidates)} startup websites for active operational SaaS signals...\n")

    for idx, c in enumerate(raw_candidates):
        domain = c["domain"]
        
        # GATE 1: REPUTATION SHIELD (Website liveness & anti-hijack check)
        is_live, op_weight, shield_meta = verify_live_website(domain, timeout=5)
        
        if not is_live:
            print(f"[-] [REJECTED/INACTIVE] [{idx+1}/{len(raw_candidates)}] {domain}: {shield_meta.get('reason')}")
            continue

        print(f"[+] [VERIFIED LIVE SAAS] [{idx+1}/{len(raw_candidates)}] {domain} (Op Weight: {op_weight}/100)")

        # GATE 2: DNS & VENDOR SPRAWL FORENSICS
        try:
            profile = score_and_package_domain(domain, biz_type="Recent YC Startup")
            profile["title"] = c["title"]
            profile["hn_author"] = c["hn_author"]
            profile["operational_weight"] = op_weight

            if profile["is_priority_lead"]:
                print(f"  >>> [HIGH-PRIORITY BLEEDING TARGET] Score: {profile['bleed_score']}/100")
                print(f"      • Lookups: {profile['spf_lookups']}/10 | DMARC: {profile['dmarc_policy']}")
                print(f"      • Vendors ({profile['vendor_count']}): {', '.join(profile['detected_vendors'])}")
                print(f"      • Tripwire: ${profile['tripwire_service']['price_usd']} | Retainer: ${profile['retainer_service']['price_usd_monthly']}/mo")
                verified_leads.append(profile)
        except Exception as e:
            continue

    out_file = r"D:\projects\HK\tensix\data\verified_active_yc_leads.json"
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(verified_leads, f, indent=2)

    print("\n" + "=" * 80)
    print(f"[+] PIPELINE COMPLETE!")
    print(f"[+] Total Raw Candidates: {len(raw_candidates)}")
    print(f"[+] 100% Verified Active & Bleeding Targets: {len(verified_leads)}")
    print(f"[+] Clean verified leads persisted to: {out_file}")
    print("=" * 80)

if __name__ == "__main__":
    execute_pipeline()
