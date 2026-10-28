#!/usr/bin/env python3
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sys.path.append(r"D:\projects\HK\crawler")
from run_production_engine import load_env

def send_graceful_close():
    config = load_env()
    smtp_login = config.get("BREVO_SMTP_LOGIN")
    smtp_key = config.get("BREVO_SMTP_KEY")
    sender_email = config.get("SENDER_EMAIL", "hemal@tensix.in")
    sender_name = config.get("SENDER_NAME", "Hemal Shah | TENSIX")

    to_email = "anand@clevertap.com"
    subject = "Re: RFC 7208 PermError & p=reject interaction on clevertap.com sending domain"

    text_body = """Understood, Anand. Glad to hear things are running smoothly on your end.

Wishing you and the CleverTap team a great quarter ahead!

Best,

Hemal Shah
Infrastructure & MailOps | TENSIX
https://tensix.in
"""

    html_body = """<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b;">
<p>Understood, Anand. Glad to hear things are running smoothly on your end.</p>

<p>Wishing you and the CleverTap team a great quarter ahead!</p>

<p>Best,</p>

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

    try:
        server = smtplib.SMTP("smtp-relay.brevo.com", 587)
        server.starttls()
        server.login(smtp_login, smtp_key)
        server.sendmail(sender_email, [to_email], msg.as_string())
        server.quit()
        print("[+] Successfully sent graceful sign-off to Anand Jain (CleverTap)")
        return True
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

if __name__ == "__main__":
    send_graceful_close()
