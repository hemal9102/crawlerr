import sys
sys.path.append(r"D:\projects\emaillinggggggg\crawler")
from smtp_rcpt_verifier import verify_email_comprehensive

# SigNoz founders:
# Pranay Prateek (CEO & Co-founder)
# Ankit Nayan (CTO & Co-founder)
targets = [
    "pranay@signoz.io",
    "ankit@signoz.io"
]

print("=== Verifying SigNoz Founders Mailboxes ===")
for t in targets:
    res = verify_email_comprehensive(t)
    status = "DELIVERABLE (250 OK)" if res['is_deliverable'] else "BLOCKED"
    print(f"{t:<22} | {status:<18} | Risk: {res['bounce_risk']:<6} | {res['reason'][:60]}")
