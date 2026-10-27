#!/usr/bin/env python3
"""
TENSIX Precision Dispatcher to Bindwell (YC W25)
Founder: Navvye Anand (Caltech) & Tyler Rose (Wolfram Research)
Vulnerability: Boilerplate 'email@example.com' in DMARC RUA + missing SPF/DMARC on bindwell.com
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

def dispatch_bindwell():
    config = load_env()
    smtp_login = config.get("BREVO_SMTP_LOGIN")
    smtp_key = config.get("BREVO_SMTP_KEY")
    sender_email = config.get("SENDER_EMAIL", "hemal@tensix.in")
    sender_name = config.get("SENDER_NAME", "Hemal Shah | TENSIX")

    to_email = "founders@bindwell.ai"
    cc_emails = ["navvye@bindwell.com", "tyler@bindwell.com"]
    subject = "Configuration flag: Placeholder RUA address on bindwell.ai & missing DMARC on bindwell.com"

    text_body = """Hi Navvye and Tyler,

I hope you are both doing well and congrats on the YC W25 launch with Bindwell.

I am an infrastructure and protocol engineer specializing in RFC transport compliance (tensix.in). While running automated infrastructure audits across recent YC cohorts, I noticed two configuration issues across your dual-domain setup:

1. Placeholder RUA Mailbox on bindwell.ai:
Your current DMARC record on _dmarc.bindwell.ai contains boilerplate placeholder addresses:
"v=DMARC1;p=none;sp=none;pct=100;rua=mailto:email@example.com;ruf=mailto:email@example.com;ri=86400;aspf=s;adkim=s;fo=1"
Receiving MTAs (Google Workspace, Yahoo) are routing aggregate failure telemetry to example.com, leaving you completely blind to authentication failures and domain spoofing.

2. Zero Protection on Primary bindwell.com:
Your apex web destination bindwell.com currently has no published SPF or DMARC records in DNS. Under Google's 2024 Sender Guidelines, any outbound communication originating from or aliased to @bindwell.com faces aggressive quarantine and spam penalties.

Remediation:
We can establish unified cross-domain SPF/DMARC alignment across both domains with active forensic telemetry in less than an hour so your enterprise communications remain 100% authenticated.

Best regards,

Hemal Shah
Systems & RFC Protocol Forensics | TENSIX
https://tensix.in
"""

    html_body = """<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1a1a1a;">
<p>Hi Navvye and Tyler,</p>

<p>I hope you are both doing well and congrats on the YC W25 launch with Bindwell.</p>

<p>I am an infrastructure and protocol engineer specializing in RFC transport compliance (<a href="https://tensix.in" style="color: #2563eb; text-decoration: none;">tensix.in</a>). While running automated infrastructure audits across recent YC cohorts, I noticed two configuration issues across your dual-domain setup:</p>

<h4 style="color: #b91c1c; margin-bottom: 4px;">1. Placeholder RUA Mailbox on bindwell.ai:</h4>
<p style="margin-top: 0;">Your current DMARC record on <code>_dmarc.bindwell.ai</code> contains boilerplate placeholder addresses:<br>
<code style="background-color: #f4f4f5; padding: 4px 8px; border-radius: 4px; display: inline-block; font-size: 13px;">v=DMARC1;p=none;sp=none;pct=100;rua=mailto:email@example.com;ruf=mailto:email@example.com;ri=86400;aspf=s;adkim=s;fo=1</code><br>
Receiving MTAs (Google Workspace, Yahoo) are routing aggregate failure telemetry to <em>example.com</em>, leaving you completely blind to authentication failures and domain spoofing.</p>

<h4 style="color: #b91c1c; margin-bottom: 4px;">2. Zero Protection on Primary bindwell.com:</h4>
<p style="margin-top: 0;">Your apex web destination <strong>bindwell.com</strong> currently has no published SPF or DMARC records in DNS. Under Google's 2024 Sender Guidelines, any outbound communication originating from or aliased to @bindwell.com faces aggressive quarantine and spam penalties.</p>

<h4 style="color: #0f172a; margin-bottom: 4px;">Remediation:</h4>
<p style="margin-top: 0;">We can establish unified cross-domain SPF/DMARC alignment across both domains with active forensic telemetry in less than an hour so your enterprise communications remain 100% authenticated.</p>

<p>Best regards,</p>

<p><strong>Hemal Shah</strong><br>
Systems & RFC Protocol Forensics | <a href="https://tensix.in" style="color: #2563eb; text-decoration: none;">TENSIX</a></p>
</body>
</html>"""

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = to_email
    msg["Cc"] = ", ".join(cc_emails)
    msg["Subject"] = subject

    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    all_recipients = [to_email] + cc_emails

    try:
        print(f"[*] Connecting to smtp-relay.brevo.com:587...")
        server = smtplib.SMTP("smtp-relay.brevo.com", 587)
        server.starttls()
        server.login(smtp_login, smtp_key)
        server.sendmail(sender_email, all_recipients, msg.as_string())
        server.quit()
        print(f"[+] SUCCESS: Dispatched to {all_recipients}!")
        return True
    except Exception as e:
        print(f"[-] ERROR: {e}")
        return False

if __name__ == "__main__":
    dispatch_bindwell()
