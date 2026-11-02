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

# Target cohort: Solomon Hykes (Dagger), Vipul Ved Prakash (Together AI), Stas Kelvich (Neon)
pitches = [
    {
        "name": "Solomon",
        "email": "solomon@dagger.io",
        "company": "Dagger",
        "subject": "Dagger programmable engine / OCI container socket graph & systems challenge",
        "observation": "Tracking Dagger's architectural shift running DAG pipelines directly on top of client-side OCI execution graphs and custom BuildKit runtimes.",
        "pitch": "I authored the IETF agent readiness draft (draft-shah-agent-readiness-evaluation-00) and engineer low-level systems in Rust and Go, focusing on zero-copy container IPC, socket multiplexing, and custom network parsers (github.com/hemal9102/network-inceptor, tensix.in).\n\nI'd love to take on a 4-hour take-home challenge or backlog issue on Dagger's engine execution graph or socket bridge under strict concurrency and memory benchmarks.",
        "pitch_html": "I authored the IETF agent readiness draft (<a href=\"https://datatracker.ietf.org/doc/draft-shah-agent-readiness-evaluation-00/\">draft-shah-agent-readiness-evaluation-00</a>) and engineer low-level systems in Rust and Go, focusing on zero-copy container IPC, socket multiplexing, and custom network parsers (<a href=\"https://github.com/hemal9102/network-inceptor\">github.com/hemal9102/network-inceptor</a>, <a href=\"https://tensix.in\">tensix.in</a>).<br><br>I'd love to take on a 4-hour take-home challenge or backlog issue on Dagger's engine execution graph or socket bridge under strict concurrency and memory benchmarks."
    },
    {
        "name": "Vipul",
        "email": "vipul@together.ai",
        "company": "Together AI",
        "subject": "Together AI inference cluster networking / streaming socket telemetry & challenge",
        "observation": "Tracking Together AI's infrastructure scaling low-latency streaming token inference and interconnect throughput across massive distributed GPU clusters.",
        "pitch": "I authored the IETF agent readiness draft (draft-shah-agent-readiness-evaluation-00) and build high-throughput network engines, zero-copy buffer eviction, and custom socket parsers in Rust and Go (github.com/hemal9102/network-inceptor, tensix.in).\n\nI'd love to tackle a systems take-home or backlog challenge on your streaming inference ingress or distributed socket layer with strict p99 latency SLAs.",
        "pitch_html": "I authored the IETF agent readiness draft (<a href=\"https://datatracker.ietf.org/doc/draft-shah-agent-readiness-evaluation-00/\">draft-shah-agent-readiness-evaluation-00</a>) and build high-throughput network engines, zero-copy buffer eviction, and custom socket parsers in Rust and Go (<a href=\"https://github.com/hemal9102/network-inceptor\">github.com/hemal9102/network-inceptor</a>, <a href=\"https://tensix.in\">tensix.in</a>).<br><br>I'd love to tackle a systems take-home or backlog challenge on your streaming inference ingress or distributed socket layer with strict p99 latency SLAs."
    },
    {
        "name": "Stas",
        "email": "stas@neon.tech",
        "company": "Neon",
        "subject": "Neon custom Rust storage engine / page server WAL streaming & systems challenge",
        "observation": "Tracking Neon's architecture decoupling Postgres compute from storage, specifically your Rust-based safekeeper and pageserver WAL ingestion pipeline.",
        "pitch": "I authored the IETF agent readiness draft (draft-shah-agent-readiness-evaluation-00) and build low-level networking primitives, zero-copy buffer pools, and custom socket engines in Rust and Go (github.com/hemal9102/network-inceptor, tensix.in).\n\nI'd love to take on an engineering take-home or backlog challenge for Neon's pageserver or safekeeper WAL streaming datapath against strict latency and throughput benchmarks.",
        "pitch_html": "I authored the IETF agent readiness draft (<a href=\"https://datatracker.ietf.org/doc/draft-shah-agent-readiness-evaluation-00/\">draft-shah-agent-readiness-evaluation-00</a>) and build low-level networking primitives, zero-copy buffer pools, and custom socket engines in Rust and Go (<a href=\"https://github.com/hemal9102/network-inceptor\">github.com/hemal9102/network-inceptor</a>, <a href=\"https://tensix.in\">tensix.in</a>).<br><br>I'd love to take on an engineering take-home or backlog challenge for Neon's pageserver or safekeeper WAL streaming datapath against strict latency and throughput benchmarks."
    }
]

print("=== Dispatching High-Converting Systems Pitches (Dagger, Together AI, Neon) ===")

for p in pitches:
    recipient = p["email"]
    subject = p["subject"]

    text_body = f"""Hi {p['name']},

{p['observation']}

{p['pitch']}

Would you be open to assigning a challenge or pointing me toward a backlog issue?

Best,
Hemal Shah
hemal@tensix.in | github.com/hemal9102 | tensix.in
"""

    html_body = f"""<p>Hi {p['name']},</p>
<p>{p['observation']}</p>
<p>{p['pitch_html']}</p>
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
        print(f"[SUCCESS] 250 OK Delivered -> {p['name']} ({recipient}) | {p['company']}")
    except Exception as e:
        print(f"[ERROR] Failed to send to {recipient}: {e}")
