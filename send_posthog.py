import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import dotenv_values

cfg = dotenv_values(r'D:\projects\emaillinggggggg\.env')
login = cfg.get('BREVO_SMTP_LOGIN')
key = cfg.get('BREVO_SMTP_KEY')
smtp_server = 'smtp-relay.brevo.com'
smtp_port = 587

recipient = "tim@glsr.nl"
subject = "PostHog ClickHouse ingestion datapath / socket telemetry & SuperDay challenge"

text_content = """Hi Tim,

Tracking PostHog's scale as your ClickHouse clusters ingest billions of analytics events and MCP queries daily across multi-tenant deployments.

I authored the IETF agent readiness draft (draft-shah-agent-readiness-evaluation-00) and engineer low-level network engines, zero-copy buffer eviction, and custom socket parsers in Rust and Go (github.com/hemal9102/network-inceptor, tensix.in).

I'd love to take on PostHog's engineering SuperDay / work-trial challenge for your ClickHouse operations or platform ingestion layer with strict latency, throughput, and memory benchmarks.

Would you be open to assigning a challenge or pointing me toward a backlog issue?

Best,
Hemal Shah
hemal@tensix.in | github.com/hemal9102 | tensix.in
"""

html_content = """<p>Hi Tim,</p>
<p>Tracking PostHog's scale as your ClickHouse clusters ingest billions of analytics events and MCP queries daily across multi-tenant deployments.</p>
<p>I authored the IETF agent readiness draft (<a href="https://datatracker.ietf.org/doc/draft-shah-agent-readiness-evaluation-00/">draft-shah-agent-readiness-evaluation-00</a>) and engineer low-level network engines, zero-copy buffer eviction, and custom socket parsers in Rust and Go (<a href="https://github.com/hemal9102/network-inceptor">github.com/hemal9102/network-inceptor</a>, <a href="https://tensix.in">tensix.in</a>).</p>
<p>I'd love to take on PostHog's engineering SuperDay / work-trial challenge for your ClickHouse operations or platform ingestion layer with strict latency, throughput, and memory benchmarks.</p>
<p>Would you be open to assigning a challenge or pointing me toward a backlog issue?</p>
<p>Best,<br>
Hemal Shah<br>
<a href="mailto:hemal@tensix.in">hemal@tensix.in</a> | <a href="https://github.com/hemal9102">github.com/hemal9102</a> | <a href="https://tensix.in">tensix.in</a></p>
"""

msg = MIMEMultipart("alternative")
msg["Subject"] = subject
msg["From"] = "Hemal Shah <hemal@tensix.in>"
msg["To"] = recipient
msg["Reply-To"] = "hemal@tensix.in"

msg.attach(MIMEText(text_content, "plain", "utf-8"))
msg.attach(MIMEText(html_content, "html", "utf-8"))

try:
    with smtplib.SMTP(smtp_server, smtp_port, timeout=15) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(login, key)
        server.sendmail("hemal@tensix.in", [recipient], msg.as_string())
        print(f"SUCCESS: Delivered pitch to PostHog CTO (Tim Glaser -> {recipient})")
except Exception as e:
    print(f"FAILED: {e}")
