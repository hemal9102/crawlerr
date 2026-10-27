#!/usr/bin/env python3
"""
YC Company Scraper & Batch Deliverability Auditor
Crawls Y Combinator directory / Hacker News launches via public APIs / Hacker News Algolia API,
filters for SaaS/B2B companies, and audits their SPF/DMARC records for RFC violations.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from html.parser import HTMLParser

# Link our forensic engine
sys.path.append(r"D:\projects\HK\tensix\scripts")
from forensic_dns_recon import audit_domain

def fetch_hn_yc_companies(query: str = "launch yc", max_hits: int = 40):
    """
    Query the official, free Algolia Hacker News API for recent YC launches.
    Extracts authentic company domains without scraping hurdles.
    """
    url = f"https://hn.algolia.com/api/v1/search?query={urllib.parse.quote(query)}&tags=story&hitsPerPage={max_hits}"
    print(f"[*] Querying YC Launch registry via Algolia API: {url}...")
    
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) YCRecon/1.0"}
    )
    
    extracted_companies = []
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            hits = data.get("hits", [])
            print(f"[+] Retrieved {len(hits)} launch posts from YC ecosystem.")
            
            for h in hits:
                story_url = h.get("url") or ""
                title = h.get("title") or ""
                if story_url:
                    parsed = urllib.parse.urlparse(story_url)
                    netloc = parsed.netloc.lower()
                    if netloc:
                        parts = netloc.split(":")[0].split(".")
                        if len(parts) >= 2:
                            root_domain = ".".join(parts[-2:])
                            if root_domain not in ("github.com", "medium.com", "youtube.com", "substack.com", "ycombinator.com", "techcrunch.com"):
                                extracted_companies.append({
                                    "domain": root_domain,
                                    "title": title,
                                    "url": story_url,
                                    "author": h.get("author")
                                })
    except Exception as e:
        print(f"[-] Error querying YC registry: {e}")

    # Deduplicate by domain
    unique = {}
    for c in extracted_companies:
        if c["domain"] not in unique:
            unique[c["domain"]] = c
            
    return list(unique.values())

def run_yc_crawler_pipeline():
    print("=" * 70)
    print("YC PIPELINE: Real-time Discovery + RFC DNS Forensics")
    print("=" * 70)
    
    companies = fetch_hn_yc_companies("launch yc", max_hits=60)
    print(f"[+] Extracted {len(companies)} unique startup domains.")
    
    bleeding_targets = []
    
    print("\n[*] Auditing domains against RFC 7208 (SPF 10-lookup limit) & DMARC alignment...\n")
    for comp in companies:
        d = comp["domain"]
        audit_res = audit_domain(d)
        if audit_res and audit_res["is_bleeding"]:
            print(f"[!] VULNERABLE TARGET DETECTED: {d}")
            print(f"    - Title: {comp['title']}")
            print(f"    - SPF Lookups: {audit_res['spf_lookups']}/10")
            print(f"    - DMARC Policy: {audit_res['dmarc_policy']}")
            print(f"    - Reasons: {', '.join(audit_res['reasons'])}")
            print()
            comp.update(audit_res)
            bleeding_targets.append(comp)
        elif audit_res:
            print(f"[+] Clean: {d} (SPF: {audit_res['spf_lookups']}/10, DMARC: {audit_res['dmarc_policy']})")

    out_file = r"D:\projects\HK\crawler\yc_vulnerable_targets.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(bleeding_targets, f, indent=2)

    print(f"\n[+] PIPELINE COMPLETE: Found {len(bleeding_targets)} bleeding YC/SaaS targets.")
    print(f"[+] Results saved to: {out_file}")

if __name__ == "__main__":
    run_yc_crawler_pipeline()
