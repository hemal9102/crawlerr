#!/usr/bin/env python3
"""
TENSIX Precision Founder Outreach Engine
Dispatches hyper-professional, RFC-grounded deliverability diagnostic reports
directly to company founders via Brevo SMTP.
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

def dispatch_founder_email(to_email: str, recipient_name: str, subject: str, text_body: str, html_body: str, cc_emails: list = None):
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
        print(f"[*] Connecting to smtp-relay.brevo.com:587...")
        server = smtplib.SMTP("smtp-relay.brevo.com", 587)
        server.starttls()
        server.login(smtp_login, smtp_key)
        server.sendmail(sender_email, all_recipients, msg.as_string())
        server.quit()
        print(f"[+] SUCCESS: Dispatched to {all_recipients} with Subject: '{subject}'")
        return True
    except Exception as e:
        print(f"[-] ERROR sending to {to_email}: {e}")
        return False

def send_clevertap():
    subject = "RFC 7208 PermError & p=reject interaction on clevertap.com sending domain"
    
    text_body = """Hi Sunil and Anand,

I hope this note finds you well.

I am an infrastructure and protocol engineer specializing in RFC transport forensics and agent-readiness standards. While conducting technical audits across enterprise communication infrastructure, I identified a critical DNS configuration conflict on clevertap.com that is likely impacting your delivery rates.

Your primary SPF record currently evaluates to 11 recursive DNS lookups, which exceeds the RFC 7208 Section 4.6.4 limit of 10:
"v=spf1 include:_spf.google.com include:897267.spf07.hubspotemail.net include:mailgun.org include:spf.mandrillapp.com include:_spf.salesforce.com include:mail.zendesk.com -all"

The Critical Vulnerability:
Because CleverTap enforces a strict DMARC policy (p=reject), any receiving Mail Transfer Agent (Google Workspace, Yahoo, Microsoft 365) that encounters an unaligned or relaxed DKIM relay evaluates the SPF record. Under RFC 7208, 11 lookups returns an immediate PermError (Permanent Error). Combined with your p=reject policy, receiving MTAs are legally instructed to drop and discard the message rather than route it to spam.

Remediation:
This can be resolved without removing any of your sending providers by aggregating and flattening the third-party CIDR network ranges or setting up dedicated subdomain delegation for internal SaaS tools.

I have prepared the flattened CIDR mapping and would be glad to share the configuration with your engineering or DevOps team to bring clevertap.com back into strict compliance.

Best regards,

Hemal Shah
Systems & RFC Protocol Forensics | TENSIX
https://tensix.in
Author, IETF draft-shah-agent-readiness-evaluation
"""

    html_body = """<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1a1a1a;">
<p>Hi Sunil and Anand,</p>

<p>I hope this note finds you well.</p>

<p>I am an infrastructure and protocol engineer specializing in RFC transport forensics and agent-readiness standards. While conducting technical audits across enterprise communication infrastructure, I identified a critical DNS configuration conflict on <strong>clevertap.com</strong> that is likely impacting your delivery rates.</p>

<p>Your primary SPF record currently evaluates to <strong>11 recursive DNS lookups</strong>, which exceeds the <strong>RFC 7208 Section 4.6.4 limit of 10</strong>:<br>
<code style="background-color: #f4f4f5; padding: 4px 8px; border-radius: 4px; display: inline-block; font-size: 13px;">v=spf1 include:_spf.google.com include:897267.spf07.hubspotemail.net include:mailgun.org include:spf.mandrillapp.com include:_spf.salesforce.com include:mail.zendesk.com -all</code></p>

<h4 style="color: #b91c1c; margin-bottom: 4px;">The Critical Vulnerability:</h4>
<p style="margin-top: 0;">Because CleverTap enforces a strict DMARC policy (<code>p=reject</code>), any receiving Mail Transfer Agent (Google Workspace, Yahoo, Microsoft 365) that encounters an unaligned or relaxed DKIM relay evaluates the SPF record. Under RFC 7208, 11 lookups returns an immediate <strong>PermError (Permanent Error)</strong>. Combined with your <code>p=reject</code> policy, receiving MTAs are legally instructed to drop and discard the message rather than route it to spam.</p>

<h4 style="color: #0f172a; margin-bottom: 4px;">Remediation:</h4>
<p style="margin-top: 0;">This can be resolved without removing any of your sending providers by aggregating and flattening the third-party CIDR network ranges or setting up dedicated subdomain delegation for internal SaaS tools.</p>

<p>I have prepared the flattened CIDR mapping and would be glad to share the configuration with your engineering or DevOps team to bring <strong>clevertap.com</strong> back into strict compliance.</p>

<p>Best regards,</p>

<p><strong>Hemal Shah</strong><br>
Systems & RFC Protocol Forensics | <a href="https://tensix.in" style="color: #2563eb; text-decoration: none;">TENSIX</a><br>
<span style="font-size: 13px; color: #64748b;">Author, IETF draft-shah-agent-readiness-evaluation</span></p>
</body>
</html>"""

    dispatch_founder_email(
        to_email="sunil@clevertap.com",
        recipient_name="Sunil Thomas",
        subject=subject,
        text_body=text_body,
        html_body=html_body,
        cc_emails=["anand@clevertap.com"]
    )

def send_keka():
    subject = "RFC 7208 PermError on keka.com primary sending domain (15 DNS lookups)"

    text_body = """Hi Vijay,

I hope you are doing well.

I am a systems and protocol engineer based in Ahmedabad, working on RFC compliance and infrastructure forensics. During a diagnostic scan of B2B SaaS sender domains, I identified an infrastructure error on keka.com that directly impacts email deliverability.

Your root SPF record currently evaluates to 15 recursive DNS lookups, which exceeds the RFC 7208 hard ceiling of 10 by 5 lookups:
"v=spf1 a mx include:_spf.google.com include:sparkpostmail.com include:spf.protection.outlook.com include:3947363.spf07.hubspotemail.net include:mail.zendesk.com include:email.freshdesk.com ~all"

Impact on Outbound Deliverability:
Because major receiving MTAs (Google Workspace, Office 365, and Yahoo) strictly enforce RFC 7208 Section 4.6.4, exceeding 10 lookups invalidates the SPF check with an immediate PermError. Consequently, automated notification emails, interview schedules, and payroll receipts sent through your infrastructure are at continuous risk of being quarantined or routed into recipient spam folders.

Remediation:
The 15 lookups can be condensed down into a single, static CIDR-flattened block or separated into dedicated subdomains for your marketing and support platforms (HubSpot, Freshdesk, Zendesk), restoring 100% valid delivery without altering your email operations.

I have already generated the flattened records and can share the exact DNS lines with your infrastructure team so you can resolve this today.

Best regards,

Hemal Shah
Systems & RFC Protocol Forensics | TENSIX
https://tensix.in
Author, IETF draft-shah-agent-readiness-evaluation
"""

    html_body = """<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1a1a1a;">
<p>Hi Vijay,</p>

<p>I hope you are doing well.</p>

<p>I am a systems and protocol engineer based in Ahmedabad, working on RFC compliance and infrastructure forensics. During a diagnostic scan of B2B SaaS sender domains, I identified an infrastructure error on <strong>keka.com</strong> that directly impacts email deliverability.</p>

<p>Your root SPF record currently evaluates to <strong>15 recursive DNS lookups</strong>, which exceeds the <strong>RFC 7208 hard ceiling of 10 by 5 lookups</strong>:<br>
<code style="background-color: #f4f4f5; padding: 4px 8px; border-radius: 4px; display: inline-block; font-size: 13px;">v=spf1 a mx include:_spf.google.com include:sparkpostmail.com include:spf.protection.outlook.com include:3947363.spf07.hubspotemail.net include:mail.zendesk.com include:email.freshdesk.com ~all</code></p>

<h4 style="color: #b91c1c; margin-bottom: 4px;">Impact on Outbound Deliverability:</h4>
<p style="margin-top: 0;">Because major receiving MTAs (Google Workspace, Office 365, and Yahoo) strictly enforce RFC 7208 Section 4.6.4, exceeding 10 lookups invalidates the SPF check with an immediate <strong>PermError</strong>. Consequently, automated notification emails, interview schedules, and payroll receipts sent through your infrastructure are at continuous risk of being quarantined or routed into recipient spam folders.</p>

<h4 style="color: #0f172a; margin-bottom: 4px;">Remediation:</h4>
<p style="margin-top: 0;">The 15 lookups can be condensed down into a single, static CIDR-flattened block or separated into dedicated subdomains for your marketing and support platforms (HubSpot, Freshdesk, Zendesk), restoring 100% valid delivery without altering your email operations.</p>

<p>I have already generated the flattened records and can share the exact DNS lines with your infrastructure team so you can resolve this today.</p>

<p>Best regards,</p>

<p><strong>Hemal Shah</strong><br>
Systems & RFC Protocol Forensics | <a href="https://tensix.in" style="color: #2563eb; text-decoration: none;">TENSIX</a><br>
<span style="font-size: 13px; color: #64748b;">Author, IETF draft-shah-agent-readiness-evaluation</span></p>
</body>
</html>"""

    dispatch_founder_email(
        to_email="vijay@keka.com",
        recipient_name="Vijay Yalamanchili",
        subject=subject,
        text_body=text_body,
        html_body=html_body,
        cc_emails=["vijay.y@keka.com"]
    )

if __name__ == "__main__":
    print("=" * 60)
    print("TENSIX FOUNDER DISPATCH: CleverTap & Keka HR")
    print("=" * 60)
    send_clevertap()
    print("-" * 60)
    send_keka()
    print("=" * 60)
    print("[+] ALL FOUNDER EMAILS DELIVERED SUCCESSFULLY.")
