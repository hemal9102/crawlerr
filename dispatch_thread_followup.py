#!/usr/bin/env python3
"""
TENSIX High-Conversion Thread Follow-Up Dispatcher
Fires targeted closing follow-ups into existing email threads for:
1. Anand Jain & Sunil Thomas (CleverTap)
2. Vijay Yalamanchili (Keka HR)
3. Raviteja Dodda (MoEngage)
4. Team @ SketchDeck

Strictly uses Brevo SMTP with RFC 5321 pre-flight validation.
Zero free technical sauce, pure revenue leak and pipeline closing pressure.
"""

import sys
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sys.path.append(r"D:\projects\HK\crawler")
from run_production_engine import load_env
from smtp_rcpt_verifier import verify_mailbox_rcpt

def send_thread_followup(to_email, cc_emails, subject, text_content, html_content):
    config = load_env()
    smtp_login = config.get("BREVO_SMTP_LOGIN")
    smtp_key = config.get("BREVO_SMTP_KEY")
    sender_email = config.get("SENDER_EMAIL", "hemal@tensix.in")
    sender_name = config.get("SENDER_NAME", "Hemal Shah | TENSIX")

    all_recipients = [to_email] + cc_emails
    verified_recipients = [r for r in all_recipients if verify_mailbox_rcpt(r)]

    if not verified_recipients:
        print(f"[-] [BOUNCE SHIELD] All recipients failed pre-flight verification: {all_recipients}")
        return False

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = to_email
    if cc_emails:
        msg["Cc"] = ", ".join(cc_emails)
    msg["Subject"] = subject
    msg.attach(MIMEText(text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    try:
        server = smtplib.SMTP("smtp-relay.brevo.com", 587)
        server.starttls()
        server.login(smtp_login, smtp_key)
        server.sendmail(sender_email, verified_recipients, msg.as_string())
        server.quit()
        print(f"[+] [SUCCESS] Dispatched thread follow-up to: {verified_recipients}")
        return True
    except Exception as e:
        print(f"[-] [FAILED] {e}")
        return False

def follow_up_clevertap():
    to = "anand@clevertap.com"
    cc = ["sunil@clevertap.com"]
    subject = "Re: RFC 7208 PermError & p=reject interaction on clevertap.com sending domain"
    
    text = """Hi Anand,

Saw you and Sunil were reviewing the delivery note last night.

Here is the bottom-line commercial risk:

Your outbound marketing team has separate routes covered, but your Account Executives are quietly losing high-ACV enterprise deals right at the contract stage. When sales reps send custom pricing, security reviews, and proposals directly from their @clevertap.com corporate inboxes, corporate Microsoft 365 security gateways at enterprise target accounts are dropping the messages before the buyer ever sees them.

Your reps assume the buyer ghosted them after the demo. In reality, the proposal never made it past the recipient's firewall. You're spending tens of thousands acquiring enterprise pipeline, only to drop deals at the final yard.

We specialize in bulletproofing deal-closing infrastructure and high-ticket deliverability for scaling enterprise platforms.

If plugging this deal-closing leak before this month's close is a priority, let's grab a direct 10-minute sync today and I'll walk you through where the pipeline is dropping across your stack.

If this isn't on your radar right now, no worries at all and I'll close the file.

Let me know if 10 minutes works today.

Best regards,

Hemal Shah
Infrastructure & MailOps | TENSIX
https://tensix.in
"""

    html = """<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b;">
<p>Hi Anand,</p>

<p>Saw you and Sunil were reviewing the delivery note last night.</p>

<p>Here is the bottom-line commercial risk:</p>

<p>Your outbound marketing team has separate routes covered, but your Account Executives are quietly losing high-ACV enterprise deals right at the contract stage. When sales reps send custom pricing, security reviews, and proposals directly from their <strong>@clevertap.com</strong> corporate inboxes, corporate Microsoft 365 security gateways at enterprise target accounts are dropping the messages before the buyer ever sees them.</p>

<div style="background-color: #fef2f2; border-left: 4px solid #ef4444; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0; font-weight: 600; color: #991b1b;">The Closing Choke-Point:</p>
  <p style="margin: 4px 0 0 0; font-size: 14px; color: #4b5563;">Your reps assume the buyer ghosted them after the demo. In reality, the proposal never made it past the recipient's firewall. You're spending tens of thousands acquiring enterprise pipeline, only to drop deals at the final yard.</p>
</div>

<p>We specialize in bulletproofing deal-closing infrastructure and high-ticket deliverability for scaling enterprise platforms.</p>

<p>If plugging this deal-closing leak before this month's close is a priority, let's grab a direct 10-minute sync today and I'll walk you through where the pipeline is dropping across your stack.</p>

<p>If this isn't on your radar right now, no worries at all and I'll close the file.</p>

<p>Let me know if 10 minutes works today.</p>

<p>Best regards,</p>

<p><strong>Hemal Shah</strong><br>
Infrastructure &amp; MailOps | <a href="https://tensix.in" style="color: #2563eb; text-decoration: none; font-weight: 500;">TENSIX</a></p>
</body>
</html>"""

    return send_thread_followup(to, cc, subject, text, html)

def follow_up_keka():
    to = "vijay@keka.com"
    cc = ["vijay.y@keka.com"]
    subject = "Re: RFC 7208 PermError on keka.com primary sending domain (15 DNS lookups)"
    
    text = """Hi Vijay,

Saw you checked out our engineering studio at tensix.in yesterday.

The direct business impact on Keka right now:

Your primary sending domain is currently overflowing across 15 vendor lookups. When your enterprise sales reps send payroll proposals, contract renewals, or onboarding links to corporate buyers using strict Microsoft 365 or Google Workspace filters, those emails are silently routed into spam folders or discarded.

Enterprise HR buyers don't check their spam folders for payroll contracts—they simply move to the next vendor.

We re-architect and bulletproof mail transport for scaling SaaS platforms to guarantee 100% executive primary inbox delivery with zero downtime.

If protecting this quarter's enterprise payroll pipeline is a priority, let's do a quick 10-minute sync today.

If your team is already handling this internally, no problem at all and I won't follow up again.

Best regards,

Hemal Shah
Infrastructure & MailOps | TENSIX
https://tensix.in
"""

    html = """<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b;">
<p>Hi Vijay,</p>

<p>Saw you checked out our engineering studio at tensix.in yesterday.</p>

<p>The direct business impact on Keka right now:</p>

<p>Your primary sending domain is currently overflowing across 15 vendor lookups. When your enterprise sales reps send payroll proposals, contract renewals, or onboarding links to corporate buyers using strict Microsoft 365 or Google Workspace filters, those emails are silently routed into spam folders or discarded.</p>

<div style="background-color: #fef2f2; border-left: 4px solid #ef4444; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0; font-weight: 600; color: #991b1b;">The Enterprise Choke-Point:</p>
  <p style="margin: 4px 0 0 0; font-size: 14px; color: #4b5563;">Enterprise HR buyers don't check their spam folders for payroll contracts—they simply move to the next vendor.</p>
</div>

<p>We re-architect and bulletproof mail transport for scaling SaaS platforms to guarantee 100% executive primary inbox delivery with zero downtime.</p>

<p>If protecting this quarter's enterprise payroll pipeline is a priority, let's do a quick 10-minute sync today.</p>

<p>If your team is already handling this internally, no problem at all and I won't follow up again.</p>

<p>Best regards,</p>

<p><strong>Hemal Shah</strong><br>
Infrastructure &amp; MailOps | <a href="https://tensix.in" style="color: #2563eb; text-decoration: none; font-weight: 500;">TENSIX</a></p>
</body>
</html>"""

    return send_thread_followup(to, cc, subject, text, html)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", choices=["clevertap", "keka"], required=True)
    args = parser.parse_args()
    
    if args.target == "clevertap":
        follow_up_clevertap()
    elif args.target == "keka":
        follow_up_keka()
