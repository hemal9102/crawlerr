#!/usr/bin/env python3
"""
TENSIX Automated SMTP Dispatch Engine
Reads bleeding leads and sends forensic RFC diagnostic reports via Brevo SMTP
using credentials stored in D:\\projects\\HK\\.env
"""

import os
import sys
import smtplib
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

def send_forensic_email(to_email: str, recipient_name: str, domain: str, spf_lookups: int, dmarc_policy: str, reasons: list, dry_run: bool = True):
    config = load_env()
    smtp_login = config.get("BREVO_SMTP_LOGIN")
    smtp_key = config.get("BREVO_SMTP_KEY")
    sender_email = config.get("SENDER_EMAIL", "contact@tensix.in")
    sender_name = config.get("SENDER_NAME", "Hemal Shah | TENSIX")

    if not smtp_key and not dry_run:
        print("[-] Error: BREVO_SMTP_KEY is not set in D:\\projects\\HK\\.env!")
        return False

    subject = f"Notice: RFC 7208 PermError on {domain} sending domain ({spf_lookups} SPF Lookups)"
    
    body = f"""Hi {recipient_name},

Quick technical flag regarding {domain}'s primary email infrastructure:

During an automated RFC compliance scan across B2B senders, your root domain triggered an RFC 7208 PermError:
- Evaluated DNS Lookups: {spf_lookups} / 10 hard limit
- Configured DMARC Policy: {dmarc_policy}
- Flags: {', '.join(reasons)}

Under RFC 7208 Section 4.6.4, exceeding 10 lookups invalidates SPF evaluation on major receiving MTAs (Google Workspace, Yahoo, Microsoft 365), causing automated transactional or outbound emails to silently drop or land in spam folders.

I can share the flattened CIDR SPF record mapping to bring {domain} back under strict 10-lookup compliance immediately.

Best regards,
Hemal Shah
Systems & RFC Protocol Forensics | tensix.in
Author, IETF draft-shah-agent-readiness-evaluation
"""

    if dry_run:
        print("=" * 60)
        print(f"[DRY-RUN] To: {to_email}")
        print(f"[DRY-RUN] From: {sender_name} <{sender_email}>")
        print(f"[DRY-RUN] Subject: {subject}")
        print("-" * 60)
        print(body)
        print("=" * 60)
        return True

    msg = MIMEMultipart()
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        print(f"[*] Connecting to smtp-relay.brevo.com:587 for {to_email}...")
        server = smtplib.SMTP("smtp-relay.brevo.com", 587)
        server.starttls()
        server.login(smtp_login, smtp_key)
        server.sendmail(sender_email, [to_email], msg.as_string())
        server.quit()
        print(f"[+] Successfully delivered forensic email to: {to_email}")
        return True
    except Exception as e:
        print(f"[-] Failed to send to {to_email}: {e}")
        return False

if __name__ == "__main__":
    # Test dry run
    send_forensic_email(
        to_email="vijay@keka.com",
        recipient_name="Vijay",
        domain="keka.com",
        spf_lookups=15,
        dmarc_policy="quarantine",
        reasons=["RFC_7208_PERM_ERROR (15 lookups > 10 limit)"],
        dry_run=True
    )
