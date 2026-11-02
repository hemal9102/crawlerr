import sys
sys.path.append(r"D:\projects\emaillinggggggg\crawler")
from smtp_rcpt_verifier import verify_email_comprehensive

targets = [
    "manish@dgraph.io",
    "tanmai@hasura.io",
    "abhinav@postman.com",
    "ankit@postman.com"
]

for t in targets:
    res = verify_email_comprehensive(t)
    status = "DELIVERABLE (250 OK)" if res['is_deliverable'] else "BLOCKED"
    print(f"{t:<22} | {status:<18} | Risk: {res['bounce_risk']:<6} | {res['reason'][:50]}")
