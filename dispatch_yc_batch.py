#!/usr/bin/env python3
"""
TENSIX Automated Batch Dispatcher for High-Priority YC Targets
Dispatches personalized RFC 7208 / DMARC diagnostic teardowns to verified founders.
"""

import os
import sys
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

def dispatch_email(to_email: str, recipient_name: str, subject: str, text_body: str, html_body: str, cc_emails: list = None):
    config = load_env()
    smtp_login = config.get("BREVO_SMTP_LOGIN")
    smtp_key = config.get("BREVO_SMTP_KEY")
    sender_email = config.get("SENDER_EMAIL", "hemal@tensix.in")
    sender_name = config.get("SENDER_NAME", "Hemal Shah | TENSIX")

    if not smtp_key:
        print("[-] Error: BREVO_SMTP_KEY is missing from D:\\projects\\HK\\.env")
        return False

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = to_email
    if cc_emails:
        msg["Cc"] = ", ".join(cc_emails)
    msg["Subject"] = subject

    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    all_recipients = [to_email] + (cc_emails if cc_emails else [])

    try:
        server = smtplib.SMTP("smtp-relay.brevo.com", 587)
        server.starttls()
        server.login(smtp_login, smtp_key)
        server.sendmail(sender_email, all_recipients, msg.as_string())
        server.quit()
        print(f"[+] SUCCESS: Dispatched to {all_recipients} | Subject: '{subject}'")
        return True
    except Exception as e:
        print(f"[-] ERROR dispatching to {to_email}: {e}")
        return False

# Target Roster (Real YC & High-Bleed Startups)
TARGETS = [
    {
        "domain": "sketchdeck.com",
        "to": "chris@sketchdeck.com",
        "name": "Chris Finneral",
        "cc": [],
        "subject": "RFC 7208 PermError on sketchdeck.com primary sending domain (14 DNS lookups)",
        "flaw": "Your primary SPF evaluates to 14 recursive DNS lookups (exceeding the RFC 7208 Section 4.6.4 ceiling of 10) across Zendesk, Mandrill, Mailgun, HubSpot, and Google.",
        "impact": "Exceeding 10 lookups invalidates SPF evaluation with an automatic PermError. Because DMARC is un-enforced (p=none), receiving MTAs at Google and Yahoo are increasingly routing outbound client proposals and notifications into spam.",
        "remediation": "We can aggregate and flatten the 5 vendor ranges down into a static CIDR block (<=3 lookups) and configure strict DMARC protection without disrupting your design workflows."
    },
    {
        "domain": "swishjam.com",
        "to": "collin@swishjam.com",
        "name": "Collin Schneider & Zach Zimbler",
        "cc": ["zach@swishjam.com", "founders@swishjam.com"],
        "subject": "Missing DMARC policy & SPF configuration flags on swishjam.com",
        "flaw": "During an infrastructure scan of YC W23 cohorts, swishjam.com showed zero DMARC records (_dmarc.swishjam.com is completely missing).",
        "impact": "Under Google & Yahoo's mandatory sender guidelines enacted in 2024, sending domains without explicit DMARC records and authenticated return paths face strict spam placement penalties and zero defense against unauthorized domain spoofing.",
        "remediation": "We can establish clean SPF and deploy an authenticated DMARC policy with automated aggregate forensic reporting (RUA) today to ensure 100% primary inbox delivery."
    },
    {
        "domain": "zenfetch.com",
        "to": "gabe@zenfetch.com",
        "name": "Gabe Villasana & Akash Mandavilli",
        "cc": ["akash@zenfetch.com"],
        "subject": "Critical: Missing DMARC record on zenfetch.com primary domain",
        "flaw": "Your sending domain has zero configured DMARC records in DNS (_dmarc.zenfetch.com returns NXDOMAIN).",
        "impact": "Unauthenticated sending domains are now flagged as high-risk by major consumer and enterprise MTAs, causing onboarding verifications and transactional alerts to land in junk folders.",
        "remediation": "We can publish a verified DMARC policy with forensic telemetry monitoring to guarantee uninterrupted inbox delivery for your user onboarding."
    },
    {
        "domain": "tobikodata.com",
        "to": "tyson@tobikodata.com",
        "name": "Tyson Mao & Toby Mao",
        "cc": ["toby@tobikodata.com"],
        "subject": "DMARC authentication & visibility gaps on tobikodata.com",
        "flaw": "Your primary domain runs a passive DMARC policy (p=none) with zero configured forensic RUA reporting mailboxes.",
        "impact": "Running p=none without aggregate reporting leaves you blind to third-party spoofing and provides no active protection against authentication failures on outbound transactional pipes.",
        "remediation": "We can audit your sending endpoints (SQLMesh telemetry / notifications) and transition tobikodata.com to strict quarantine/reject alignment safely."
    }
]

def run_batch():
    print("=" * 70)
    print("TENSIX AUTOMATED FOUNDER DISPATCH: TOP YC BATCH TARGETS")
    print("=" * 70)

    for idx, t in enumerate(TARGETS):
        print(f"\n[*] Processing [{idx+1}/{len(TARGETS)}]: {t['domain']} -> {t['to']}")
        
        text_body = f"""Hi {t['name']},

I hope this note finds you well.

I am an infrastructure and protocol engineer specializing in RFC transport forensics and agent-readiness standards (tensix.in). While conducting technical audits across recent YC and high-growth B2B infrastructure, I identified a critical DNS configuration error on {t['domain']} that directly impacts your email delivery.

Technical Diagnostic:
{t['flaw']}

Impact on Deliverability:
{t['impact']}

Remediation:
{t['remediation']}

I have already generated the required DNS mappings and would be glad to share them with your engineering team to bring {t['domain']} into strict compliance today.

Best regards,

Hemal Shah
Systems & RFC Protocol Forensics | TENSIX
https://tensix.in
Author, IETF draft-shah-agent-readiness-evaluation
"""

        html_body = f"""<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1a1a1a;">
<p>Hi {t['name']},</p>

<p>I hope this note finds you well.</p>

<p>I am an infrastructure and protocol engineer specializing in RFC transport forensics and agent-readiness standards (<a href="https://tensix.in" style="color: #2563eb; text-decoration: none;">tensix.in</a>). While conducting technical audits across recent YC and high-growth B2B infrastructure, I identified a critical DNS configuration error on <strong>{t['domain']}</strong> that directly impacts your email delivery.</p>

<h4 style="color: #b91c1c; margin-bottom: 4px;">Technical Diagnostic:</h4>
<p style="margin-top: 0;">{t['flaw']}</p>

<h4 style="color: #0f172a; margin-bottom: 4px;">Impact on Deliverability:</h4>
<p style="margin-top: 0;">{t['impact']}</p>

<h4 style="color: #0f172a; margin-bottom: 4px;">Remediation:</h4>
<p style="margin-top: 0;">{t['remediation']}</p>

<p>I have already generated the required DNS mappings and would be glad to share them with your engineering team to bring <strong>{t['domain']}</strong> into strict compliance today.</p>

<p>Best regards,</p>

<p><strong>Hemal Shah</strong><br>
Systems & RFC Protocol Forensics | <a href="https://tensix.in" style="color: #2563eb; text-decoration: none;">TENSIX</a><br>
<span style="font-size: 13px; color: #64748b;">Author, IETF draft-shah-agent-readiness-evaluation</span></p>
</body>
</html>"""

        success = dispatch_email(
            to_email=t["to"],
            recipient_name=t["name"],
            subject=t["subject"],
            text_body=text_body,
            html_body=html_body,
            cc_emails=t["cc"]
        )

        time.sleep(2)  # Polite pause between SMTP sessions

    print("\n" + "=" * 70)
    print("[+] BATCH DISPATCH COMPLETE!")
    print("=" * 70)

if __name__ == "__main__":
    run_batch()
