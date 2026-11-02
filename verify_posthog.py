import sys
sys.path.append(r"D:\projects\emaillinggggggg\crawler")
from smtp_rcpt_verifier import verify_email_comprehensive

# PostHog founders & engineering leadership
# James Hawkins (CEO & Co-founder)
# Tim Glaser (CTO & Co-founder)
targets = [
    "james@posthog.com",
    "tim@posthog.com",
    "careers@posthog.com"
]

print("=== Pre-flight Socket Verification for PostHog ===")
for t in targets:
    res = verify_email_comprehensive(t)
    status = "DELIVERABLE (250 OK)" if res['is_deliverable'] else "BLOCKED"
    print(f"{t:<22} | {status:<18} | Risk: {res['bounce_risk']:<6} | {res['reason'][:50]}")
