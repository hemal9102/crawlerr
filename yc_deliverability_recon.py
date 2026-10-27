#!/usr/bin/env python3
"""
YC & SaaS Deliverability Vulnerability Crawler
Connects hemal9102/crawler with forensic_dns_recon to crawl companies
whose business model depends on email and identify RFC 7208 / DMARC vulnerabilities.
"""

import sys
import os
import json
import re
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from collections import deque

# Import our forensic recon engine
sys.path.append(r"D:\projects\HK\tensix\scripts")
from forensic_dns_recon import audit_domain

class DomainLinkExtractor(HTMLParser):
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.domains = set()

    def handle_starttag(self, tag: str, attrs: list):
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v:
                    parsed = urllib.parse.urlparse(v)
                    netloc = parsed.netloc.lower()
                    if netloc:
                        # strip subdomains like www.
                        parts = netloc.split(":")[0].split(".")
                        if len(parts) >= 2:
                            root_domain = ".".join(parts[-2:])
                            if root_domain not in ("ycombinator.com", "google.com", "github.com", "twitter.com", "linkedin.com"):
                                self.domains.add(root_domain)

def run_targeted_audit(domains: list):
    print(f"[*] Starting Forensic Audit across {len(domains)} target domains...\n")
    bleeding_leads = []

    for domain in domains:
        res = audit_domain(domain)
        if res and res["is_bleeding"]:
            print(f"[!] VULNERABLE TARGET DETECTED: {domain}")
            print(f"    - SPF Lookups: {res['spf_lookups']}/10 (RFC 7208)")
            print(f"    - DMARC Policy: {res['dmarc_policy']}")
            print(f"    - Flags: {', '.join(res['reasons'])}")
            print()
            bleeding_leads.append(res)
        elif res:
            print(f"[+] Clean: {domain} (SPF Lookups: {res['spf_lookups']}/10, DMARC: {res['dmarc_policy']})")

    # Save actionable leads to disk
    output_path = r"D:\projects\HK\tensix\data\bleeding_deliverability_leads.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(bleeding_leads, f, indent=2)

    print(f"\n[+] Total Vulnerable Targets Saved: {len(bleeding_leads)} -> {output_path}")

if __name__ == "__main__":
    # Test batch including YC/Email-heavy startups & Indian SaaS
    sample_targets = [
        "keka.com",
        "clevertap.com",
        "brevo.com",
        "mailjet.com",
        "apollo.io",
        "lemlist.com",
        "instantly.ai",
        "smartlead.ai",
        "woodpecker.co",
        "sendinblue.com",
        "moengage.com",
        "webengage.com"
    ]
    run_targeted_audit(sample_targets)
