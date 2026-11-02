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

followups = [
    {
        "name": "Quicknode",
        "to": ["alex@quicknode.com", "dima@quicknode.com"],
        "subject": "Re: Senior Software Engineer (Go & Rust): RPC Socket Pools, Node Ingestion & IETF Draft-Shah",
        "text": """Hi Alex, Dima,

Bumping this to the top of your inbox for the week.

If you have an open backlog ticket around RPC socket pooling or batching in Go/Rust, feel free to toss it over. Happy to write a working prototype and benchmarks so you can see how I build before getting into any interview loops.

Let me know if that works.

Hemal
hemal@tensix.in | github.com/hemal9102 | tensix.in
""",
        "html": """<p>Hi Alex, Dima,</p>
<p>Bumping this to the top of your inbox for the week.</p>
<p>If you have an open backlog ticket around RPC socket pooling or batching in Go/Rust, feel free to toss it over. Happy to write a working prototype and benchmarks so you can see how I build before getting into any interview loops.</p>
<p>Let me know if that works.</p>
<p>Hemal<br>
<a href="mailto:hemal@tensix.in">hemal@tensix.in</a> | <a href="https://github.com/hemal9102">github.com/hemal9102</a> | <a href="https://tensix.in">tensix.in</a></p>
"""
    },
    {
        "name": "Tavily",
        "to": ["rotem@tavily.com"],
        "subject": "Re: Software Engineer - Web Crawling: Socket throughput, JA4 evasion & IETF Draft-Shah",
        "text": """Hey Rotem,

Wanted to follow up on this quickly.

Rather than a standard interview loop, I'm happy to take on any open challenge you have around crawl throughput, connection pooling, or proxy handling. Just send over a benchmark or test case and I'll build it out.

Open to trying it?

Hemal
hemal@tensix.in | github.com/hemal9102 | tensix.in
""",
        "html": """<p>Hey Rotem,</p>
<p>Wanted to follow up on this quickly.</p>
<p>Rather than a standard interview loop, I'm happy to take on any open challenge you have around crawl throughput, connection pooling, or proxy handling. Just send over a benchmark or test case and I'll build it out.</p>
<p>Open to trying it?</p>
<p>Hemal<br>
<a href="mailto:hemal@tensix.in">hemal@tensix.in</a> | <a href="https://github.com/hemal9102">github.com/hemal9102</a> | <a href="https://tensix.in">tensix.in</a></p>
"""
    },
    {
        "name": "LangChain",
        "to": ["harrison@langchain.dev", "ankush@langchain.dev"],
        "subject": "Re: Python OSS / SmithDB: Client trace overhead, socket backpressure & IETF Draft-Shah",
        "text": """Hey Harrison, Ankush,

Following up on my note last week.

If there's an open ticket or annoying bug on the Smith client or trace pipeline, feel free to throw it my way. I’d rather just build something useful for you guys for 4 hours to show what I can do.

Let me know if you have something in the backlog.

Hemal
hemal@tensix.in | github.com/hemal9102 | tensix.in
""",
        "html": """<p>Hey Harrison, Ankush,</p>
<p>Following up on my note last week.</p>
<p>If there's an open ticket or annoying bug on the Smith client or trace pipeline, feel free to throw it my way. I’d rather just build something useful for you guys for 4 hours to show what I can do.</p>
<p>Let me know if you have something in the backlog.</p>
<p>Hemal<br>
<a href="mailto:hemal@tensix.in">hemal@tensix.in</a> | <a href="https://github.com/hemal9102">github.com/hemal9102</a> | <a href="https://tensix.in">tensix.in</a></p>
"""
    },
    {
        "name": "Decagon AI",
        "to": ["talent@decagon.ai"],
        "subject": "Re: Staff Software Engineer, Agent Platform (Remote) — Recursive State Synchronization & IETF Draft-Shah",
        "text": """Hey team,

Just floating this back up for Monday morning.

If you have a gnarly ticket or small prototype on the agent platform that someone hasn't had time to get to, I'd love to take a crack at it.

Let me know if you’d be up for passing one over.

Hemal
hemal@tensix.in | github.com/hemal9102 | tensix.in
""",
        "html": """<p>Hey team,</p>
<p>Just floating this back up for Monday morning.</p>
<p>If you have a gnarly ticket or small prototype on the agent platform that someone hasn't had time to get to, I'd love to take a crack at it.</p>
<p>Let me know if you’d be up for passing one over.</p>
<p>Hemal<br>
<a href="mailto:hemal@tensix.in">hemal@tensix.in</a> | <a href="https://github.com/hemal9102">github.com/hemal9102</a> | <a href="https://tensix.in">tensix.in</a></p>
"""
    }
]

def dispatch_all():
    print(f"Connecting to Brevo SMTP via {login}...")
    try:
        with smtplib.SMTP(smtp_server, smtp_port, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(login, key)
            
            for item in followups:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = item["subject"]
                msg["From"] = "Hemal Shah <hemal@tensix.in>"
                msg["To"] = ", ".join(item["to"])
                msg["Reply-To"] = "hemal@tensix.in"
                
                part1 = MIMEText(item["text"], "plain", "utf-8")
                part2 = MIMEText(item["html"], "html", "utf-8")
                msg.attach(part1)
                msg.attach(part2)
                
                server.sendmail("hemal@tensix.in", item["to"], msg.as_string())
                print(f"SUCCESS: Delivered humanized follow-up to {item['name']} -> {', '.join(item['to'])}")
    except Exception as e:
        print(f"FAILED during dispatch: {e}")

if __name__ == "__main__":
    dispatch_all()
