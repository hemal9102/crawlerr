#!/usr/bin/env python3
"""
TENSIX High-Ticket Enterprise Dispatcher: Dubizzle Group (Dubai / UAE)
Bleed Score: 100/100 (16/10 Lookups + Strict p=reject)
Targets: Haider Ali Khan (CEO MENA) & Ovidiu Sabou (CTO)
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

def dispatch_dubizzle():
    config = load_env()
    smtp_login = config.get("BREVO_SMTP_LOGIN")
    smtp_key = config.get("BREVO_SMTP_KEY")
    sender_email = config.get("SENDER_EMAIL", "hemal@tensix.in")
    sender_name = config.get("SENDER_NAME", "Hemal Shah | TENSIX")

    to_email = "haider.khan@dubizzle.com"
    cc_emails = ["ovidiu.sabou@dubizzle.com", "tech@dubizzle.com"]
    subject = "RFC 7208 PermError & p=reject interaction on dubizzle.com sending domain"

    text_body = """Hi Haider and Ovidiu,

I hope this note finds you well.

I am an infrastructure and protocol engineer specializing in RFC transport forensics and agent-readiness standards (tensix.in). While conducting deliverability audits across high-traffic digital platforms in the UAE, I identified a critical DNS configuration failure on dubizzle.com that is actively impacting transactional email placement.

Technical Diagnostic:
Your primary SPF record currently evaluates to 16 recursive DNS lookups, exceeding the RFC 7208 Section 4.6.4 hard ceiling of 10 by 6 lookups:
"v=spf1 include:spf.mandrillapp.com include:_spf.google.com include:dubizzle.zendesk.com include:sendgrid.net include:aspmx.pardot.com include:_spf.salesforce.com include:spf2.esputnik.com include:amazonses.com include:mail.zendesk.com -all"

The Fatal Drop Condition:
Because Dubizzle enforces a strict DMARC policy (p=reject), any receiving Mail Transfer Agent (Google Workspace, Yahoo, Microsoft 365) evaluating unaligned or relaxed relay headers triggers an automatic RFC 7208 PermError on the SPF check. Under p=reject, receiving MTAs are legally instructed to drop and discard user notifications, OTPs, and listing updates rather than routing them to spam.

Remediation Architecture:
We deconstruct the 8 vendor includes (Mandrill, Google, Zendesk, SendGrid, Pardot, Salesforce, eSputnik, Amazon SES) and compile a static, aggregated CIDR network map that condenses your entire lookup footprint down to <= 3 lookups with zero operational downtime.

Commercial Scope ($350 / AED 1,300 Flat Fee):
Our one-time triage and hardening engagement is a flat $350 (or AED 1,300). We deliver the complete validated DNS block, coordinate with your technical team during the record swap, and execute live end-to-end inbox delivery verification across Google and Microsoft within 2 hours.

I have already generated the required DNS mapping. Let me know if you would like me to get this deployed for you today.

Best regards,

Hemal Shah
Systems & RFC Protocol Forensics | TENSIX
https://tensix.in
"""

    html_body = """<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1a1a1a;">
<p>Hi Haider and Ovidiu,</p>

<p>I hope this note finds you well.</p>

<p>I am an infrastructure and protocol engineer specializing in RFC transport forensics and agent-readiness standards (<a href="https://tensix.in" style="color: #2563eb; text-decoration: none;">tensix.in</a>). While conducting deliverability audits across high-traffic digital platforms in the UAE, I identified a critical DNS configuration failure on <strong>dubizzle.com</strong> that is actively impacting transactional email placement.</p>

<h4 style="color: #b91c1c; margin-bottom: 4px;">Technical Diagnostic:</h4>
<p style="margin-top: 0;">Your primary SPF record currently evaluates to <strong>16 recursive DNS lookups</strong>, exceeding the <strong>RFC 7208 Section 4.6.4 hard ceiling of 10 by 6 lookups</strong>:<br>
<code style="background-color: #f4f4f5; padding: 4px 8px; border-radius: 4px; display: inline-block; font-size: 13px;">v=spf1 include:spf.mandrillapp.com include:_spf.google.com include:dubizzle.zendesk.com include:sendgrid.net include:aspmx.pardot.com include:_spf.salesforce.com include:spf2.esputnik.com include:amazonses.com include:mail.zendesk.com -all</code></p>

<h4 style="color: #b91c1c; margin-bottom: 4px;">The Fatal Drop Condition:</h4>
<p style="margin-top: 0;">Because Dubizzle enforces a strict DMARC policy (<code>p=reject</code>), any receiving Mail Transfer Agent (Google Workspace, Yahoo, Microsoft 365) evaluating unaligned or relaxed relay headers triggers an automatic RFC 7208 <strong>PermError</strong> on the SPF check. Under <code>p=reject</code>, receiving MTAs are legally instructed to drop and discard user notifications, OTPs, and listing updates rather than routing them to spam.</p>

<h4 style="color: #0f172a; margin-bottom: 4px;">Remediation Architecture:</h4>
<p style="margin-top: 0;">We deconstruct the 8 vendor includes (Mandrill, Google, Zendesk, SendGrid, Pardot, Salesforce, eSputnik, Amazon SES) and compile a static, aggregated CIDR network map that condenses your entire lookup footprint down to &lt;= 3 lookups with zero operational downtime.</p>

<div style="background-color: #f8fafc; border-left: 4px solid #2563eb; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0; font-weight: 600; color: #0f172a;">Commercial Scope ($350 / AED 1,300 Flat Fee):</p>
  <p style="margin: 4px 0 0 0; font-size: 14px; color: #475569;">Our one-time triage engagement is a flat <strong>$350</strong> (or AED 1,300). We deliver the complete validated DNS block, coordinate with your technical team during the record swap, and execute live end-to-end inbox delivery verification across Google and Microsoft within 2 hours.</p>
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
    msg["Cc"] = ", ".join(cc_emails)
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
        print(f"[+] [DUBIZZLE DISPATCH SUCCESS] {all_recipients}")
        return True
    except Exception as e:
        print(f"[-] [DUBIZZLE DISPATCH FAILED]: {e}")
        return False

if __name__ == "__main__":
    dispatch_dubizzle()
