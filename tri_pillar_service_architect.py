#!/usr/bin/env python3
"""
TENSIX Unified Tri-Pillar Engine (RFC, GEO/AI Citation, & Email Presentation)
Compiles variables, scoring formulas, and bespoke service packages directly synthesized
from docs 17 (RFC Web Protocols), 09 (48 Algorithmic Variables), and email-html-presentation-layer.md.
"""

import json
from typing import Dict, List

# ==============================================================================
# PILLAR 1: RFC TRANSPORT & AGENT READINESS WEIGHTS (From Doc 17)
# ==============================================================================
RFC_WEB_WEIGHTS = {
    "RFC_8288_LINK_HEADER": {
        "points": 25,
        "description": "Exposes HTTP Link headers (e.g. </llms.txt>; rel='describedby', </api-catalog>)",
        "failure_impact": "AI crawlers (ClaudeBot, GPTBot) cannot discover markdown/APIs in 1 round-trip."
    },
    "RFC_9309_ROBOTS_EXCLUSION": {
        "points": 20,
        "description": "Explicit token authorization for AI agents (ClaudeBot, PerplexityBot, GPTBot)",
        "failure_impact": "Zero AI crawler visibility or aggressive rate-limiting."
    },
    "RFC_9111_EDGE_CACHE_CONTROL": {
        "points": 20,
        "description": "Strict immutable/stale-while-revalidate edge cache headers & ETag validation",
        "failure_impact": "CrUX/PageSpeed TTFB penalties causing ranking drops."
    },
    "RFC_7763_CONTENT_NEGOTIATION": {
        "points": 20,
        "description": "Content negotiation returning text/markdown for LLM ingestors",
        "failure_impact": "Agents burn 10x tokens parsing heavy JavaScript DOM instead of clean markdown."
    },
    "RFC_8615_WELL_KNOWN": {
        "points": 15,
        "description": "Published /.well-known/security.txt and /.well-known/mcp manifests",
        "failure_impact": "Zero institutional trust verification."
    }
}

# ==============================================================================
# PILLAR 2: GEO & AI CITATION DOMINANCE WEIGHTS (From Doc 09)
# ==============================================================================
GEO_AI_CITATION_WEIGHTS = {
    "JSON_LD_ENTITY_GRAPH": {
        "points": 30,
        "description": "Valid W3C JSON-LD 1.1 AST (TechArticle, FAQPage, Organization, sameAs Wikidata QIDs)",
        "failure_impact": "LLMs hallucinate brand facts; zero inclusion in Google AI Overviews / Perplexity."
    },
    "STRUCTURED_HTML_TABLES": {
        "points": 20,
        "description": "Clean semantic <table> data blocks for direct comparative token matrix ingestion",
        "failure_impact": "AI Overviews bypass unstructured prose in favor of competitors' clean tables."
    },
    "DEFINITION_ANCHORS": {
        "points": 20,
        "description": "40-word declarative lead definition sentences ('X is a...') for zero-shot snippets",
        "failure_impact": "Loss of Google Position 0 featured snippet card."
    },
    "STRUCTURED_LISTS": {
        "points": 15,
        "description": "Hierarchical <ol>/<ul> step instructions matching LLM synthesis format",
        "failure_impact": "LLM synthesis prompts quote external competitors."
    },
    "EEAT_INSTITUTIONAL_SIGNALS": {
        "points": 15,
        "description": "Authoritative author nodes, peer-reviewed citations, verified IETF/W3C/patent refs",
        "failure_impact": "Classified as low-confidence synthetic content."
    }
}

# ==============================================================================
# PILLAR 3: EMAIL HTML PRESENTATION & ANTI-CLIPPING WEIGHTS (From Presentation Layer)
# ==============================================================================
EMAIL_PRESENTATION_WEIGHTS = {
    "P1_GMAIL_102KB_CLIPPING_BUDGET": {
        "points": 30,
        "description": "HTML payload strictly under 98,000 bytes uncompressed (zero base64 images)",
        "failure_impact": "Gmail cuts message; 0% open tracking, truncated unsubscribe triggers instant spam flags."
    },
    "P2_GHOST_TABLE_VML_SHIMS": {
        "points": 25,
        "description": "Fluid hybrid ghost tables with MSO/VML shims for desktop Outlook 96-150 DPI displays",
        "failure_impact": "Outlook desktop destroys layout, text overlaps, CTA buttons break completely."
    },
    "P6_DARK_MODE_INVERSION_SHIELD": {
        "points": 20,
        "description": "Two-tier Dark Mode CSS overrides (@media prefers-color-scheme & [data-ogsc])",
        "failure_impact": "Email client auto-inverts dark logos onto black backgrounds (invisible text/logos)."
    },
    "P7_PREHEADER_BUFFER_FLOOD": {
        "points": 15,
        "description": "Preheader buffer flood via &zwnj;&nbsp; chain suppressing unwanted preview text",
        "failure_impact": "Recipient preview snippet shows 'View in browser' or raw CSS garbage."
    },
    "P14_SCHEMA_INBOX_ACTIONS": {
        "points": 10,
        "description": "Schema.org microdata / JSON-LD for One-Click Actions in Gmail (ViewAction / RSVP)",
        "failure_impact": "Missing interactive action pill in recipient inbox list."
    }
}

# ==============================================================================
# THE 4 HIGH-TICKET BESPOKE SERVICE PACKAGES (Synthesized from All 3 Docs)
# ==============================================================================
TENSIX_COMMERCIAL_SERVICE_PACKAGES = [
    {
        "service_id": "SERVICE-01-MAILOPS",
        "name": "Emergency RFC 7208 CIDR Flattening & Mailbox Triage",
        "tier_type": "Tripwire (Immediate Fix)",
        "price_usd": 350,
        "timeline": "Same-Day Delivery (2 to 4 hours)",
        "target_audience": "B2B SaaS hitting 11-19 SPF lookups with strict DMARC",
        "deliverables": [
            "Deconstruct all third-party vendor includes (HubSpot, SendGrid, Zendesk, Mandrill, Salesforce).",
            "Generate optimized, aggregated CIDR network blocks to reduce lookups down to <= 3.",
            "Eliminate RFC 7208 PermErrors and test live delivery on Google Workspace and Office 365.",
            "Issue verified DNS patch files for Cloudflare, Route53, or GoDaddy."
        ]
    },
    {
        "service_id": "SERVICE-02-PRESENTATION",
        "name": "Bulletproof Anti-Clipping HTML Email Template Architecture",
        "tier_type": "Design & Systems Engineering",
        "price_usd": 750,
        "timeline": "3 Days",
        "target_audience": "E-commerce, B2B SaaS, and high-volume newsletters experiencing low opens or clipping",
        "deliverables": [
            "Re-engineer raw email HTML under the strict 98 KB Gmail clipping ceiling (zero Base64 leakage).",
            "Implement Outlook MSO Ghost Tables and VML vector buttons for 96/120/150 DPI display scaling.",
            "Deploy two-tier Dark Mode overrides to prevent logo/color inversion on Apple Mail & Outlook.",
            "Configure Preheader Buffer Flooding (&zwnj;&nbsp;) to guarantee clean preview snippets.",
            "Full verification across Litmus / Email on Acid test suites (40+ mobile and desktop clients)."
        ]
    },
    {
        "service_id": "SERVICE-03-GEO-AI",
        "name": "Autonomous Agent Readiness & GEO AI Citation Dominance Engine",
        "tier_type": "High-Ticket Systems Optimization",
        "price_usd": 1200,
        "timeline": "5 Days",
        "target_audience": "B2B SaaS, tech platforms, and venture-backed startups losing search traffic to AI answers",
        "deliverables": [
            "Inject RFC 8288 Link headers and deploy /.well-known/ai-catalog for zero-friction LLM discovery.",
            "Compile and validate full W3C JSON-LD 1.1 AST Entity Graph with Wikidata QID entity grounding.",
            "Re-structure content with 40-word BERT Definition Anchors and structured <table> comparison blocks.",
            "Implement content negotiation (Accept: text/markdown) for instant token-efficient agent ingestion.",
            "Attain 90+ score on Claude's isitaiagentready.com and Google Rich Results."
        ]
    },
    {
        "service_id": "SERVICE-04-RETAINER",
        "name": "TENSIX Autonomous MailOps & Reputation Governance Retainer",
        "tier_type": "Monthly Recurring Retainer",
        "price_usd_monthly": 1500,
        "timeline": "Ongoing Continuous Supervision",
        "target_audience": "Funded startups, scaleups, and enterprises with multiple email vendor platforms",
        "deliverables": [
            "Active DNS Sprawl Guard: Continuous monitoring across all SaaS tools to prevent unvetted SPF bloat.",
            "Automated DMARC Aggregate Threat Ingestion: Daily parsing of XML failure reports with instant alerts.",
            "Zero-Bounce Transactional Guarantee: Real-time triage of Google Postmaster spam rate drifts over 0.1%.",
            "Monthly Deliverability Forensic Ledger with executive deliverability health score."
        ]
    }
]

def print_master_catalog():
    print("=" * 80)
    print("TENSIX TRI-PILLAR WEIGHTS & COMMERCIAL SERVICE CATALOG")
    print("Synthesized from Docs 17, 09, and Email Presentation Layer")
    print("=" * 80)

    print("\n--- 1. RFC TRANSPORT & AGENT READINESS WEIGHTS (100 PTS) ---")
    for k, v in RFC_WEB_WEIGHTS.items():
        print(f"  • {k} ({v['points']} pts): {v['description']}")

    print("\n--- 2. GEO AI CITATION DOMINANCE WEIGHTS (100 PTS) ---")
    for k, v in GEO_AI_CITATION_WEIGHTS.items():
        print(f"  • {k} ({v['points']} pts): {v['description']}")

    print("\n--- 3. EMAIL HTML PRESENTATION & ANTI-CLIPPING WEIGHTS (100 PTS) ---")
    for k, v in EMAIL_PRESENTATION_WEIGHTS.items():
        print(f"  • {k} ({v['points']} pts): {v['description']}")

    print("\n" + "=" * 80)
    print("--- 4. BESPOKE COMMERCIAL SERVICE PACKAGES ---")
    print("=" * 80)
    for s in TENSIX_COMMERCIAL_SERVICE_PACKAGES:
        print(f"\n[{s['service_id']}] {s['name']}")
        price = f"${s.get('price_usd')} (One-time)" if "price_usd" in s else f"${s.get('price_usd_monthly')}/mo (Retainer)"
        print(f"  • Tier: {s['tier_type']} | Price: {price} | Timeline: {s['timeline']}")
        print(f"  • Target: {s['target_audience']}")
        print("  • Scope of Deliverables:")
        for d in s["deliverables"]:
            print(f"      - {d}")

if __name__ == "__main__":
    print_master_catalog()
    
    # Save to disk as central catalog
    out_file = r"D:\projects\HK\tensix\data\tri_pillar_services_catalog.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({
            "rfc_web_weights": RFC_WEB_WEIGHTS,
            "geo_ai_weights": GEO_AI_CITATION_WEIGHTS,
            "email_presentation_weights": EMAIL_PRESENTATION_WEIGHTS,
            "commercial_packages": TENSIX_COMMERCIAL_SERVICE_PACKAGES
        }, f, indent=2)
    print(f"\n[+] Master Tri-Pillar Catalog saved to: {out_file}")
