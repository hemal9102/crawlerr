import sys
sys.path.append(r"D:\projects\emaillinggggggg\crawler")
from smtp_rcpt_verifier import verify_email_comprehensive

# Cursor / Anysphere founders:
# Michael Truell (CEO)
# Sualeh Asif (COO / Co-founder)
# Arvid Lunnemark (CTO / Co-founder)
# Aman Sanger (Co-founder)
targets = [
    "michael@cursor.com",
    "michael@anysphere.co",
    "arvid@cursor.com",
    "arvid@anysphere.co",
    "aman@cursor.com",
    "aman@anysphere.co",
    "sualeh@cursor.com",
    "sualeh@anysphere.co"
]

print("=== Pre-flight Socket Verification for Cursor / Anysphere Founders ===")
for t in targets:
    res = verify_email_comprehensive(t)
    status = "DELIVERABLE (250 OK)" if res['is_deliverable'] else "BLOCKED"
    print(f"{t:<24} | {status:<18} | Risk: {res['bounce_risk']:<6} | {res['reason'][:50]}")
