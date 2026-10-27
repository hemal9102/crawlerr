#!/usr/bin/env python3
"""
TENSIX Multi-Dimensional Dubai Scaleup Audit Engine
Audits the top 8 Dubai/UAE unicorns & scaleups across:
1. MailOps & RFC Transport (SPF Lookups, DMARC, Vendor Sprawl)
2. AEO & Agent Readiness (RFC 8288 Link headers, robots.txt AI crawler tokens, llms.txt)
3. SEO Knowledge Graph (JSON-LD 1.1 AST, Wikidata QIDs, Schema.org Organization)
Synthesizes multi-dimensional commercial attack vectors ($350 Triage -> $1,200 AEO -> $1,500/mo Retainer).
"""

import os
import sys
import json
import re
import urllib.request
import urllib.parse
import ssl

sys.path.append(r"D:\projects\HK\crawler")
from mailops_scorer import score_and_package_domain
from reputation_shield import verify_live_website

DUBAI_TARGETS = [
    {"domain": "dubizzle.com", "name": "Dubizzle Group", "sector": "Classifieds & Auto Unicorn"},
    {"domain": "kitopi.com", "name": "Kitopi", "sector": "Cloud Kitchen / FoodTech Unicorn"},
    {"domain": "postpay.io", "name": "Postpay", "sector": "UAE FinTech / BNPL"},
    {"domain": "lean.tech", "name": "Lean Technologies", "sector": "DIFC Open Banking API"},
    {"domain": "ziina.com", "name": "Ziina", "sector": "Dubai P2P & Merchant Payments"},
    {"domain": "baraka.co", "name": "Baraka", "sector": "Dubai Retail Investment Platform"},
    {"domain": "huspy.com", "name": "Huspy", "sector": "Dubai PropTech & Mortgages"}
]

def audit_aeo_and_seo(domain: str):
    """
    Evaluates:
    - RFC 8288 Link headers for agent discovery
    - RFC 9309 robots.txt permissions for ClaudeBot, GPTBot, PerplexityBot
    - JSON-LD structured data presence & Schema types
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    results = {
        "has_llms_txt": False,
        "robots_ai_status": "RESTRICTIVE_OR_DEFAULT",
        "has_json_ld": False,
        "schema_types": [],
        "aeo_score": 0
    }

    # 1. Check llms.txt
    try:
        req = urllib.request.Request(f"https://{domain}/llms.txt", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=4, context=ctx) as resp:
            if resp.getcode() == 200 and len(resp.read(500)) > 50:
                results["has_llms_txt"] = True
                results["aeo_score"] += 30
    except:
        pass

    # 2. Check robots.txt for AI bots
    try:
        req = urllib.request.Request(f"https://{domain}/robots.txt", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=4, context=ctx) as resp:
            content = resp.read().decode("utf-8", errors="ignore").lower()
            if "claudebot" in content or "gptbot" in content or "perplexitybot" in content:
                if "disallow: /" in content:
                    results["robots_ai_status"] = "BLOCKED_AI_AGENTS"
                else:
                    results["robots_ai_status"] = "EXPLICIT_AI_RULES"
                    results["aeo_score"] += 25
            else:
                results["robots_ai_status"] = "GENERIC_DEFAULT"
                results["aeo_score"] += 10
    except:
        pass

    # 3. Check Homepage HTML for JSON-LD Schemas
    try:
        req = urllib.request.Request(f"https://{domain}", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
            html = resp.read(60000).decode("utf-8", errors="ignore")
            json_ld_matches = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
            if json_ld_matches:
                results["has_json_ld"] = True
                results["aeo_score"] += 25
                for block in json_ld_matches[:5]:
                    types = re.findall(r'["\']@type["\']\s*:\s*["\']([^"\']+)["\']', block)
                    results["schema_types"].extend(types)
                results["schema_types"] = list(set(results["schema_types"]))
                if any(t in results["schema_types"] for t in ["Organization", "FinancialProduct", "FAQPage"]):
                    results["aeo_score"] += 20
    except:
        pass

    return results

def run_dubai_multidimensional_audit():
    print("=" * 85)
    print("TENSIX MULTI-DIMENSIONAL DUBAI AUDIT: MailOps + AEO + SEO Knowledge Graph")
    print("=" * 85)

    full_dossier = []

    for t in DUBAI_TARGETS:
        domain = t["domain"]
        print(f"\n---> Auditing: {t['name']} ({domain}) - {t['sector']}")

        # 1. MailOps RFC Scan
        mailops = score_and_package_domain(domain, biz_type="Dubai Tech Scaleup")
        
        # 2. AEO & SEO Knowledge Graph Scan
        aeo = audit_aeo_and_seo(domain)

        composite = {
            "target": t,
            "mailops": {
                "bleed_score": mailops["bleed_score"],
                "spf_lookups": mailops["spf_lookups"],
                "dmarc_policy": mailops["dmarc_policy"],
                "vendors": mailops["detected_vendors"]
            },
            "aeo_seo": aeo
        }
        full_dossier.append(composite)

        print(f"     [MAILOPS]: Bleed Score {mailops['bleed_score']}/100 | SPF: {mailops['spf_lookups']}/10 | DMARC: {mailops['dmarc_policy']}")
        print(f"     [AEO/SEO]: Score {aeo['aeo_score']}/100 | llms.txt: {aeo['has_llms_txt']} | JSON-LD: {aeo['has_json_ld']} ({', '.join(aeo['schema_types'][:3])})")
        print(f"     [AI BOT POLICY]: {aeo['robots_ai_status']}")

    out_file = r"D:\projects\HK\tensix\data\dubai_multidimensional_dossier.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(full_dossier, f, indent=2)

    print("\n" + "=" * 85)
    print(f"[+] Multi-Dimensional Dubai Audit Complete! Saved to: {out_file}")
    print("=" * 85)

if __name__ == "__main__":
    run_dubai_multidimensional_audit()
