import sys
sys.path.append(r"D:\projects\emaillinggggggg\crawler")
from smtp_rcpt_verifier import verify_email_comprehensive

emails = ["abhishek@appsmith.com", "arpit@appsmith.com", "navaneeth@tooljet.com"]
for e in emails:
    res = verify_email_comprehensive(e)
    status = "250 OK" if res.get("is_deliverable") else "REJECTED"
    print(f"{e:<26} | {status:<10} | {res.get('reason', '')[:50]}")
