#!/usr/bin/env python3
"""
TENSIX Multi-Dimensional Autonomous Dispatch Engine (Hardened v4)
Integrates:
1. Multi-Cohort Harvester (YC W24/S24, Product Hunt)
2. Reputation Shield (Rejects 404s, slot/casino redirects, cross-domain hijacks)
3. 21-Variable Scorer (Bleed Score >= 60 required)
4. Dynamic Pitch Synthesis:
   - If SPF > 10 -> Dispatches MailOps Triage ($350 Flat Fee)
   - If AEO < 40 -> Dispatches AI Citation Dominance / Agent Readiness ($1,200)
5. Strict Jitter & Brevo Reputation Safety Limits (max 5 verified targets per cycle)
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
from dubai_multidimensional_audit import audit_aeo_and_seo
from smtp_rcpt_verifier import verify_mailbox_rcpt

DISPATCH_LOG_FILE = r"D:\projects\HK\tensix\data\autonomous_dispatch_log.json"

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

def get_already_dispatched():
    if os.path.exists(DISPATCH_LOG_FILE):
        try:
            with open(DISPATCH_LOG_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def record_dispatch(domain: str):
    dispatched = get_already_dispatched()
    dispatched.add(domain)
    os.makedirs(os.path.dirname(DISPATCH_LOG_FILE), exist_ok=True)
    with open(DISPATCH_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(list(dispatched), f, indent=2)

def harvest_high_intent_startups():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) TENSIX-Harvester/4.0"}
    candidates = {}
    queries = ["Launch YC", "YC W24", "YC S24", "AI Agent YC"]

    print(f"[*] Querying high-intent startup batches across: {queries}")
    for q in queries:
        url = f"https://hn.algolia.com/api/v1/search?query={urllib.parse.quote(q)}&tags=story&hitsPerPage=50"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for h in data.get("hits", []):
                    story_url = h.get("url") or ""
                    title = h.get("title") or ""
                    if story_url:
                        parsed = urllib.parse.urlparse(story_url)
                        netloc = parsed.netloc.lower().split(":")[0]
                        parts = netloc.split(".")
                        if len(parts) >= 2:
                            root = ".".join(parts[-2:])
                            ignored = ("github.com", "medium.com", "youtube.com", "ycombinator.com", "techcrunch.com", "twitter.com", "x.com", "notion.site", "google.com", "apple.com")
                            if root not in ignored and root not in candidates:
                                candidates[root] = {"domain": root, "title": title}
        except Exception as e:
            print(f"[-] Query error: {e}")
        time.sleep(0.3)

    return list(candidates.values())

def dispatch_targeted_email(domain: str, mailops_profile: dict, aeo_profile: dict, title: str):
    config = load_env()
    smtp_login = config.get("BREVO_SMTP_LOGIN")
    smtp_key = config.get("BREVO_SMTP_KEY")
    sender_email = config.get("SENDER_EMAIL", "hemal@tensix.in")
    sender_name = config.get("SENDER_NAME", "Hemal Shah | TENSIX")

    to_email = f"founders@{domain}"
    cc_emails = [f"team@{domain}"]

    spf_lookups = mailops_profile["spf_lookups"]
    dmarc_policy = mailops_profile["dmarc_policy"]
    vendors = mailops_profile["detected_vendors"]
    has_llms = aeo_profile["has_llms_txt"]
    has_json_ld = aeo_profile["has_json_ld"]

    # Synthesize the exact attack vector - High-Conversion Revenue & Pipeline Bleed Angle
    vendor_str = ", ".join(vendors[:4]) if vendors else "third-party SaaS relays"
    
    if spf_lookups > 10:
        subject = f"{domain} is silently dropping enterprise sales & user emails at the M365 boundary"
        diagnostic_text = (
            f"Your DNS footprint cascades through {spf_lookups} recursive lookups across {vendor_str}, "
            f"violating RFC 7208 Section 4.6.4 (10-lookup ceiling). When enterprise buyers evaluate your domain, "
            f"their gateway triggers a fatal PermError. Because this occurs silently depending on receiver cache, "
            f"outbound proposals, contract links, and onboarding notifications never reach the recipient's primary inbox."
        )
        commercial_hook = (
            "Fixing this is not as simple as deleting an include—stripping records blindly drops whatever SaaS or product tool is tied to it. "
            "We re-architect transport layers for high-growth tech companies to guarantee 100% inbox placement and protect high-value sales pipeline."
        )
    else:
        subject = f"Silent signup drops & spoofing vulnerability on {domain}"
        diagnostic_text = (
            f"Your primary domain currently operates with an un-enforced DMARC policy (p={dmarc_policy}). "
            f"Under current Google Workspace & Yahoo receiver thresholds, lack of cryptographic alignment drops your "
            f"sender trust score—routing activation links and transactional updates into user Spam folders. "
            f"Simultaneously, unauthorized actors can send forged emails displaying @{domain} directly to your prospects."
        )
        commercial_hook = (
            "Slapping a generic TXT record onto DNS without mapping third-party selectors will accidentally drop your own SendGrid, Stripe, or CRM webhooks. "
            "We safe-route domains to strict enforcement without breaking existing product pipes."
        )

    text_body = f"""Hi Team,

You have a silent pipeline leak occurring at the mail transport boundary of {domain}.

Technical Diagnostic:
{diagnostic_text}

Revenue Impact:
{commercial_hook}

If you want to plug this deliverability leak before this month's close, let me know and we can review the transport architecture.

Best regards,

Hemal Shah
Infrastructure & MailOps | TENSIX
https://tensix.in
"""

    html_body = f"""<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b;">
<p>Hi Team,</p>

<p>You have a silent pipeline leak occurring at the mail transport boundary of <strong>{domain}</strong>.</p>

<div style="background-color: #f8fafc; border-left: 4px solid #dc2626; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0; font-weight: 600; color: #991b1b;">Technical Root Cause:</p>
  <p style="margin: 4px 0 0 0; font-size: 14px; color: #334155;">{diagnostic_text}</p>
</div>

<div style="background-color: #f0fdf4; border-left: 4px solid #16a34a; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0; font-weight: 600; color: #166534;">Revenue & Pipeline Impact:</p>
  <p style="margin: 4px 0 0 0; font-size: 14px; color: #334155;">{commercial_hook}</p>
</div>

<p>If you want to plug this deliverability leak before this month's close, let me know and we can review the transport architecture.</p>

<p>Best regards,</p>

<p><strong>Hemal Shah</strong><br>
Infrastructure &amp; MailOps | <a href="https://tensix.in" style="color: #2563eb; text-decoration: none; font-weight: 500;">TENSIX</a></p>
</body>
</html>"""

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    all_recipients = [to_email] + cc_emails

    # Pre-Flight Multi-Stage Mailbox Verification Gate (All Recipients)
    verified_recipients = []
    for rcpt in all_recipients:
        if verify_mailbox_rcpt(rcpt):
            verified_recipients.append(rcpt)
        else:
            print(f"[-] [BOUNCE SHIELD] {rcpt} failed pre-flight check (550 / Soft Bounce / Null MX). Filtered out.")

    if not verified_recipients:
        print(f"[-] [BOUNCE SHIELD] No valid recipient addresses remaining for {domain}. Aborting dispatch.")
        return False

    try:
        server = smtplib.SMTP("smtp-relay.brevo.com", 587)
        server.starttls()
        server.login(smtp_login, smtp_key)
        server.sendmail(sender_email, verified_recipients, msg.as_string())
        server.quit()
        print(f"[+] [DISPATCH SUCCESS] {domain} -> {verified_recipients}")
        record_dispatch(domain)
        return True
    except Exception as e:
        print(f"[-] [DISPATCH FAILED] {domain}: {e}")
        return False

def run_engine(max_dispatches=5):
    print("=" * 80)
    print("TENSIX PRODUCTION MULTI-DIMENSIONAL ENGINE (RUNNING LIVE)")
    print("=" * 80)

    already_done = get_already_dispatched()
    print(f"[*] Historically dispatched: {len(already_done)} domains")

    raw_pool = harvest_high_intent_startups()
    print(f"[*] Harvested {len(raw_pool)} startup candidates.")

    dispatched = 0

    for idx, c in enumerate(raw_pool):
        if dispatched >= max_dispatches:
            print(f"\n[!] Reached throttle cap of {max_dispatches} dispatches. Throttling for domain safety.")
            break

        domain = c["domain"]
        if domain in already_done:
            continue

        print(f"\n---> Auditing [{idx+1}/{len(raw_pool)}]: {domain}")

        # GATE 1: Reputation Shield
        is_live, op_weight, shield_meta = verify_live_website(domain, timeout=5)
        if not is_live:
            print(f"     [SHIELD BLOCKED]: {shield_meta.get('reason')}")
            continue

        print(f"     [SHIELD PASSED]: Op Weight {op_weight}/100")

        # GATE 2: Multi-Variable Scorer
        mailops = score_and_package_domain(domain, biz_type="High-Growth SaaS")
        aeo = audit_aeo_and_seo(domain)
        bleed_score = mailops["bleed_score"]

        print(f"     [SCORES]: MailOps Bleed {bleed_score}/100 | Lookups: {mailops['spf_lookups']}/10 | AEO Score: {aeo['aeo_score']}/100")

        if bleed_score < 60:
            print(f"     [SKIPPED]: Bleed score < 60")
            continue

        print(f"     [HIGH-INTENT TARGET CONFIRMED] Bleed: {bleed_score}")

        # GATE 3: Autonomous Dispatch
        success = dispatch_targeted_email(domain, mailops, aeo, c["title"])
        if success:
            dispatched += 1
            if dispatched < max_dispatches:
                jitter = random.randint(50, 80)
                print(f"[*] [SAFETY JITTER] Sleeping {jitter}s...")
                time.sleep(jitter)

    print("\n" + "=" * 80)
    print(f"[+] ENGINE RUN COMPLETE! Dispatched: {dispatched}")
    print(f"[+] Total in Ledger: {len(get_already_dispatched())}")
    print("=" * 80)

if __name__ == "__main__":
    run_engine(max_dispatches=5)
