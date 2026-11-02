import sys
sys.path.append(r"D:\projects\emaillinggggggg\crawler")
from smtp_rcpt_verifier import verify_email_comprehensive

targets = [
    # Atlan: Prukalpa Sankar & Varun Banka (Co-founders)
    "prukalpa@atlan.com", "varun@atlan.com"
]

for t in targets:
    res = verify_email_comprehensive(t)
    status = "250 OK DELIVERABLE" if res.get("is_deliverable") else "REJECTED"
    print(f"{t:<24} | {status:<18} | {res.get('reason', '')[:50]}")
