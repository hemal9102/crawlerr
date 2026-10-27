#!/usr/bin/env python3
"""
TENSIX Multi-Variable MailOps Reconnaissance & Scorer
Calculates Bleed Scores (0-100) across 8 RFC & Vendor Sprawl Variables,
and maps each target to a bespoke personalized MailOps service package.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.parse

# Import base DoH resolver
sys.path.append(r"D:\projects\HK\tensix\scripts")
from forensic_dns_recon import get_dns_records, evaluate_spf_recursive

KNOWN_VENDORS = {
    "google": ["_spf.google.com", "aspmx.l.google.com"],
    "microsoft": ["spf.protection.outlook.com", "outlook.com"],
    "hubspot": ["hubspotemail.net", "hubspot.com"],
    "sendgrid": ["sendgrid.net", "sendgrid.com"],
    "mailgun": ["mailgun.org", "mailgun.com"],
    "mandrill": ["mandrillapp.com"],
    "sparkpost": ["sparkpostmail.com"],
    "salesforce": ["_spf.salesforce.com", "salesforce.com"],
    "zendesk": ["mail.zendesk.com"],
    "freshdesk": ["email.freshdesk.com", "freshdesk.com"],
    "klaviyo": ["klaviyo.com"],
    "intercom": ["intercom.com", "intercom-mail.com"],
    "postmark": ["postmarkapp.com"]
}

def analyze_vendor_sprawl(raw_spf: str):
    """Detects vendor sprawl and fragmentation in SPF records."""
    if not raw_spf:
        return []
    
    detected = []
    raw_lower = raw_spf.lower()
    for vendor, signatures in KNOWN_VENDORS.items():
        for sig in signatures:
            if sig in raw_lower:
                detected.append(vendor)
                break
    return list(set(detected))

def score_and_package_domain(domain: str, biz_type: str = "B2B SaaS"):
    """
    Evaluates the 8 RFC & Sprawl variables and computes BLEED_SCORE (0-100).
    Synthesizes a personalized service proposal.
    """
    domain = domain.strip().lower()
    
    # 1. Probe SPF
    txt_records = get_dns_records(domain, "TXT")
    spf_records = [r for r in txt_records if "v=spf1" in r]
    
    spf_raw = spf_records[0] if spf_records else None
    duplicate_spf = len(spf_records) > 1
    
    spf_lookups = 0
    spf_mechanisms = []
    if spf_raw:
        spf_lookups, spf_mechanisms = evaluate_spf_recursive(domain)
        
    vendors = analyze_vendor_sprawl(spf_raw)
    
    # 2. Probe DMARC
    dmarc_domain = f"_dmarc.{domain}"
    dmarc_records = get_dns_records(dmarc_domain, "TXT")
    dmarc_raw = next((r for r in dmarc_records if "v=DMARC1" in r), None)
    
    dmarc_policy = "MISSING"
    has_rua = False
    if dmarc_raw:
        match = re.search(r'p=([a-zA-Z]+)', dmarc_raw)
        if match:
            dmarc_policy = match.group(1).lower()
        has_rua = "rua=" in dmarc_raw

    # 3. Compute Bleed Score (0 to 100)
    w_spf = 0
    if not spf_raw or duplicate_spf:
        w_spf = 40
    elif spf_lookups > 10:
        w_spf = 40
    elif spf_lookups >= 8:
        w_spf = 25

    w_dmarc = 0
    if spf_lookups > 10 and dmarc_policy == "reject":
        w_dmarc = 30  # Fatal drop condition!
    elif dmarc_policy in ("missing", "none"):
        w_dmarc = 25
    elif not has_rua:
        w_dmarc = 15

    w_sprawl = min(len(vendors) * 5, 20)
    w_biz = 10 if "saas" in biz_type.lower() or "b2b" in biz_type.lower() else 5
    
    bleed_score = min(w_spf + w_dmarc + w_sprawl + w_biz, 100)

    # 4. Synthesize Personalized Service Packaging
    tripwire_offer = {}
    retainer_offer = {}

    if spf_lookups > 10:
        tripwire_offer = {
            "tier": "Emergency CIDR Flattening & RFC Alignment",
            "price_usd": 350,
            "scope": f"Consolidate {len(vendors)} disparate SaaS vendor inclusions into a static, aggregated CIDR block to reduce lookup count from {spf_lookups} down to <=3 without breaking any email workflows."
        }
    elif dmarc_policy in ("none", "missing"):
        tripwire_offer = {
            "tier": "Zero-Trust DMARC Hardening & Forensic RUA Pipeline",
            "price_usd": 400,
            "scope": "Deploy strict DMARC enforcement with automated aggregate reporting to eliminate brand spoofing and ensure Google/Yahoo 2024 compliance."
        }
    else:
        tripwire_offer = {
            "tier": "MTA Transport & Header Integrity Audit",
            "price_usd": 250,
            "scope": "Full cryptographic inspection of Return-Path vs From alignment and TLS 1.3 handshake verification."
        }

    # High-ticket Retainer Packaging ($1,500/mo MailOps)
    retainer_offer = {
        "tier": "TENSIX Autonomous MailOps Retainer",
        "price_usd_monthly": 1500,
        "deliverables": [
            f"Active DNS Guard: Real-time monitoring across your {len(vendors)} email platforms ({', '.join(vendors[:4])}) to prevent unvetted vendor sprawl.",
            "Continuous DMARC Threat Mitigation: Ingestion & analysis of daily XML aggregate reports with anomaly alerts.",
            "Zero-Bounce Transactional Assurance: Immediate triage of any 550 policy errors or Google Postmaster spam-rate drifts over 0.1%."
        ]
    }

    return {
        "domain": domain,
        "bleed_score": bleed_score,
        "is_priority_lead": bleed_score >= 60,
        "spf_lookups": spf_lookups,
        "spf_duplicate": duplicate_spf,
        "dmarc_policy": dmarc_policy,
        "has_dmarc_rua": has_rua,
        "detected_vendors": vendors,
        "vendor_count": len(vendors),
        "tripwire_service": tripwire_offer,
        "retainer_service": retainer_offer
    }

if __name__ == "__main__":
    targets = [
        ("keka.com", "B2B Payroll SaaS"),
        ("clevertap.com", "B2B Customer Engagement"),
        ("moengage.com", "B2B Customer Engagement"),
        ("sketchdeck.com", "YC Design Platform"),
        ("smartlead.ai", "Sales Outbound Platform")
    ]

    print("=" * 80)
    print("TENSIX AUTOMATED MULTI-VARIABLE SCORER & BESPOKE SERVICE GENERATOR")
    print("=" * 80)

    scored_dossier = []
    for d, b_type in targets:
        result = score_and_package_domain(d, b_type)
        scored_dossier.append(result)
        
        status = "[HIGH PRIORITY BLEEDING TARGET]" if result["is_priority_lead"] else "[MONITOR]"
        print(f"\n{status}: {result['domain']} (Bleed Score: {result['bleed_score']}/100)")
        print(f"  • SPF Lookups: {result['spf_lookups']}/10 | DMARC: {result['dmarc_policy']} (RUA: {result['has_dmarc_rua']})")
        print(f"  • Vendor Sprawl ({result['vendor_count']}): {', '.join(result['detected_vendors'])}")
        print(f"  • Immediate Tripwire: ${result['tripwire_service']['price_usd']} - {result['tripwire_service']['tier']}")
        print(f"  • Monthly MailOps Retainer: ${result['retainer_service']['price_usd_monthly']}/mo")

    # Persist structured dossier
    out_path = r"D:\projects\HK\tensix\data\scored_mailops_dossier.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(scored_dossier, f, indent=2)

    print(f"\n[+] Scored dossier persisted to: {out_path}")
