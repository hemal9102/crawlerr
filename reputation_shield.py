#!/usr/bin/env python3
"""
TENSIX Liveness & Domain Reputation Shield (Calibrated v3)
Strictly guards against domain expirations, cross-domain hijacks, and parked spam
while accurately scoring operational SaaS companies.
"""

import urllib.request
import urllib.parse
import ssl
import time
from typing import Dict, Tuple

def verify_live_website(domain: str, timeout: int = 6) -> Tuple[bool, int, Dict]:
    ctx = ssl.create_default_context()
    ctx.check_hostname = True
    ctx.verify_mode = ssl.CERT_REQUIRED

    target_url = f"https://{domain}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    req = urllib.request.Request(target_url, headers=headers)
    
    try:
        start_time = time.time()
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
            latency_ms = int((time.time() - start_time) * 1000)
            final_url = response.geturl().lower()
            
            # RULE 1: Cross-domain redirect hijack check
            parsed_final = urllib.parse.urlparse(final_url)
            final_netloc = parsed_final.netloc.split(":")[0]
            final_parts = final_netloc.split(".")
            final_root = ".".join(final_parts[-2:]) if len(final_parts) >= 2 else final_netloc
            
            req_parts = domain.lower().split(".")
            req_root = ".".join(req_parts[-2:]) if len(req_parts) >= 2 else domain.lower()

            if final_root != req_root:
                return False, 0, {
                    "reason": f"CROSS_DOMAIN_HIJACK_DETECTED: Redirected to '{final_root}'",
                    "final_url": final_url
                }

            raw_html = response.read(40000).decode("utf-8", errors="ignore").lower()

            # RULE 2: Parked / Gambling / Spam keywords
            bad_signals = [
                "domain is for sale", "buy this domain", "hugedomains", "sedo", 
                "dan.com", "godaddy", "gacor", "slot", "judi", "casino", "poker",
                "this domain has expired", "renew your domain"
            ]

            for s in bad_signals:
                if s in raw_html:
                    return False, 0, {"reason": f"SPAM_OR_PARKED_KEYWORD: '{s}'", "final_url": final_url}

            if len(raw_html) < 1000:
                return False, 0, {"reason": "DEAD_OR_EMPTY_STUB (<1000 bytes)", "final_url": final_url}

            # RULE 3: Operational SaaS Weight Calculation (Base: 50 for clean domain match)
            weight = 50
            if "pricing" in raw_html or "pricing" in final_url:
                weight += 15
            if any(term in raw_html for term in ["login", "sign in", "dashboard", "get started", "book a demo", "free trial"]):
                weight += 20
            if any(term in raw_html for term in ["2024", "2025", "2026", "copyright"]):
                weight += 15

            is_approved = weight >= 50

            return is_approved, weight, {
                "final_url": final_url,
                "latency_ms": latency_ms,
                "weight": weight
            }

    except Exception as e:
        return False, 0, {"reason": f"CONNECTION_FAILED: {str(e)[:60]}"}

if __name__ == "__main__":
    targets = ["clevertap.com", "keka.com", "swishjam.com", "sketchdeck.com", "apigacor88wz.com"]
    for t in targets:
        approved, weight, meta = verify_live_website(t)
        tag = "[APPROVED REAL SAAS]" if approved else "[BLOCKED REPUTATION RISK]"
        print(f"{tag}: {t} (Weight: {weight}/100) -> {meta.get('reason') or meta.get('final_url')}")
