#!/usr/bin/env python3
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

def run_test():
    config = load_env()
    smtp_login = config.get("BREVO_SMTP_LOGIN")
    smtp_key = config.get("BREVO_SMTP_KEY")
    sender_email = config.get("SENDER_EMAIL", "hemal@tensix.in")
    sender_name = config.get("SENDER_NAME", "Hemal Shah | TENSIX")
    to_email = "hemal.shah2004@gmail.com"

    print(f"[*] Dispatching test email via Brevo SMTP to: {to_email}")
    print(f"[*] From: {sender_name} <{sender_email}>")

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = to_email
    msg["Subject"] = "TENSIX Infrastructure Verification - DKIM/SPF Test"

    text_body = """Hi Hemal,

This is an automated test dispatch from TENSIX Infrastructure.
Testing authenticated delivery through Brevo SMTP with newly synchronized brevo2._domainkey CNAME.

Diagnostic Parameters:
- Sender: hemal@tensix.in
- Selector: brevo2._domainkey
- Expected Verdict: dkim=pass, spf=pass, dmarc=pass

Best regards,
Hemal Shah
tensix.in
"""

    html_body = """<html>
<body>
<h3>TENSIX Infrastructure Verification</h3>
<p>This is an automated test dispatch from TENSIX Infrastructure.<br>
Testing authenticated delivery through Brevo SMTP with newly synchronized <code>brevo2._domainkey</code> CNAME.</p>
<ul>
  <li><b>Sender:</b> hemal@tensix.in</li>
  <li><b>Selector:</b> brevo2._domainkey</li>
  <li><b>Expected Verdict:</b> dkim=pass, spf=pass, dmarc=pass</li>
</ul>
<p>Best regards,<br>
<b>Hemal Shah</b><br>
<a href="https://tensix.in">tensix.in</a></p>
</body>
</html>"""

    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        print("[*] Connecting to smtp-relay.brevo.com:587...")
        server = smtplib.SMTP("smtp-relay.brevo.com", 587)
        server.starttls()
        server.login(smtp_login, smtp_key)
        print("[+] Authenticated with Brevo SMTP.")
        server.sendmail(sender_email, [to_email], msg.as_string())
        server.quit()
        print(f"[+] SUCCESS: Email dispatched to {to_email}!")
    except Exception as e:
        print(f"[-] ERROR: Failed to dispatch: {e}")

if __name__ == "__main__":
    run_test()
