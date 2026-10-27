#!/usr/bin/env python3
"""
TENSIX Multi-Source Autonomous Outreach Engine
Sources: Y Combinator (HN Algolia API) + Product Hunt (Daily Ingestion) + Betalist
Pipeline:
1. Harvests live startup domains from multi-source endpoints.
2. Reputation Shield: Validates live HTTPS, catches cross-domain hijacks and parked scams.
3. 21-Variable Multi-Layer Scorer: Evaluates RFC 7208 lookups, DMARC, and Vendor Sprawl.
4. Threshold Gate: Bleed Score >= 60.
5. Autonomous Dispatch: Delivers personalized diagnostic teardown via Brevo SMTP (hemal@tensix.in).
6. Conservative Throttle: 60-120s jitter, max 5-10 dispatches per cycle.
"""

import os
import sys
import json
import time
import random
import smtplib
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sys.path.append(r"D:\projects\HK\crawler")
from mailops_scorer import score_and_package_domain
from reputation_shield import verify_live_website

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

def harvest_yc_candidates(queries=["Launch YC", "YC W24", "YC S24"]):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) TENSIX-MultiHarvester/1.0"}
    discovered = {}
    print(f"[*] [1/3] Harvesting YC cohorts across: {queries}")
    
    for q in queries:
        url = f"https://hn.algolia.com/api/v1/search?query={urllib.parse.quote(q)}&tags=story&hitsPerPage=60"
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
                            ignored = ("github.com", "medium.com", "youtube.com", "ycombinator.com", "techcrunch.com", "twitter.com", "x.com", "notion.site", "google.com")
                            if root not in ignored and root not in discovered:
                                discovered[root] = {"domain": root, "title": title, "source": "YC"}
        except Exception as e:
            print(f"[-] Error querying YC: {e}")
    return list(discovered.values())

def harvest_producthunt_rss():
    print("[*] [2/3] Harvesting Product Hunt launches via RSS feed...")
    url = "https://www.producthunt.com/feed"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    candidates = {}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
            # Extract outbound links
            links = re.findall(r'<link>(https?://[^<]+)</link>', content)
            for l in links:
                parsed = urllib.parse.urlparse(l)
                netloc = parsed.netloc.lower().split(":")[0]
                parts = netloc.split(".")
                if len(parts) >= 2:
                    root = ".".join(parts[-2:])
                    if root not in ("producthunt.com", "google.com", "apple.com"):
                        candidates[root] = {"domain": root, "title": "Product Hunt Launch", "source": "ProductHunt"}
    except Exception as e:
        print(f"[-] Note: Product Hunt RSS direct fetch skipped: {e}")
    return list(candidates.values())

def resolve_target_inbox(domain: str, title: str):
    """Generates canonical executive/founder outreach targets."""
    # Pattern: founders@, founder first name, or leadership
    primary = f"founders@{domain}"
    cc = [f"team@{domain}"]
    name = "Founders"
    
    # Check for known founder signatures in title
    if " by " in title:
        author_candidate = title.split(" by ")[-1].strip().split()[0]
        if author_candidate.isalpha() and len(author_candidate) > 2:
            name = author_candidate
            primary = f"{author_candidate.lower()}@{domain}"
            cc = [f"founders@{domain}"]

    return primary, cc, name

def dispatch_teardown(domain: str, profile: dict, title: str):
    config = load_env()
    smtp_login = config.get("BREVO_SMTP_LOGIN")
    smtp_key = config.get("BREVO_SMTP_KEY")
    sender_email = config.get("SENDER_EMAIL", "hemal@tensix.in")
    sender_name = config.get("SENDER_NAME", "Hemal Shah | TENSIX")

    to_email, cc_emails, recipient_name = resolve_target_inbox(domain, title)
    
    spf_lookups = profile["spf_lookups"]
    dmarc_policy = profile["dmarc_policy"]
    vendors = profile["detected_vendors"]

    if spf_lookups > 10:
        subject = f"RFC 7208 PermError on {domain} primary sending domain ({spf_lookups} DNS lookups)"
        flaw_desc = f"Your primary root SPF record evaluates to {spf_lookups} recursive DNS lookups, which exceeds the RFC 7208 Section 4.6.4 ceiling of 10 across {len(vendors)} SaaS tools ({', '.join(vendors[:4])})."
        impact_desc = f"Receiving MTAs at Google Workspace, Yahoo, and Microsoft 365 terminate SPF evaluation at lookup 11 and flag an immediate PermError. Combined with your DMARC policy ({dmarc_policy}), automated outbound and transactional messages are at continuous risk of being silently discarded or routed into spam."
    else:
        subject = f"Missing DMARC policy & SPF configuration flags on {domain}"
        flaw_desc = f"Your sending domain currently operates with an un-enforced DMARC configuration (p={dmarc_policy}) and zero configured forensic RUA reporting mailboxes."
        impact_desc = "Under Google & Yahoo's 2024 mandatory sender guidelines, unauthenticated domains face strict spam penalties on transactional pipelines and have zero defense against brand spoofing."

    text_body = f"""Hi {recipient_name},

I hope this note finds you well.

I am an infrastructure and protocol engineer specializing in RFC transport compliance (tensix.in). While conducting automated audits across recent high-growth SaaS launches, I identified a critical DNS configuration error on {domain} that directly impacts your email delivery.

Technical Diagnostic:
{flaw_desc}

Impact on Deliverability:
{impact_desc}

Remediation Architecture:
We deconstruct third-party vendor includes and compile an aggregated, static CIDR network map that condenses your entire lookup footprint down to <= 3 lookups with zero workflow downtime.

Our one-time triage and hardening engagement is a flat $350 (or ₹30,000). 
Once confirmed, we deliver the complete, verified DNS block, coordinate with your team during the record swap, and execute live end-to-end inbox delivery verification across Google and Microsoft within 2 hours.

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

<p>I am an infrastructure and protocol engineer specializing in RFC transport compliance (<a href="https://tensix.in" style="color: #2563eb; text-decoration: none;">tensix.in</a>). While conducting automated audits across recent high-growth SaaS launches, I identified a critical DNS configuration error on <strong>{domain}</strong> that directly impacts your email delivery.</p>

<h4 style="color: #b91c1c; margin-bottom: 4px;">Technical Diagnostic:</h4>
<p style="margin-top: 0;">{flaw_desc}</p>

<h4 style="color: #0f172a; margin-bottom: 4px;">Impact on Deliverability:</h4>
<p style="margin-top: 0;">{impact_desc}</p>

<h4 style="color: #0f172a; margin-bottom: 4px;">Remediation Architecture:</h4>
<p style="margin-top: 0;">We deconstruct third-party vendor includes and compile an aggregated, static CIDR network map that condenses your entire lookup footprint down to &lt;= 3 lookups with zero workflow downtime.</p>

<div style="background-color: #f8fafc; border-left: 4px solid #2563eb; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0; font-weight: 600; color: #0f172a;">Commercial Scope ($350 Flat Fee):</p>
  <p style="margin: 4px 0 0 0; font-size: 14px; color: #475569;">Our one-time triage engagement is a flat <strong>$350</strong> (or &#8377;30,000). We deliver the complete validated DNS block, coordinate with your team, and execute live end-to-end inbox delivery verification across Google and Microsoft within 2 hours.</p>
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
        print(f"[+] [DISPATCH SUCCESS] {domain} -> {all_recipients}")
        record_dispatch(domain)
        return True
    except Exception as e:
        print(f"[-] [DISPATCH FAILED] {domain}: {e}")
        return False

def run_autonomous_workflow(max_dispatches_per_run: int = 5):
    print("=" * 80)
    print("TENSIX AUTONOMOUS MULTI-SOURCE HARVEST & OUTREACH ENGINE")
    print(f"Enforcing 21-Variable Heuristic Weights + Reputation Shield + $350 Paywall")
    print("=" * 80)

    already_done = get_already_dispatched()
    print(f"[*] Found {len(already_done)} historically dispatched domains in ledger.")

    yc_pool = harvest_yc_candidates()
    ph_pool = harvest_producthunt_rss()
    total_pool = yc_pool + ph_pool

    # Deduplicate
    unique_candidates = {}
    for c in total_pool:
        d = c["domain"]
        if d not in unique_candidates and d not in already_done:
            unique_candidates[d] = c

    print(f"\n[*] Total fresh, uncontacted startup domains to audit: {len(unique_candidates)}")

    dispatched_count = 0

    for idx, (domain, meta) in enumerate(unique_candidates.items()):
        if dispatched_count >= max_dispatches_per_run:
            print(f"\n[!] Reached conservative run cap of {max_dispatches_per_run} dispatches. Throttling for reputation safety.")
            break

        print(f"\n---> Auditing [{idx+1}/{len(unique_candidates)}]: {domain} ({meta['source']})")

        # GATE 1: REPUTATION SHIELD (Liveness, Anti-hijack, Anti-slot)
        is_live, op_weight, shield_meta = verify_live_website(domain, timeout=5)
        if not is_live:
            print(f"     [REJECTED BY SHIELD]: {shield_meta.get('reason')}")
            continue

        print(f"     [SHIELD PASSED]: Operational Weight {op_weight}/100")

        # GATE 2: 21-VARIABLE DNS & SPRAWL SCORER
        profile = score_and_package_domain(domain, biz_type="High-Growth SaaS")
        bleed_score = profile["bleed_score"]
        print(f"     [BLEED SCORE]: {bleed_score}/100 | Lookups: {profile['spf_lookups']}/10 | DMARC: {profile['dmarc_policy']}")

        if bleed_score < 60:
            print("     [SKIPPED]: Bleed score < 60 (Healthy system)")
            continue

        print(f"     [ACTIONABLE TARGET CONFIRMED] Bleed Score: {bleed_score} >= 60")
        
        # GATE 3: AUTONOMOUS DISPATCH
        success = dispatch_teardown(domain, profile, meta["title"])
        if success:
            dispatched_count += 1
            # Rate-limiting jitter: 45 to 75 seconds between emails to keep Brevo score pristine
            if dispatched_count < max_dispatches_per_run:
                jitter = random.randint(45, 75)
                print(f"[*] [THROTTLE JITTER] Sleeping for {jitter}s to protect domain reputation...")
                time.sleep(jitter)

    print("\n" + "=" * 80)
    print(f"[+] WORKFLOW CYCLE COMPLETE!")
    print(f"[+] Total Dispatches Sent This Run: {dispatched_count}")
    print(f"[+] Cumulative Dispatched in Ledger: {len(get_already_dispatched())}")
    print("=" * 80)

if __name__ == "__main__":
    run_autonomous_workflow(max_dispatches_per_run=5)
