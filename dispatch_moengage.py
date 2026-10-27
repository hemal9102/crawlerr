#!/usr/bin/env python3
import sys
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sys.path.append(r"D:\projects\HK\crawler")
from run_production_engine import load_env, record_dispatch

def dispatch_moengage():
    config = load_env()
    smtp_login = config.get("BREVO_SMTP_LOGIN")
    smtp_key = config.get("BREVO_SMTP_KEY")
    sender_email = config.get("SENDER_EMAIL", "hemal@tensix.in")
    sender_name = config.get("SENDER_NAME", "Hemal Shah | TENSIX")

    to_email = "raviteja@moengage.com"
    cc_emails = ["founders@moengage.com"]
    all_recipients = [to_email] + cc_emails

    subject = "moengage.com is silently losing enterprise sales & proposals at the M365 boundary"

    diagnostic_text = (
        "Your primary SPF record cascades through 19 recursive DNS lookups across Zendesk, Google, HubSpot, and Mandrill, "
        "violating RFC 7208 Section 4.6.4 (10-lookup ceiling). Because your DMARC policy is set to strict p=reject, "
        "enterprise security gateways at Fortune 500 prospects evaluate this as a fatal PermError and silently discard outbound "
        "contract links, sales proposals, and executive correspondence. Because this occurs non-deterministically based on "
        "receiver DNS caching, your enterprise sales reps never get a bounce notification—the buyer simply never receives the email."
    )

    commercial_hook = (
        "Stripping vendor includes blindly will break whichever customer engagement or CRM pipeline is tied to it. "
        "We re-architect transport architectures for scaling tech companies, compiling dynamic CIDR network maps "
        "that condense lookup footprints down to <= 2 without dropping active SaaS webhooks."
    )

    text_body = f"""Hi Raviteja,

You have a critical revenue leak occurring at the mail transport boundary of moengage.com.

Technical Root Cause:
{diagnostic_text}

Revenue & Pipeline Impact:
{commercial_hook}

If you want to plug this pipeline bleed before this month's close, let me know and we can review the transport architecture.

Best regards,

Hemal Shah
Infrastructure & MailOps | TENSIX
https://tensix.in
"""

    html_body = f"""<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b;">
<p>Hi Raviteja,</p>

<p>You have a critical revenue leak occurring at the mail transport boundary of <strong>moengage.com</strong>.</p>

<div style="background-color: #f8fafc; border-left: 4px solid #dc2626; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0; font-weight: 600; color: #991b1b;">Technical Root Cause:</p>
  <p style="margin: 4px 0 0 0; font-size: 14px; color: #334155;">{diagnostic_text}</p>
</div>

<div style="background-color: #f0fdf4; border-left: 4px solid #16a34a; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0; font-weight: 600; color: #166534;">Revenue &amp; Pipeline Impact:</p>
  <p style="margin: 4px 0 0 0; font-size: 14px; color: #334155;">{commercial_hook}</p>
</div>

<p>If you want to plug this pipeline bleed before this month's close, let me know and we can review the transport architecture.</p>

<p>Best regards,</p>

<p><strong>Hemal Shah</strong><br>
Infrastructure &amp; MailOps | <a href="https://tensix.in" style="color: #2563eb; text-decoration: none; font-weight: 500;">TENSIX</a></p>
</body>
</html>"""

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = to_email
    msg["Cc"] = ", ".join(cc_emails)
    msg["Subject"] = subject
    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        server = smtplib.SMTP("smtp-relay.brevo.com", 587)
        server.starttls()
        server.login(smtp_login, smtp_key)
        server.sendmail(sender_email, all_recipients, msg.as_string())
        server.quit()

        record_dispatch("moengage.com")
        print(f"[+] [SUCCESS] Dispatched to Raviteja Dodda (MoEngage): {all_recipients}")
        return True
    except Exception as e:
        print(f"[-] [FAILED] {e}")
        return False

if __name__ == "__main__":
    dispatch_moengage()
