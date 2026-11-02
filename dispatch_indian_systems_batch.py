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
        "name": "Rohit",
        "email": "rohit@acceldata.io",
        "company": "Acceldata",
        "subject": "Acceldata data observability ingestion / pipeline telemetry & systems challenge",
        "observation": "Tracking Acceldata's architecture as you ingest and correlate massive telemetry streams across Kafka, Spark, and hybrid enterprise data lakes.",
        "pitch": "I authored the IETF agent readiness draft (draft-shah-agent-readiness-evaluation-00) and engineer low-level systems in Rust and Go, focusing on zero-copy socket ingestion, event stream backpressure, and high-throughput network engines (github.com/hemal9102/network-inceptor, tensix.in).\n\nI'd love to take on an engineering take-home or backlog trial on your streaming telemetry ingestion layer with strict latency and memory benchmarks.",
        "pitch_html": "I authored the IETF agent readiness draft (<a href=\"https://datatracker.ietf.org/doc/draft-shah-agent-readiness-evaluation-00/\">draft-shah-agent-readiness-evaluation-00</a>) and engineer low-level systems in Rust and Go, focusing on zero-copy socket ingestion, event stream backpressure, and high-throughput network engines (<a href=\"https://github.com/hemal9102/network-inceptor\">github.com/hemal9102/network-inceptor</a>, <a href=\"https://tensix.in\">tensix.in</a>).<br><br>I'd love to take on an engineering take-home or backlog trial on your streaming telemetry ingestion layer with strict latency and memory benchmarks."
    },
    {
        "name": "Uma",
        "email": "uma@chaosnative.com",
        "company": "ChaosNative",
        "subject": "LitmusChaos socket resilience / network fault injection & systems challenge",
        "observation": "Following ChaosNative and LitmusChaos's scale across cloud-native resilience and automated fault injection at the container and network layers.",
        "pitch": "I authored the IETF agent readiness draft (draft-shah-agent-readiness-evaluation-00) and build low-level networking primitives, socket interception engines, and automated resilience runners in Rust and Go (github.com/hemal9102/network-inceptor, tensix.in).\n\nI'd love to take on a 4-hour take-home challenge or backlog issue on your network chaos injection and socket fault engine with rigorous correctness criteria.",
        "pitch_html": "I authored the IETF agent readiness draft (<a href=\"https://datatracker.ietf.org/doc/draft-shah-agent-readiness-evaluation-00/\">draft-shah-agent-readiness-evaluation-00</a>) and build low-level networking primitives, socket interception engines, and automated resilience runners in Rust and Go (<a href=\"https://github.com/hemal9102/network-inceptor\">github.com/hemal9102/network-inceptor</a>, <a href=\"https://tensix.in\">tensix.in</a>).<br><br>I'd love to take on a 4-hour take-home challenge or backlog issue on your network chaos injection and socket fault engine with rigorous correctness criteria."
    },
    {
        "name": "Kedar",
        "email": "kedar@hyperverge.co",
        "company": "HyperVerge",
        "subject": "HyperVerge low-latency edge AI inference sockets & systems challenge",
        "observation": "Tracking HyperVerge's real-time computer vision inference platform processing hundreds of millions of edge transactions with strict latency SLAs.",
        "pitch": "I authored the IETF agent readiness draft (draft-shah-agent-readiness-evaluation-00) and engineer high-throughput socket engines, zero-copy buffer pools, and low-latency concurrency pipelines in Rust and Go (github.com/hemal9102/network-inceptor, tensix.in).\n\nI'd love to take on a practical take-home challenge or backlog task for your edge inference ingress/streaming pipeline evaluated against latency and throughput benchmarks.",
        "pitch_html": "I authored the IETF agent readiness draft (<a href=\"https://datatracker.ietf.org/doc/draft-shah-agent-readiness-evaluation-00/\">draft-shah-agent-readiness-evaluation-00</a>) and engineer high-throughput socket engines, zero-copy buffer pools, and low-latency concurrency pipelines in Rust and Go (<a href=\"https://github.com/hemal9102/network-inceptor\">github.com/hemal9102/network-inceptor</a>, <a href=\"https://tensix.in\">tensix.in</a>).<br><br>I'd love to take on a practical take-home challenge or backlog task for your edge inference ingress/streaming pipeline evaluated against latency and throughput benchmarks."
    }
]

print("=== Dispatching Verified Systems Pitches to Acceldata, ChaosNative & HyperVerge ===")

for t in targets:
    recipient = t["email"]
    subject = t["subject"]
    
    text_content = f"""Hi {t['name']},

{t['observation']}

{t['pitch']}

Would you be open to assigning a challenge or pointing me toward a backlog issue?

Best,
Hemal Shah
hemal@tensix.in | github.com/hemal9102 | tensix.in
"""

    html_content = f"""<p>Hi {t['name']},</p>
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

    msg.attach(MIMEText(text_content, "plain", "utf-8"))
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=15)
        server.starttls()
        server.login(login, key)
        server.sendmail("hemal@tensix.in", [recipient], msg.as_string())
        server.quit()
        print(f"[SUCCESS] 250 OK Delivered -> {t['name']} ({recipient}) | {t['company']}")
    except Exception as e:
        print(f"[ERROR] Failed to send to {recipient}: {e}")
