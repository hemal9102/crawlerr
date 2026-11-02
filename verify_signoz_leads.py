import sys
sys.path.append(r"D:\projects\emaillinggggggg\crawler")
from smtp_rcpt_verifier import verify_email_comprehensive

emails = ["pranay@signoz.io", "ankit@signoz.io", "ashu.ghildiyal@signoz.io"]
for e in emails:
    res = verify_email_comprehensive(e)
    status = "250 OK" if res.get("is_deliverable") else "REJECTED"
    reason = res.get("reason", "")[:50]
    print(f"{e:<26} | {status:<10} | {reason}")
