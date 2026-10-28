#!/usr/bin/env python3
"""
TENSIX Global High-Ticket Harvester & MailOps Auditor
Targets ultra-high liquidity, non-technical B2B sectors in:
1. Switzerland (Geneva & Zurich Wealth Management, Private Equity, Family Offices)
2. Dubai / UAE (DIFC Finance, Luxury Real Estate Brokerages, Tech Scaleups)
3. US High-Ticket B2B (Retained Executive Search, M&A Boutiques, High-Growth DTC)

Executes:
- 34-Variable MailOps & Boundary Inversion Reconnaissance
- Pre-flight RFC 5321 MX & Mailbox Handshake Verification
- Revenue-First Commercial Proposal Synthesis ($350 Triage / $1,500 Retainer)
"""

import sys
import os
import json
import time

sys.path.append(r"D:\projects\HK\crawler")
from mailops_scorer import score_and_package_domain
from smtp_rcpt_verifier import verify_email_comprehensive
from reputation_shield import verify_live_website

# Curated High-Ticket Discovery Target Pool across Switzerland, Dubai, and US
HIGH_TICKET_TARGET_POOL = [
    # --- SWISS WEALTH MANAGEMENT & ASSET MANAGERS ---
    {"domain": "pictet.com", "name": "Pictet Group", "country": "Switzerland", "sector": "Swiss Wealth Management", "primary_contact": "info@pictet.com"},
    {"domain": "lombardodier.com", "name": "Lombard Odier", "country": "Switzerland", "sector": "Swiss Private Banking", "primary_contact": "contact@lombardodier.com"},
    {"domain": "vontobel.com", "name": "Vontobel", "country": "Switzerland", "sector": "Swiss Investment Banking", "primary_contact": "corporate@vontobel.com"},
    {"domain": "edmond-de-rothschild.com", "name": "Edmond de Rothschild", "country": "Switzerland", "sector": "Swiss Private Wealth", "primary_contact": "contact@edmond-de-rothschild.com"},
    {"domain": "mirabaud.com", "name": "Mirabaud Group", "country": "Switzerland", "sector": "Swiss Private Banking", "primary_contact": "info@mirabaud.com"},
    {"domain": "reyl.com", "name": "REYL Intesa Sanpaolo", "country": "Switzerland", "sector": "Swiss Wealth Advisory", "primary_contact": "contact@reyl.com"},
    {"domain": "syzgroup.com", "name": "Bank Syz", "country": "Switzerland", "sector": "Swiss Boutique Private Bank", "primary_contact": "info@syzgroup.com"},
    {"domain": "bordier.com", "name": "Bordier & Cie", "country": "Switzerland", "sector": "Swiss Private Banking", "primary_contact": "geneva@bordier.com"},
    {"domain": "gonet.ch", "name": "Gonet & Cie", "country": "Switzerland", "sector": "Swiss Wealth Advisory", "primary_contact": "info@gonet.ch"},
    {"domain": "cité-gestion.com", "name": "Cite Gestion", "country": "Switzerland", "sector": "Swiss Wealth Management", "primary_contact": "info@cite-gestion.com"},

    # --- DUBAI / DIFC LUXURY REAL ESTATE & SCALEUPS ---
    {"domain": "hausandhaus.com", "name": "haus & haus", "country": "UAE", "sector": "Dubai Luxury Real Estate", "primary_contact": "info@hausandhaus.com"},
    {"domain": "allsoppandallsopp.com", "name": "Allsopp & Allsopp", "country": "UAE", "sector": "Dubai Real Estate Brokerage", "primary_contact": "admin@allsoppandallsopp.com"},
    {"domain": "fämproperties.com", "name": "fam Properties", "country": "UAE", "sector": "Dubai Real Estate Giant", "primary_contact": "info@famproperties.com"},
    {"domain": "betterhomes.com", "name": "Betterhomes", "country": "UAE", "sector": "Dubai Brokerage", "primary_contact": "customercare@betterhomes.com"},
    {"domain": "drivenproperties.com", "name": "Driven Properties", "country": "UAE", "sector": "Dubai Luxury Brokerage", "primary_contact": "info@drivenproperties.com"},
    {"domain": "elysian.com", "name": "Elysian Real Estate", "country": "UAE", "sector": "Dubai Luxury Brokerage", "primary_contact": "info@elysian.com"},
    {"domain": "postpay.io", "name": "Postpay", "country": "UAE", "sector": "DIFC Fintech BNPL", "primary_contact": "hello@postpay.io"},
    {"domain": "lean.tech", "name": "Lean Technologies", "country": "UAE", "sector": "DIFC Open Banking", "primary_contact": "contact@lean.tech"},
    {"domain": "ziina.com", "name": "Ziina", "country": "UAE", "sector": "Dubai P2P Fintech", "primary_contact": "support@ziina.com"},
    {"domain": "baraka.co", "name": "baraka", "country": "UAE", "sector": "DIFC Investment Platform", "primary_contact": "support@baraka.co"},

    # --- US RETAINED EXECUTIVE SEARCH & HIGH-TICKET B2B ---
    {"domain": "heidrick.com", "name": "Heidrick & Struggles", "country": "USA", "sector": "Retained Executive Search", "primary_contact": "contact@heidrick.com"},
    {"domain": "russellreynolds.com", "name": "Russell Reynolds Associates", "country": "USA", "sector": "Executive Search", "primary_contact": "info@russellreynolds.com"},
    {"domain": "spencerstuart.com", "name": "Spencer Stuart", "country": "USA", "sector": "Leadership Advisory", "primary_contact": "contact@spencerstuart.com"},
    {"domain": "kornferry.com", "name": "Korn Ferry", "country": "USA", "sector": "Global Organizational Consulting", "primary_contact": "info@kornferry.com"},
    {"domain": "insidetracker.com", "name": "InsideTracker", "country": "USA", "sector": "High-End HealthTech DTC", "primary_contact": "contactus@insidetracker.com"}
]

def run_global_harvester():
    print("=" * 85)
    print("TENSIX GLOBAL HIGH-TICKET CLIENT AUDITOR: SWITZERLAND | DUBAI | USA")
    print("=" * 85)

    results = []
    high_bleed_targets = []

    for idx, target in enumerate(HIGH_TICKET_TARGET_POOL):
        d = target["domain"]
        country = target["country"]
        sector = target["sector"]
        print(f"\n[{idx+1}/{len(HIGH_TICKET_TARGET_POOL)}] Probing {d} ({target['name']} - {country} / {sector})")

        # Gate 1: Liveness Check via Shield
        try:
            is_live, op_weight, shield_meta = verify_live_website(d, timeout=5)
            if not is_live:
                print(f"  [-] Skipped: Website failed liveness shield ({shield_meta.get('reason')})")
                continue
        except Exception:
            pass

        # Gate 2: 34-Variable Scorer
        try:
            audit = score_and_package_domain(d, biz_type=sector)
            bleed = audit["bleed_score"]
            lookups = audit["spf_lookups"]
            pol = audit["dmarc_policy"]
            vendors = audit["detected_vendors"]
            
            print(f"  [METRICS] Bleed Score: {bleed}/100 | Lookups: {lookups}/10 | DMARC: {pol}")
            print(f"  [VENDORS] ({len(vendors)}): {', '.join(vendors[:4])}")

            # Gate 3: Live MX Validation on Primary Contact
            contact = target["primary_contact"]
            mx_eval = verify_email_comprehensive(contact)
            print(f"  [MX AUDIT] {contact} -> Deliverable: {mx_eval['is_deliverable']} (Risk: {mx_eval['bounce_risk']})")

            record = {
                "name": target["name"],
                "domain": d,
                "country": country,
                "sector": sector,
                "bleed_score": bleed,
                "spf_lookups": lookups,
                "dmarc_policy": pol,
                "detected_vendors": vendors,
                "primary_contact": contact,
                "mx_deliverable": mx_eval["is_deliverable"],
                "bounce_risk": mx_eval["bounce_risk"],
                "tripwire_service": audit["tripwire_service"],
                "retainer_service": audit["retainer_service"]
            }
            results.append(record)

            if bleed >= 60 and mx_eval["is_deliverable"]:
                high_bleed_targets.append(record)
                print(f"  [!] QUALIFIED HIGH PRIORITY TARGET IDENTIFIED!")

        except Exception as e:
            print(f"  [-] Error scoring {d}: {e}")

        time.sleep(0.5)

    # Persist Dossier
    out_file = r"D:\projects\HK\tensix\data\global_high_ticket_dossier.json"
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 85)
    print(f"AUDIT COMPLETE! Total Targets Evaluated: {len(results)}")
    print(f"[*] Qualified High-Bleed Targets (Score >= 60): {len(high_bleed_targets)}")
    print(f"Persisted to: {out_file}")
    print("=" * 85)

    print("\nTOP QUALIFIED LEADS FOR OUTREACH:")
    for h in high_bleed_targets:
        curr = "CHF" if h["country"] == "Switzerland" else ("AED" if h["country"] == "UAE" else "USD")
        print(f"* {h['name']} ({h['domain']} - {h['country']}): Bleed {h['bleed_score']}/100 | Lookups: {h['spf_lookups']}/10 | DMARC: {h['dmarc_policy']}")

if __name__ == "__main__":
    run_global_harvester()
