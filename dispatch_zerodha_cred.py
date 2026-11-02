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

targets = [
    {
        "name": "Kailash",
        "email": "kailash@zerodha.com",
        "company": "Zerodha",
        "subject": "Zerodha Kite order datapath / zero-dependency systems & engineering challenge",
        "observation": "Tracking Zerodha's engineering culture around lean, zero-dependency FOSS architectures handling multi-million streaming market ticks across Kite.",
        "pitch": "I authored the IETF agent readiness draft (draft-shah-agent-readiness-evaluation-00) and engineer low-level networking primitives, zero-copy buffer eviction, and custom socket engines in Rust and Go (github.com/hemal9102/network-inceptor, tensix.in).\n\nI'd love to take on an engineering take-home or backlog challenge on your streaming market-data ingress or order datapath with strict latency, throughput, and zero-allocation benchmarks.",
        "pitch_html": "I authored the IETF agent readiness draft (<a href=\"https://datatracker.ietf.org/doc/draft-shah-agent-readiness-evaluation-00/\">draft-shah-agent-readiness-evaluation-00</a>) and engineer low-level networking primitives, zero-copy buffer eviction, and custom socket engines in Rust and Go (<a href=\"https://github.com/hemal9102/network-inceptor\">github.com/hemal9102/network-inceptor</a>, <a href=\"https://tensix.in\">tensix.in</a>).<br><br>I'd love to take on an engineering take-home or backlog challenge on your streaming market-data ingress or order datapath with strict latency, throughput, and zero-allocation benchmarks."
    },
    {
        "name": "Kunal",
        "email": "kunal@cred.club",
        "company": "CRED",
        "subject": "CRED high-concurrency event telemetry & systems infrastructure challenge",
        "observation": "Tracking CRED's platform scale as your backend processes massive high-concurrency transaction bursts and real-time ledger telemetry during peak settlement windows.",
        "pitch": "I authored the IETF agent readiness draft (draft-shah-agent-readiness-evaluation-00) and engineer high-throughput socket engines, zero-copy buffer pools, and distributed networking pipelines in Rust and Go (github.com/hemal9102/network-inceptor, tensix.in).\n\nI'd love to take on an engineering take-home or backlog trial on your transaction telemetry or high-throughput event ingress with strict resilience and latency SLAs.",
        "pitch_html": "I authored the IETF agent readiness draft (<a href=\"https://datatracker.ietf.org/doc/draft-shah-agent-readiness-evaluation-00/\">draft-shah-agent-readiness-evaluation-00</a>) and engineer high-throughput socket engines, zero-copy buffer pools, and distributed networking pipelines in Rust and Go (<a href=\"https://github.com/hemal9102/network-inceptor\">github.com/hemal9102/network-inceptor</a>, <a href=\"https://tensix.in\">tensix.in</a>).<br><br>I'd love to take on an engineering take-home or backlog trial on your transaction telemetry or high-throughput event ingress with strict resilience and latency SLAs."
    },
    {
        "name": "CRED Talent Team",
        "email": "talent@cred.club",
        "company": "CRED",
        "subject": "Systems & Platform Engineering Take-Home Challenge (Hemal Shah)",
        "observation": "Reaching out regarding CRED's infrastructure and cloud security systems roles.",
        "pitch": "I authored the IETF agent readiness draft (draft-shah-agent-readiness-evaluation-00) and build low-level networking engines, socket multiplexers, and distributed telemetry primitives in Rust and Go (github.com/hemal9102/network-inceptor, tensix.in).\n\nRather than standard screening, I would like to solve a practical 4-hour take-home challenge or backlog issue on your platform/telemetry infrastructure evaluated against strict performance benchmarks.",
        "pitch_html": "I authored the IETF agent readiness draft (<a href=\"https://datatracker.ietf.org/doc/draft-shah-agent-readiness-evaluation-00/\">draft-shah-agent-readiness-evaluation-00</a>) and build low-level networking engines, socket multiplexers, and distributed telemetry primitives in Rust and Go (<a href=\"https://github.com/hemal9102/network-inceptor\">github.com/hemal9102/network-inceptor</a>, <a href=\"https://tensix.in\">tensix.in</a>).<br><br>Rather than standard screening, I would like to solve a practical 4-hour take-home challenge or backlog issue on your platform/telemetry infrastructure evaluated against strict performance benchmarks."
    }
]

print("=== Dispatching Systems Pitches to Kailash Nadh (Zerodha) & Kunal Shah / Talent (CRED) ===")

for t in targets:
    recipient = t["email"]
    subject = t["subject"]

    text_body = f"""Hi {t['name']},

{t['observation']}

{t['pitch']}

Would you be open to assigning a challenge or pointing me toward a backlog issue?

Best,
Hemal Shah
hemal@tensix.in | github.com/hemal9102 | tensix.in
"""

    html_body = f"""<p>Hi {t['name']},</p>
<p>{t['observation']}</p>
<p>{t['pitch_html']}</p>
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

    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=15)
        server.starttls()
        server.login(login, key)
        server.sendmail("hemal@tensix.in", [recipient], msg.as_string())
        server.quit()
        print(f"[SUCCESS] 250 OK Delivered -> {t['name']} ({recipient}) | {t['company']}")
    except Exception as e:
        print(f"[ERROR] Failed to send to {recipient}: {e}")
