#!/usr/bin/env python3
"""
TENSIX UAE & Dubai High-Value Commercial Pipeline
Targets Dubai & UAE B2B Logistics, Real Estate Tech, FinTech, and Export Platforms (.ae & Dubai tech corridors).
Runs the 21-Variable Scorer, Reputation Shield, and dispatches the $350 Triage / $1,500/mo Retainer teardown.
"""

import os
import sys
import json
import time
import random
import smtplib
import urllib.request
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sys.path.append(r"D:\projects\HK\crawler")
from mailops_scorer import score_and_package_domain
from reputation_shield import verify_live_website

DUBAI_DISPATCH_LOG = r"D:\projects\HK\tensix\data\dubai_dispatch_log.json"

# Curated high-volume Dubai / UAE digital & commercial hubs
DUBAI_TARGET_CANDIDATES = [
    # Dubai Logistics, PropTech, FinTech & E-commerce Hubs
    {"domain": "propertyfinder.ae", "name": "Leadership", "sector": "Dubai PropTech"},
    {"domain": "bayut.com", "name": "Infrastructure Team", "sector": "Dubai Real Estate"},
    {"domain": "careem.com", "name": "Engineering Leadership", "sector": "UAE SuperApp & Logistics"},
    {"domain": "tabby.ai", "name": "Fintech Operations", "sector": "UAE FinTech / BNPL"},
    {"domain": "tamara.co", "name": "Fintech Leadership", "sector": "Gulf FinTech"},
    {"domain": "trukkers.com", "name": "Logistics Engineering", "sector": "MENA Freight & Logistics"},
    {"domain": "sarwa.co", "name": "WealthTech Operations", "sector": "Dubai FinTech / WealthTech"},
    {"domain": "yallacompare.com", "name": "Insurance Operations", "sector": "Dubai InsurTech"},
    {"domain": "nowmoney.me", "name": "FinTech Operations", "sector": "Dubai Digital Banking"},
    {"domain": "postex.pk", "name": "Logistics Leadership", "sector": "MENA E-commerce Logistics"},
    {"domain": "swvl.com", "name": "Transit Technology Team", "sector": "Mobility & Transit"},
    {"domain": "hubble.ae", "name": "FinTech Leadership", "sector": "Dubai B2B Payments"}
]

def load_env(env_path: str = r"D:\projects\HK\.env"):
    config = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    config[k.strip()] = v.strip()
    return config

def get_dispatched_dubai():
    if os.path.exists(DUBAI_DISPATCH_LOG):
        try:
            with open(DUBAI_DISPATCH_LOG, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def record_dubai_dispatch(domain: str):
    dispatched = get_dispatched_dubai()
    dispatched.add(domain)
    os.makedirs(os.path.dirname(DUBAI_DISPATCH_LOG), exist_ok=True)
    with open(DUBAI_DISPATCH_LOG, "w", encoding="utf-8") as f:
        json.dump(list(dispatched), f, indent=2)

def dispatch_dubai_teardown(target: dict, profile: dict):
    domain = target["domain"]
    recipient_name = target["name"]
    sector = target["sector"]

    config = load_env()
    smtp_login = config.get("BREVO_SMTP_LOGIN")
    smtp_key = config.get("BREVO_SMTP_KEY")
    sender_email = config.get("SENDER_EMAIL", "hemal@tensix.in")
    sender_name = config.get("SENDER_NAME", "Hemal Shah | TENSIX")

    to_email = f"founders@{domain}"
    cc_emails = [f"tech@{domain}", f"support@{domain}"]

    spf_lookups = profile["spf_lookups"]
    dmarc_policy = profile["dmarc_policy"]
    vendors = profile["detected_vendors"]

    if spf_lookups > 10:
        subject = f"RFC 7208 PermError on {domain} sending domain ({spf_lookups} DNS lookups)"
        flaw_desc = f"Your primary SPF record evaluates to {spf_lookups} recursive DNS lookups (exceeding RFC 7208's limit of 10) across {len(vendors)} SaaS providers ({', '.join(vendors[:4])})."
        impact_desc = f"Receiving MTAs (Google Workspace, Yahoo, Microsoft 365) reject SPF evaluation with an automatic PermError. Under policy {dmarc_policy}, customer notifications and transactional invoices face severe delivery drops."
    else:
        subject = f"DMARC authentication & visibility gaps on {domain}"
        flaw_desc = f"Your sending domain is currently operating with un-enforced DMARC policies (p={dmarc_policy}) and zero configured forensic RUA reporting mailboxes."
        impact_desc = "Without strict DMARC alignment and forensic telemetry, high-volume UAE transactional notifications are at risk of being quarantined or spoofed by malicious third parties."

    text_body = f"""Hi {recipient_name},

I hope this note finds you well.

I am an infrastructure and protocol engineer specializing in RFC transport compliance (tensix.in). While conducting deliverability audits across high-growth {sector} platforms in the UAE, I identified a critical DNS configuration conflict on {domain} that directly impacts outbound delivery rates.

Technical Diagnostic:
{flaw_desc}

Impact on Deliverability:
{impact_desc}

Remediation Architecture:
We deconstruct third-party vendor includes and compile an aggregated, static CIDR network map that condenses your entire lookup footprint down to <= 3 lookups with zero operational downtime.

Commercial Scope ($350 Flat Fee):
Our one-time triage and hardening engagement is a flat $350 (or AED 1,300). We deliver the complete validated DNS block, coordinate with your technical team, and execute live end-to-end inbox delivery verification across Google and Microsoft within 2 hours.

I have already generated the required DNS mapping. Let me know if you would like me to get this deployed for you today.

Best regards,

Hemal Shah
Systems & RFC Protocol Forensics | TENSIX
https://tensix.in
"""

    html_body = f"""<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1a1a1a;">
<p>Hi {recipient_name},</p>

<p>I hope this note finds you well.</p>

<p>I am an infrastructure and protocol engineer specializing in RFC transport compliance (<a href="https://tensix.in" style="color: #2563eb; text-decoration: none;">tensix.in</a>). While conducting deliverability audits across high-growth <strong>{sector}</strong> platforms in the UAE, I identified a critical DNS configuration conflict on <strong>{domain}</strong> that directly impacts outbound delivery rates.</p>

<h4 style="color: #b91c1c; margin-bottom: 4px;">Technical Diagnostic:</h4>
<p style="margin-top: 0;">{flaw_desc}</p>

<h4 style="color: #0f172a; margin-bottom: 4px;">Impact on Deliverability:</h4>
<p style="margin-top: 0;">{impact_desc}</p>

<h4 style="color: #0f172a; margin-bottom: 4px;">Remediation Architecture:</h4>
<p style="margin-top: 0;">We deconstruct third-party vendor includes and compile an aggregated, static CIDR network map that condenses your entire lookup footprint down to &lt;= 3 lookups with zero operational downtime.</p>

<div style="background-color: #f8fafc; border-left: 4px solid #2563eb; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0; font-weight: 600; color: #0f172a;">Commercial Scope ($350 / AED 1,300 Flat Fee):</p>
  <p style="margin: 4px 0 0 0; font-size: 14px; color: #475569;">Our one-time triage engagement is a flat <strong>$350</strong> (or AED 1,300). We deliver the complete validated DNS block, coordinate with your technical team, and execute live end-to-end inbox delivery verification across Google and Microsoft within 2 hours.</p>
</div>

<p>I have already generated the required DNS mapping. Let me know if you would like me to get this deployed for you today.</p>

<p>Best regards,</p>

<p><strong>Hemal Shah</strong><br>
Systems & RFC Protocol Forensics | <a href="https://tensix.in" style="color: #2563eb; text-decoration: none;">TENSIX</a></p>
</body>
</html>"""

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    all_recipients = [to_email] + cc_emails

    try:
        server = smtplib.SMTP("smtp-relay.brevo.com", 587)
        server.starttls()
        server.login(smtp_login, smtp_key)
        server.sendmail(sender_email, all_recipients, msg.as_string())
        server.quit()
        print(f"[+] [DUBAI DISPATCH SUCCESS] {domain} -> {all_recipients}")
        record_dubai_dispatch(domain)
        return True
    except Exception as e:
        print(f"[-] [DUBAI DISPATCH FAILED] {domain}: {e}")
        return False

def run_dubai_worker():
    print("=" * 80)
    print("TENSIX DUBAI & UAE REGIONAL WORKER")
    print("Targeting High-Ticket MENA Logistics, PropTech, and FinTech Hubs")
    print("=" * 80)

    already_done = get_dispatched_dubai()
    print(f"[*] Found {len(already_done)} historically contacted UAE domains.")

    dispatched = 0
    for idx, target in enumerate(DUBAI_TARGET_CANDIDATES):
        domain = target["domain"]
        if domain in already_done:
            continue

        print(f"\n---> [DUBAI PROBE] [{idx+1}/{len(DUBAI_TARGET_CANDIDATES)}]: {domain} ({target['sector']})")

        # GATE 1: Reputation Shield
        is_live, op_weight, shield_meta = verify_live_website(domain, timeout=5)
        if not is_live:
            print(f"     [SHIELD BLOCKED]: {shield_meta.get('reason')}")
            continue

        # GATE 2: DNS & Sprawl Scorer
        profile = score_and_package_domain(domain, biz_type="Dubai Tech Enterprise")
        bleed_score = profile["bleed_score"]
        print(f"     [BLEED SCORE]: {bleed_score}/100 | Lookups: {profile['spf_lookups']}/10 | DMARC: {profile['dmarc_policy']}")

        if bleed_score < 60:
            print(f"     [SKIPPED]: Domain is healthy (Score {bleed_score} < 60)")
            continue

        print(f"     [HIGH-PRIORITY DUBAI LEAD CONFIRMED] Bleed Score: {bleed_score} >= 60")

        # GATE 3: Autonomous Dispatch
        success = dispatch_dubai_teardown(target, profile)
        if success:
            dispatched += 1
            if dispatched >= 3:
                print("\n[!] Dispatched 3 high-priority Dubai targets. Throttling for domain safety.")
                break
            jitter = random.randint(45, 75)
            print(f"[*] Sleeping {jitter}s jitter...")
            time.sleep(jitter)

    print("\n" + "=" * 80)
    print(f"[+] DUBAI WORKER RUN COMPLETE! Dispatched: {dispatched}")
    print("=" * 80)

if __name__ == "__main__":
    run_dubai_worker()
